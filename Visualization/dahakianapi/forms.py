"""Dahakian forms module

Shares a superclass of form to be extended with user's functionality.
"""

import json
import os
import sys
import inspect
from dahakianapi.asynccomm import AsyncCommPoster
from dahakianapi.otherforminterface import OtherForm
from dahakianapi.jsfunctioninterface import set_py_functions, get_js_sources
from dahakianapi.richlog import ActionLogger, ErrorHandler
from cefpython3 import cefpython as cef
import atexit
from tkinter import filedialog, messagebox
import tkinter as tk

form_list_url = "forms.json"
form_directory = 'form_manifests'
scan_interval = 0.1

# Make directory if not exist
if not os.path.exists(form_directory):
    os.makedirs(form_directory)


class Form(metaclass=ActionLogger):
    """Desktop form class.

    Should be subclassed for usage.
    """
    def __init__(self, formname, error_url=''):
        """Initialize form.

        Args:
            formname: Name of the form.
        """
        self.error_url = error_url
        self.js_functions = {}
        self.formname = formname
        data = json.load(open(form_list_url))
        self.caption = data[self.formname]['form_caption']
        self.html_url = os.getcwd()+'\\'+data[self.formname]['form_html_url']
        self.browser = None
        self.own_comm = AsyncCommPoster(self.formname, self.formname)
        atexit.register(self.own_comm.post_to_self, 'Killed')
        self.register_manifest()
        bounds = (0, 0, 0, 0)
        self.x = bounds[0]
        self.y = bounds[1]
        self.height = bounds[2]
        self.width = bounds[3]
        self.js_sources = get_js_sources(open(self.html_url).read())
        self.js_callables = []

    def run(self):
        """Launch form with separate Chromium instance."""
        settings = {'context_menu': {   'navigation': True,
                                        'print': False,
                                        'view_source': False,
                                        'external_browser': False,
                                        'devtools': True
                    }

                    }
        commandLineSwitches = {}
        cef.Initialize(settings, commandLineSwitches)
        sys.excepthook = ErrorHandler(url=self.error_url)
        self.browser = cef.CreateBrowserSync(url=self.html_url, window_title=self.caption)
        self.set_js_functions()
        set_py_functions(self.js_sources, [self.html_url], self.browser)
        self.load_external_interfaces()
        cef.MessageLoop()
        self.on_form_close()
        cef.Shutdown()

    def set_js_functions(self):
        """Make Python functions available in JavaScript.

        Args:
            browser: Chromium browser handler.
        """
        bindings = cef.JavascriptBindings(
            bindToFrames=False, bindToPopups=False)
        functions = inspect.getmembers(sys.modules[__name__], inspect.isfunction) + inspect.getmembers(self, inspect.ismethod)
        functions += inspect.getmembers(sys.modules['__main__'], inspect.isfunction)

        for py_function in functions:
            bindings.SetFunction(*py_function)
        self.browser.SetJavascriptBindings(bindings)

    def register_object_methods(self, obj, name):
        methods = inspect.getmembers(obj, inspect.ismethod)
        for method in methods:
            setattr(self, '__'+name+'__'+method[0], method[1])
        self.set_js_functions()

    def close_form(self):
        """Shutdown form."""
        self.on_form_close()
        self.own_comm.post_to_self('Killed')
        self.__del__()

    def show(self):
        pass

    def hide(self):
        pass

    def check_comm(self):
        """Check for asynchronous commands for form and execute them."""
        msg = self.own_comm.read()
        if msg['cmd'] == 'Kill':
            self.on_form_close()
            self.own_comm.post_to_self('Killed')
            self.__del__()

        elif msg['cmd'] == 'Exec':
            func = getattr(self, msg['func'])
            args = msg['args'][0]
            kwargs = msg['kwargs']
            if args.__len__() > 0:
                if kwargs.__len__() > 0:
                    result = func(*args, **kwargs)
                else:
                    result = func(*args)
            else:
                if kwargs.__len__() > 0:
                    result = func(**kwargs)
                else:
                    result = func()

            self.own_comm.post_to_self('Retn', result)
        elif msg['cmd'] == 'Get':
            result = getattr(self, msg['args'][0])
            self.own_comm.post_to_self('Retn', result)
        elif msg['cmd'] == 'Set':
            setattr(self, msg['args'][0], msg['args'][1])
            self.own_comm.post_to_self('None')

    def __del__(self):
        cef.Shutdown()

    def register_manifest(self):
        """Save manifest with form's methods."""
        functions = inspect.getmembers(sys.modules[__name__], inspect.isfunction) + inspect.getmembers(self, inspect.ismethod)
        with open(os.getcwd()+"\\"+form_directory+"\\"+self.formname+'.txt', 'w') as manifest:
            for py_function in functions:
                manifest.write(py_function[0]+'\n')

    def load_external_interfaces(self):
        """Load other forms's interfaces."""
        forms = json.load(open(form_list_url)).keys()
        for key in forms:
            if key != self.formname:
                setattr(sys.modules['__main__'], key, OtherForm(key, self.formname, scan_interval, form_directory))

    def toggle_fullscreen(self):
        """Change form fullscreen state."""
        self.browser.ToggleFullscreen()
        self.browser.maximized = False

    def enter_fullscreen(self):
        """Make form window fullscreen."""
        if not self.browser.IsFullscreen():
            self.browser.ToggleFullscreen()

    def leave_fullscreen(self):
        """Leave fullscreen mode."""
        if self.browser.IsFullscreen():
            self.browser.ToggleFullscreen()

    def toggle_maximized(self):
        """Change form window maximized state."""
        self.enter_fullscreen()
        self.browser.maximized = not self.browser.maximized
        self.leave_fullscreen()

    def set_bounds(self, x1, y1, x2, y2):
        """Set form window screen rect."""
        self.enter_fullscreen()
        self.browser.windowRect = (x1, y1, x2, y2)
        self.browser.maximized = False
        self.leave_fullscreen()

    def set_focus(self):
        """Set focus on form window."""
        self.browser.SetFocus(True)

    def file_open_dialog(self):
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename()

    def dialog_box(self, mess, title):
        root = tk.Tk()
        root.withdraw()
        return messagebox.askyesno(title, mess)

    def file_save_dialog(self, title):
        root = tk.Tk()
        root.withdraw()
        return filedialog.asksaveasfilename(title=title)

    def dir_dialog(self, title):
        root = tk.Tk()
        root.withdraw()
        return filedialog.askdirectory(parent=root, initialdir="/", title=title)

    def on_form_close(self):
        return True

    def load_js_functions(self):
        set_py_functions(self.js_sources, [self.html_url], self.browser)
