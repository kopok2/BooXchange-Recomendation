"""Settings access module.

Handles simple reading, writing and deletion of properties.
"""

import json


def setj(path, setting, value):
    """Set setting.

    Args:
        path: setting file path (str).
        setting: setting key (str).
        value: setting value to be set (object).
    """
    settings = {}
    with open(path, 'r') as conf_file:
        settings = json.load(conf_file)
    settings[setting] = value
    with open(path, 'w') as conf_file:
        json.dump(settings, conf_file)


def getj(path, setting):
    """Get setting value.

    Args:
        path: setting file path (str).
        setting: setting key (str).

    Returns:
        value of setting (object).
    """
    with open(path, 'r') as conf_file:
        settings = json.load(conf_file)
        return settings[setting]


def remj(path, setting):
    """Remove setting.

    Args:
        path: setting file path (str).
        setting: setting key (str).
    """
    settings = {}
    with open(path, 'r') as conf_file:
        settings = json.load(conf_file)
    settings.pop(setting, None)
    with open(path, 'w') as conf_file:
        json.dump(settings, conf_file)
