"""Form run interface module

This module implements form running interface used to run app's forms in parallel.
"""

import sys
import os
import subprocess
from multiprocessing import Process
from dahakianapi.asynccomm import AsyncCommPoster
from json import JSONDecodeError

python_interpreter_path = sys.executable


class FormRunInterface:
    """Form start interface."""
    def __init__(self, path, name, direct_path=False):
        """Initialize interface process."""
        self.path = path
        self.name = name
        self.direct_path = direct_path
        self.main_process = Process(target=self.subprocess_caller)
        if not self.direct_path:
            self.scan_interface = AsyncCommPoster('no_target', self.name)

    def subprocess_caller(self):
        """Run form in subprocess."""
        if not self.direct_path:
            subprocess.call([python_interpreter_path, os.getcwd() + '\\' + self.path])
        else:
            subprocess.call([python_interpreter_path, self.path])

    def run(self):
        """Start a process."""
        self.main_process.start()

    def reset(self):
        """Reset form to be rerunned."""
        self.main_process = Process(target=self.subprocess_caller)

    def scan_for_run(self):
        """Scan whether form is about to be run."""
        try:
            curr_msg = self.scan_interface.read()
            if curr_msg['cmd'] == "Run":
                self.scan_interface.post_to_self('None')
                return True
            else:
                return False
        except:
            print(sys.exc_info()[0])
            return False

    def scan_for_killed(self):
        """Scan whether form is about to be killed."""
        try:
            curr_msg = self.scan_interface.read()
            if curr_msg['cmd'] == "Killed":
                self.scan_interface.post_to_self('None')
                return True
            elif curr_msg['cmd'] == "Kill":
                return False
            else:
                return False
        except JSONDecodeError:
            print(sys.exc_info()[0])
            return False
