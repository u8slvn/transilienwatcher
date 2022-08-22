import pytest

from transilienwatcher import TransilienWatcher


def test_rerwatcher_workflow(mocker, config, capsys):
    messages = [
        ["TEST: 1min", "TEST: 1h"],
        ["TEST: 2min", "TEST: 2h"],
    ]
    sleep = mocker.patch(
        "transilienwatcher.app.time.sleep", side_effect=[True, KeyboardInterrupt]
    )
    fetch_data = mocker.patch(
        "transilienwatcher.app.Transilien.fetch_data", side_effect=messages
    )

    app = TransilienWatcher(log_file="", config=config)
    with pytest.raises(KeyboardInterrupt):
        app.run()

    expected = "\n".join([m for msgs in messages for m in msgs]) + "\n"
    captured = capsys.readouterr()
    assert expected == captured.out
    assert 2 == fetch_data.call_count
    assert 2 == sleep.call_count
