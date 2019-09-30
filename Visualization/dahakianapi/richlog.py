import datetime
import types
import traceback
import requests
from dahakianapi.leanjson import getj


log_file_path = 'richlog.log'
SETTINGS_PATH = 'settings.json'


def clear_logs():
    """Clear log file from contents."""
    with open(log_file_path, 'w') as log_file:
        log_file.write('*'*64)


class ActionLogger(type):
    def __new__(cls, name, bases, attrs):
        for attr_name in attrs.keys():
            attr_value = attrs[attr_name]
            if isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = cls.deco(attr_value)

        return super(ActionLogger, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def deco(cls, func):
        def wrapper(*args, **kwargs):
            cls.log(cls, "Calling " + func.__name__)
            result = func(*args, **kwargs)
            cls.log(cls, "Function " + func.__name__ + " executed successfully")
            cls.log(cls, 'Result: ' + repr(result) + "\n")
            return result

        return wrapper

    def log(self, action):
        try:
            with open(log_file_path, 'a') as log_file:
                log_file.write("\n" + str(datetime.datetime.now()) + ": " + action)
        except NameError:
            pass


class ErrorHandler:
    def __init__(self, url=''):
        self.url = url

    def __call__(self, exctype, value, tb, *args, **kwargs):
        log_action('Caught exception. Logging started:')
        tracestr = ''
        for trace in traceback.format_tb(tb):
            log_action(trace)
            print(trace)
            tracestr += str(trace)
        log_action('Exception Information')
        log_action('Type:' + str(exctype))
        log_action('Value:' + str(value))
        print('Exception Information')
        print('Type:', exctype)
        print('Value:', value)
        if self.url:
            error_info = {"action": "post_error",
                          "traceback": tracestr,
                          "exctype": str(exctype),
                          "value": str(value),
                          "appid": getj(SETTINGS_PATH, "appid"),
                          "richlog": open(log_file_path, 'r').read()}
            try:
                requests.post(self.url, data=error_info)
            except:
                pass


def log_action(action):
    with open(log_file_path, 'a') as log_file:
        log_file.write("\n" + str(datetime.datetime.now()) + ": " + action)
