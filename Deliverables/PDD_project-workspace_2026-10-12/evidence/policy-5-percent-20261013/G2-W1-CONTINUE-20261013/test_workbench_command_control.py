import os, signal, subprocess, sys, tempfile, time, unittest
from pathlib import Path

PACKET = Path.home()/'Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-CONTINUE-20261013'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PACKET))
import command_control as control
import owned_process as owned


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='workbench-control-fixture-')
        self.root = Path(self.temp.name)
        self.signals = []
        self.previous = control.install_interrupt_handlers(self.signals)
        self.children = []

    def tearDown(self):
        for child in self.children:
            self.assertTrue(child.anchor_reaped)
            self.assertEqual(owned.live_group_members(child.pid), [])
        for sig, handler in self.previous.items():
            signal.signal(sig, handler)
        self.temp.cleanup()

    def run_child(self, code, timeout=3, started=None):
        def track(child):
            self.children.append(child)
            if started: started(child)
        return control.run_owned_command([sys.executable, '-c', code], owner=owned,
            cwd=self.root, env=dict(os.environ), stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, timeout=timeout, started=track)

    def test_success_and_failure_preserve_exit_status(self):
        self.assertEqual(self.run_child('raise SystemExit(0)'), 0)
        self.assertEqual(self.run_child('raise SystemExit(7)'), 7)

    def test_timeout_reaps_owned_group(self):
        self.assertEqual(self.run_child('import time; time.sleep(30)', timeout=.1), 124)

    def test_cancellation_at_spawn_is_owned_before_delivery(self):
        with self.assertRaises(InterruptedError):
            self.run_child('import time;time.sleep(30)', started=lambda child: os.kill(os.getpid(), signal.SIGTERM))

    def test_child_exec_unblocks_term(self):
        ready = self.root/'ready'
        code = 'import signal,time,pathlib;pathlib.Path('+repr(str(ready))+').write_text(str(sorted(int(x) for x in signal.pthread_sigmask(signal.SIG_BLOCK,set()))));time.sleep(30)'
        def started(child):
            deadline = time.monotonic() + 3
            while not ready.exists() and time.monotonic() < deadline: time.sleep(.01)
            self.assertTrue(ready.exists())
            self.assertEqual(ready.read_text(), '[]')
            os.kill(child.pid, signal.SIGTERM)
        self.assertEqual(self.run_child(code, started=started), -signal.SIGTERM)

    def test_repeat_signals_do_not_interrupt_restoration(self):
        with self.assertRaises(InterruptedError): os.kill(os.getpid(), signal.SIGTERM)
        os.kill(os.getpid(), signal.SIGINT)
        with control.deferred_cleanup_interruptions() as received:
            (self.root/'first').write_text('restored')
            os.kill(os.getpid(), signal.SIGHUP)
            (self.root/'second').write_text('restored')
        self.assertEqual(self.signals, [signal.SIGTERM, signal.SIGINT])
        self.assertEqual(received, [signal.SIGHUP])
        self.assertEqual((self.root/'second').read_text(), 'restored')


if __name__ == '__main__': unittest.main(verbosity=2)
