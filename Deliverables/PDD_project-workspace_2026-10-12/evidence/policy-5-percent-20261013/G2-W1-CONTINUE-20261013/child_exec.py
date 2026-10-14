"""Reset only the parent spawn-window mask, then execute the packet command."""
import os
import signal
import sys


def main():
    if len(sys.argv) < 2:
        raise SystemExit(64)
    signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGTERM, signal.SIGINT, signal.SIGHUP})
    os.execvpe(sys.argv[1], sys.argv[1:], os.environ)


if __name__ == '__main__':
    main()
