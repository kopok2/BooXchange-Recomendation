"""Asynchronous cross-process communication module

Used for communication between main app thread and form subprocesses.
"""

import jsonpickle
import os
from dahakianapi.processmisctools import accurate_json_dump
from json import JSONDecodeError
import time

local_comm_file = 'comm.json'
comm_directory = 'crosscomm'
reread_time = 0.4

# Make directory if not exist
if not os.path.exists(comm_directory):
    os.makedirs(comm_directory)


class AsyncCommPoster:
    """Async communication interface class.

    Used to send objects and calls through json file.
    """
    def __init__(self, target, source):
        """Initialize asynchronous interface.

        Args:
            target: target of comm interface.
            source: source of communication.
        """
        self.target = target
        self.source = source
        self.comm_target_url = os.getcwd()+'\\'+comm_directory+'\\'+self.target+local_comm_file
        self.comm_source_url = os.getcwd()+'\\'+comm_directory+'\\'+self.source+local_comm_file
        self.comm_target_url = self.comm_target_url.replace("/", "\\")
        self.comm_source_url = self.comm_source_url.replace("/", "\\")
        self.post('None')
        self.post_to_self('None')

    def post(self, cmd, *args, **kwargs):
        """Post args to comm file.

        Args:
            cmd: defined action to be send.
            *args: subject of sent action.
        """
        message = {
            "cmd": cmd,
            "args": args,
            "kwargs": kwargs,
            "target": self.target,
            "source": self.source
        }
        accurate_json_dump(__name__, self.comm_target_url, message)

    def post_to_self(self, cmd, *args, **kwargs):
        """Post args to comm file.

        Args:
            cmd: defined action to be send.
            *args: subject of sent action.
        """
        message = {
            "cmd": cmd,
            "args": args,
            "kwargs": kwargs,
            "target": self.target,
            "source": self.source
        }
        accurate_json_dump(__name__, self.comm_source_url, message)

    def read(self):
        """Read from interface where self is target."""
        try:
            return jsonpickle.decode(open(self.comm_source_url).read())
        except JSONDecodeError:
            time.sleep(reread_time)
            return self.read()

    def read_target(self):
        """Read self sent message."""
        try:
            return jsonpickle.decode(open(self.comm_target_url).read())
        except JSONDecodeError:
            time.sleep(reread_time)
            return self.read()
