import os
import signal

import pytest

from transilienwatcher.daemon import Daemon

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
    os = mocker.patch('transilienwatcher.daemon.os', **{
        'fork.return_value': 0,
        'path.exists.side_effect': [False, True],
        'getpid.return_value': 42,
    })
    mocker.patch('transilienwatcher.daemon.sys')
    daemon_app = DaemonApp()

    daemon_app.start()
    daemon_app.stop()

    assert os.fork.call_count == 2
    captured = capsys.readouterr()
    assert 'Daemon working!\n' == captured.out
    assert os.remove.called_once_with(pidfile)
    assert os.kill.called_once_with(42, signal.SIGTERM)


def test_daemon_do_not_start_if_os_fork_fails(mocker):
    mocker.patch('transilienwatcher.daemon.os.fork', side_effect=[1, OSError])
    daemon_app = DaemonApp()

    with pytest.raises(SystemExit):
        daemon_app.fork_os()
    with pytest.raises(RuntimeError):
        daemon_app.fork_os()


def test_daemon_do_not_start_if_already_running(mocker):
    mocker.patch('transilienwatcher.daemon.os.path.exists', return_value=True)
    daemon_app = DaemonApp()

    with pytest.raises(RuntimeError):
        daemon_app.start()


def test_daemon_do_not_stop_if_not_running(mocker):
    mocker.patch('transilienwatcher.daemon.os.path.exists', return_value=False)
    daemon_app = DaemonApp()

    with pytest.raises(SystemExit):
        daemon_app.stop()


@pytest.mark.parametrize('is_running, expected', [
    (True, 'TestApp is running.\n'),
    (False, 'TestApp is not running.\n'),
])
def test_daemon_status(mocker, capsys, is_running, expected):
    mocker.patch(
        'transilienwatcher.daemon.Daemon._is_running',
        return_value=is_running
    )
    daemon_app = DaemonApp()

    daemon_app.status()

    captured = capsys.readouterr()
    assert expected == captured.out
