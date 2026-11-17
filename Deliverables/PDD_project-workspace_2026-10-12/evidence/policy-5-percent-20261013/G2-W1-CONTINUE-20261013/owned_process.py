#!/usr/bin/env python3
"""Exclusive, bounded AgentD installation. No writes to config or Keychain.

Manual binary/config/plist editors must cooperate with the same advisory lock.
SIGKILL/power loss cannot be trapped; keep the verified backup for recovery.
Only main() uses the real launchctl. Tests inject stand-ins into Transaction.
"""
import ctypes
import errno
import ipaddress
import tempfile
import fcntl
import hashlib
import json
import os
from pathlib import Path
import plistlib
import re
import shutil
import signal
import selectors
import subprocess
import sys
import time
import urllib.request
import urllib.error


_pending_subprocesses = {}

def digest(path):
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        raise RuntimeError('file missing or symlink')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def live_group_members(pgid):
    """Darwin libproc inventory; zombies have no executable work or held locks.

    A denied/incomplete inventory fails closed, never masquerades as an empty group.
    """
    lib = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
    count = 256
    while count <= 1048576:
        buffer = (ctypes.c_int * count)()
        ctypes.set_errno(0)
        size = lib.proc_listpids(2, int(pgid), buffer, ctypes.sizeof(buffer))
        if size < 0 or (size == 0 and ctypes.get_errno()):
            raise RuntimeError('process-group inventory failed')
        if size < ctypes.sizeof(buffer): break
        count *= 2
    else: raise RuntimeError('process-group inventory exceeded bound')
    live = []
    for pid in buffer[:size // ctypes.sizeof(ctypes.c_int)]:
        if not pid: continue
        info = (ctypes.c_uint32 * 34)()  # Darwin proc_bsdinfo: 136 bytes, status second field.
        ctypes.set_errno(0)
        result = lib.proc_pidinfo(pid, 3, 0, info, ctypes.sizeof(info))
        if result == 0 and ctypes.get_errno() == errno.ESRCH: continue
        if result != ctypes.sizeof(info): raise RuntimeError('process-group member inspection failed')
        if info[1] != 5: live.append(pid)  # SZOMB: cannot execute or retain file descriptors.
    return live


class _DarwinSigInfo(ctypes.Structure):
    # SDK sys/signal.h siginfo_t; waitid only uses signo/code/pid/status here.
    _fields_ = [('signo', ctypes.c_int), ('error', ctypes.c_int), ('code', ctypes.c_int),
                ('pid', ctypes.c_int), ('uid', ctypes.c_uint), ('status', ctypes.c_int),
                ('addr', ctypes.c_void_p), ('value', ctypes.c_void_p),
                ('band', ctypes.c_long), ('pad', ctypes.c_ulong * 7)]


class OwnedPopen(subprocess.Popen):
    """Observe exit with WNOWAIT; reap only after owned-group emptiness proof.

    communicate(), wait() and poll() retain our child PID as a kernel lifetime
    anchor. A zombie cannot execute, but its unreaped PID cannot be reused.
    """
    def __init__(self, *args, **kwargs):
        if kwargs.get('start_new_session') is not True:
            raise ValueError('owned process requires its own session')
        self.anchor_lost = False
        self.anchor_reaped = False
        super().__init__(*args, **kwargs)

    def _communicate(self, input, endtime, orig_timeout):
        limit = getattr(self, '_bounded_output_limit', None)
        if limit is None:
            return super()._communicate(input, endtime, orig_timeout)
        if input is not None or self.stdout is None or self.stderr is not None:
            raise RuntimeError('unsupported bounded subprocess channels')
        output = bytearray()
        fd = self.stdout.fileno()
        os.set_blocking(fd, False)
        with selectors.DefaultSelector() as selector:
            selector.register(fd, selectors.EVENT_READ)
            while True:
                remaining = endtime - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(self.args, orig_timeout)
                if not selector.select(min(.05, remaining)):
                    continue
                try: chunk = os.read(fd, 16384)
                except BlockingIOError: continue
                if not chunk: break
                if len(chunk) > limit - len(output):
                    raise RuntimeError('subprocess output limit exceeded')
                output.extend(chunk)
        self.wait(timeout=max(0, endtime-time.monotonic()))
        value = bytes(output)
        if self.text_mode:
            value = self._translate_newlines(value, self.stdout.encoding, self.stdout.errors)
        return value, None

    def _try_wait(self, wait_flags):
        if sys.platform == 'darwin':
            info = _DarwinSigInfo()
            lib = ctypes.CDLL(None, use_errno=True)
            rc = lib.waitid(1, self.pid, ctypes.byref(info), 4 | 32 | (wait_flags & os.WNOHANG))
            if rc != 0:
                error = ctypes.get_errno()
                if error == errno.EINTR: return 0, 0
                if error == errno.ECHILD: self.anchor_lost = True
                raise OSError(error, 'owned child exit observation failed')
            return info.pid, (info.status << 8 if info.code == 1 else info.status & 127)
        info = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOWAIT | (wait_flags & os.WNOHANG))
        if info is None: return 0, 0
        return info.si_pid, (info.si_status << 8 if info.si_code == os.CLD_EXITED else info.si_status & 127)

    def _internal_poll(self, _deadstate=None, **unused):
        if self.returncode is None and self._waitpid_lock.acquire(False):
            try:
                pid, status = self._try_wait(os.WNOHANG)
                if pid == self.pid: self._handle_exitstatus(status)
            except OSError:
                self.anchor_lost = True
            finally:
                self._waitpid_lock.release()
        return self.returncode

    def owns_group(self):
        if self.anchor_lost or self.anchor_reaped: return False
        try:
            pid, _ = self._try_wait(os.WNOHANG)  # Exact unreaped child lifetime proof.
            # Darwin getpgid rejects zombies. WNOWAIT still proves the reserved
            # child PID, whose original session-leader PGID cannot be reused.
            return pid == self.pid or os.getpgid(self.pid) == self.pid
        except OSError:
            self.anchor_lost = True
            return False

    def reap_after_group_proof(self):
        with self._waitpid_lock:
            if self.anchor_reaped: return
            while True:
                try:
                    _, status = os.waitpid(self.pid, 0)
                    self._handle_exitstatus(status)
                    self.anchor_reaped = True
                    return
                except InterruptedError: continue
                except ChildProcessError:
                    # Only called after independent group-empty proof. Already
                    # reaped/lost children are never signalling authority.
                    self.anchor_lost = True
                    self.anchor_reaped = True
                    if self.returncode is None: self.returncode = 255
                    return


def observe_exit_for_cleanup(process):
    """Exit observations cannot abandon the group-empty proof barrier."""
    try: return process.poll()
    except OSError:
        if isinstance(process, OwnedPopen): process.anchor_lost = True
        return None


def terminate_group(process, grace=5):
    pgid = process.pid
    # Current members never authorize signalling. Our own unreaped child does.
    anchored = isinstance(process, OwnedPopen) and process.owns_group()
    def send(sig):
        if not anchored or not process.owns_group(): return
        try: os.killpg(pgid, sig)
        except OSError: pass  # Signal failure never authorizes abandoning the proof barrier.
    def members():
        try: return live_group_members(pgid)
        except Exception: return None
    current = members()
    if anchored: send(signal.SIGTERM)
    deadline = time.monotonic() + grace
    while current != [] and time.monotonic() < deadline:
        time.sleep(.02)
        current = members()
    if anchored: send(signal.SIGKILL)
    deadline = time.monotonic() + 5
    while current != [] and time.monotonic() < deadline:
        observe_exit_for_cleanup(process)
        time.sleep(.02)
        current = members()
    # A bounded signal attempt is not a bounded right to abandon an unknown
    # group. Retain the actual supervisor (and its flock) until proof recovers.
    # No recovery, terminal success/failure, or lock release can escape this barrier.
    if current != []:
        print('cleanup: group emptiness unverified; supervisor retained', flush=True)
    while current != []:
        observe_exit_for_cleanup(process)
        time.sleep(.1)
        current = members()
    if isinstance(process, OwnedPopen): process.reap_after_group_proof()
    else: process.wait(timeout=1)


