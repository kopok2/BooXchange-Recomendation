"""Killable interval function runner module

Shares IntervalRunner which can be used to manage asynchronous activity.
Uses files in flag directory to share state between processes.
"""

from multiprocessing import Process
import time
import json
import os

flag_file = '_timer_flag.json'
flag_directory = 'timerflags'

# Make directory if not exist
if not os.path.exists(flag_directory):
    os.makedirs(flag_directory)


class IntervalRunner:
    """Killable function running interface."""
    def __init__(self, name, func, interval, *args, **kwargs):
        """Initialize runner.

        Args:
            name: unique runner string identifier.
            func: callable object to be run.
            interval: time in seconds between func calls.
        """
        self.name = name
        self.func = func
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.fl_url = os.getcwd()+'\\'+flag_directory+'\\'+self.name.replace("/", "_").replace("\\", "_")+flag_file
        self.main_process = Process(target=self.execute_func)
        self.set_run_state(True)

    def execute_func(self):
        """Enter interval loop."""
        while not self.stop():
            time.sleep(self.interval)
            if self.args.__len__() > 0:
                if self.kwargs.__len__() > 0:
                    self.func(self.args, self.kwargs)
                else:
                    self.func(self.args)
            else:
                if self.kwargs.__len__() > 0:
                    self.func(self.kwargs)
                else:
                    self.func()

    def run(self):
        """Start running parallel."""
        self.main_process.start()

    def stop(self):
        """Check whether to stop running.

        Returns:
            bool: stop running?
        """
        if os.path.getsize(self.fl_url) > 0:
            with open(self.fl_url) as fl_f:
                state = json.load(fl_f)
                return not state[self.name]

    def set_run_state(self, state):
        """Set running state."""
        run_state = {self.name: state}
        try:
            with open(self.fl_url, "w") as fl_f:
                fl_f.write(json.dumps(run_state, ensure_ascii=False))
        except FileNotFoundError:
            pass


def kill_timer_by_name(name):
    """Kill certain runner.

    Args:
        name: Runner string identifier.
    """
    url = os.getcwd()+'\\'+flag_directory+'\\'+name.replace("/", "_").replace("\\", "_")+flag_file
    run_state = {name: False}
    with open(url, "w") as fl_f:
        fl_f.write(json.dumps(run_state, ensure_ascii=False))
