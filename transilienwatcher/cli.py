#!/usr/bin/env python3
import argparse
import sys
from enum import Enum, auto
from pathlib import Path

from loguru import logger

from transilienwatcher import ConfigManager, LOG_FILE, CONFIG_FILE, WORKSPACE
from transilienwatcher import TransilienWatcher


def _app_already_init():
    return Path(WORKSPACE).is_dir() and Path(CONFIG_FILE).is_file()


def run():
    if not _app_already_init():
        print(
            "It appears that it may be the first time you run TransilienWatcher."
            "\nYou need to run 'transilienwatcher-init' first."
        )
        sys.exit()

    parser = argparse.ArgumentParser(description="TransilienWatcher")
    parser.add_argument(
        dest="operation",
        type=str,
        choices=["start", "stop", "status"],
        help="TransilienWatcher commands.",
    )
    args = parser.parse_args()

    logger.remove()  # Reset default loguru logger.
    logger.add(LOG_FILE, rotation="00:00", retention="2 days", level="DEBUG")
    config = ConfigManager.load(file=CONFIG_FILE)

    daemon = TransilienWatcher(log_file=LOG_FILE, config=config)
    operation = getattr(daemon, args.operation)
    operation()


def init():
    if _app_already_init():
        print(f"TranslienWatcher config already exists in '{WORKSPACE}'.")
        return

    class Status(Enum):
        ASK_SETUP = auto()
        ASK_QUIT = auto()
        SETUP = auto()
        QUIT = auto()

    setup_status = Status.ASK_SETUP
    while setup_status != Status.QUIT:
        if setup_status == Status.ASK_SETUP:
            resp = input("Setup TransilienWatcher configuration file? [Y/n]: ") or "y"
            if resp.lower() in ["y", "yes"]:
                setup_status = Status.SETUP
            if resp.lower() in ["n", "no"]:
                setup_status = Status.ASK_QUIT
        if setup_status == Status.ASK_QUIT:
            resp = (
                input("Setup is mandatory to run the app, are you sure? [Y/n]: ") or "y"
            )
            if resp.lower() in ["y", "yes"]:
                setup_status = Status.QUIT
            if resp.lower() in ["n", "no"]:
                setup_status = Status.ASK_SETUP
        if setup_status == Status.SETUP:
            print("Setting up TransilienWatcher...")
            Path(WORKSPACE).mkdir(exist_ok=True)
            print("Creating TransilienWatcher config...")
            ConfigManager.create(CONFIG_FILE)
            print(
                f"All done!\n\nYou can now edit TransilienWatcher config in "
                f"'{CONFIG_FILE}' and then start the app."
            )
            setup_status = Status.QUIT
    sys.exit()
