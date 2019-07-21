import atexit
import os
import signal
import sys
from abc import ABC, abstractmethod


class Daemon(ABC):
    def __init__(self,
                 pidfile: str,
                 app_name: str,
                 stdin: str = '/dev/null',
                 stdout: str = '/dev/null',
                 stderr: str = '/dev/null'
                 ):
        self.pidfile = pidfile
        self.app_name = app_name
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def daemonize(self):
        if self._is_running():
            raise RuntimeError(f"{self.app_name} is already Running.")

        self.fork_os()

        os.chdir('/')
        os.umask(0)
        os.setsid()

        self.fork_os()

        sys.stdout.flush()
        sys.stderr.flush()

        with open(self.stdin, 'rb') as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open(self.stdout, 'ab') as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
        with open(self.stderr, 'ab') as f:
            os.dup2(f.fileno(), sys.stderr.fileno())

        with open(self.pidfile, 'w') as f:
            print(os.getpid(), file=f)

        atexit.register(lambda: os.remove(self.pidfile))

        def sigterm_handler(signo, frame):
            raise SystemExit(1)

        signal.signal(signal.SIGTERM, sigterm_handler)

    @staticmethod
    def fork_os():
        try:
            if os.fork() > 0:
                raise SystemExit(0)
        except OSError:
            raise RuntimeError("Fork failed.")

    def _is_running(self):
        return os.path.exists(self.pidfile)

    def start(self):
        self.daemonize()
        self.run()

    def stop(self):
        if not self._is_running():
            print(f"{self.app_name} is not running.")
            raise SystemExit(1)

        with open(self.pidfile) as f:
            pid = int(f.read())
            os.kill(pid, signal.SIGTERM)

    @abstractmethod
    def run(self):
        raise NotImplementedError
