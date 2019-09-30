"""Misc tools module

Implements additional tools for multiprocessing.
"""

import os
import sys
import jsonpickle
from multiprocessing import Process
import subprocess


def get_current_name(name):
    """Get name of currently running module.

    Args:
        name: Current __name__

    Returns:
        name: Name of the script file; replaces __main__ with filename.
    """
    file = sys.modules[name].__file__
    path = file[os.getcwd().__len__()+1:]
    s = ''
    for x in path:
        s = x + s
    s = s.split('.')[1]
    name = ''
    for x in s:
        name = x + name
    return name


def accurate_json_dump(name, url, message):
    """Dump message to url file.

    Args:
        name: Current __name__.
        url: Dump file url.
        message: Any object to be dumped in file.
    """
    with open(url, "w") as comm:
        comm.write(jsonpickle.encode(message))
    accurate_message = []
    for line in open(url):
        accurate_message.append(line.replace('__main__', get_current_name(name)))
    with open(url, "w") as comm:
        for line in accurate_message:
            comm.write(line)

def run_script(path):
    subprocess.call([sys.executable, path])

def pyrun(path):
    run_process = Process(target= run_script, args=(path,))
    run_process.start()
    