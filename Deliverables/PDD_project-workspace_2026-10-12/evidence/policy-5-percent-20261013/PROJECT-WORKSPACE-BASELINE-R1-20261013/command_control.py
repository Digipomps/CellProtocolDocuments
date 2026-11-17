from pathlib import Path
from contextlib import contextmanager
import os, signal, subprocess, sys
HERE=Path(__file__).resolve().parent
SIGNALS={signal.SIGTERM,signal.SIGINT,signal.SIGHUP}

def run_owned_command(args, *, owner, cwd, env, stdout, stderr, timeout, started=None):
    """Install cleanup ownership before any pending parent interruption is delivered."""
    previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, SIGNALS)
    child = None
    try:
        # The launcher resets the mask inherited from this blocked spawn window.
        child = owner.OwnedPopen([sys.executable, str(HERE/'child_exec.py'), *args],
                cwd=cwd, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        if started is not None: started(child)
        signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        try: return child.wait(timeout=timeout)
        except subprocess.TimeoutExpired: return 124
    finally:
        signal.pthread_sigmask(signal.SIG_BLOCK, SIGNALS)
        try:
            if child is not None: owner.terminate_group(child)
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)


def install_interrupt_handlers(received):
    """Raise once; record repeat cancellations through the entire cleanup path."""
    def record(signum, frame):
        if signum not in received: received.append(signum)
    def interrupted(signum, frame):
        previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, SIGNALS)
        record(signum, frame)
        try:
            for sig in SIGNALS: signal.signal(sig, record)
        finally: signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        raise InterruptedError('Interrupted by signal '+str(signum))
    previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, SIGNALS)
    try: return {sig:signal.signal(sig, interrupted) for sig in SIGNALS}
    finally: signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)


@contextmanager
def deferred_cleanup_interruptions():
    """Catchable repeat signals record cancellation without interrupting restoration."""
    previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, SIGNALS)
    previous_handlers = {s:signal.getsignal(s) for s in SIGNALS}
    received = []
    def record(signum, frame):
        if signum not in received: received.append(signum)
    for signum in SIGNALS: signal.signal(signum, record)
    signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
    try: yield received
    finally:
        signal.pthread_sigmask(signal.SIG_BLOCK, SIGNALS)
        try:
            for signum, handler in previous_handlers.items(): signal.signal(signum, handler)
        finally: signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)


