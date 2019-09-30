"""Customized form asynchronous interface module"""

from dahakianapi.asynccomm import AsyncCommPoster, comm_directory, local_comm_file
from dahakianapi.processmisctools import accurate_json_dump
import time
import os


class Runner:
    """Generator class to run external functions."""
    def __init__(self, poster, func_name):
        """Create callable object.

        Args:
            poster: An AsyncCommPoster object.
            func_name: function name.
        """
        self.poster = poster
        self.func_name = func_name

    def __call__(self, *args, **kwargs):
        """Run external function and wair for result."""
        if self.func_name == 'run':
            self.poster.post('Run', args, kwargs)
        elif self.func_name == 'close_form':
            self.poster.post('Kill', args, kwargs)
        else:
            if kwargs.__len__() == 0:
                kwargs = ()
            self.poster.post_exec('Exec', self.func_name, args, kwargs)
            time.sleep(self.poster.comm_interval * 2)
            return self.poster.read_target()['args']


class OtherForm(AsyncCommPoster):
    """Seamless other forms interface class."""
    def __init__(self, target, source, comm_interval, manifest_source):
        """Initialize customized interface.

        Args:
            target: target form (str)
            source: source form (str)
            comm_interval: interval between comm checks (int) [seconds]
            manifest_source: form manifests directory URL (str)
        """
        self.__dict__['target'] = target
        self.__dict__['source'] = source
        self.__dict__['comm_target_url'] = os.getcwd() + '\\' + comm_directory + '\\' + self.target + local_comm_file
        self.__dict__['comm_source_url'] = os.getcwd() + '\\' + comm_directory + '\\' + self.source + local_comm_file
        self.post('None')
        self.post_to_self('None')
        self.__dict__['comm_interval'] = comm_interval
        self.__dict__['manifest_source'] = os.getcwd()+"\\"+manifest_source+"\\"+self.target+'.txt'
        for func in open(self.manifest_source, 'r'):
            func = func.strip()
            self.__dict__[func] = Runner(self, func)

    def post_exec(self, cmd, func, *args, **kwargs):
        """Post an exec command."""
        message = {
            "cmd": cmd,
            "args": args,
            "func": func,
            "kwargs": kwargs,
            "target": self.target,
            "source": self.source
        }
        accurate_json_dump(__name__, self.comm_target_url, message)

    def __getattr__(self, item):
        """Override to implement external interface."""
        self.post('Get', item)
        time.sleep(self.comm_interval*2)
        result = self.read_target()
        if result['cmd'] == 'Retn':
            return result['args'][0]
        else:
            time.sleep(self.comm_interval * 4)
            result = self.read_target()
            if result['cmd'] == 'Retn':
                return result['args'][0]
            else:
                return None

    def __setattr__(self, key, value):
        """Override to implement external interface."""
        self.post('Set', key, value)
