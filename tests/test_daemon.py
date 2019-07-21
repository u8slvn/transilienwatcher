import os
import signal

import pytest

from rerwatcher.daemon import Daemon

base_dir = os.getcwd()
pidfile = f'{base_dir}/test_pid'


class DaemonApp(Daemon):
    def __init__(self):
        super(DaemonApp, self).__init__(
            pidfile=pidfile,
            app_name='TestApp'
        )

    def run(self):
        print('Daemon working!')


# TODO: find a better way to test the real case.
def test_daemon(mocker, capsys):
    os = mocker.patch('rerwatcher.daemon.os', **{
        'fork.return_value': 0,
        'path.exists.side_effect': [False, True],
        'getpid.return_value': 42,
    })
    mocker.patch('rerwatcher.daemon.sys')
    daemon_app = DaemonApp()

    daemon_app.start()
    daemon_app.stop()

    assert os.fork.call_count == 2
    captured = capsys.readouterr()
    assert 'Daemon working!\n' == captured.out
    assert os.remove.called_once_with(pidfile)
    assert os.kill.called_once_with(42, signal.SIGTERM)


def test_daemon_do_not_start_if_os_fork_fails(mocker):
    mocker.patch('rerwatcher.daemon.os', **{
        'path.exists.return_value': False,
        'fork.return_value': 1,
    })
    daemon_app = DaemonApp()

    with pytest.raises(SystemExit):
        daemon_app.start()


def test_daemon_do_not_start_if_os_fork2_fails(mocker):
    mocker.patch('rerwatcher.daemon.os', **{
        'path.exists.return_value': False,
        'fork.side_effect': [0, 1],
    })
    daemon_app = DaemonApp()

    with pytest.raises(SystemExit):
        daemon_app.start()


def test_daemon_do_not_start_if_already_running(mocker):
    mocker.patch('rerwatcher.daemon.os.path.exists', return_value=True)
    daemon_app = DaemonApp()

    with pytest.raises(RuntimeError):
        daemon_app.start()


def test_daemon_do_not_stop_if_not_running(mocker):
    mocker.patch('rerwatcher.daemon.os.path.exists', return_value=False)
    daemon_app = DaemonApp()

    with pytest.raises(SystemExit):
        daemon_app.stop()
