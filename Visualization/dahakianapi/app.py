"""Dahakian desktop application class module

This module implements a class used to manage app's forms and state.
"""
import os
import time
from dahakianapi.formrun import FormRunInterface
from dahakianapi.intervalrun import kill_timer_by_name
from dahakianapi.richlog import clear_logs
scan_interval = 0.2


class App:
    """Desktop application class."""
    def __init__(self, app_version, form_list_path='forms.txt', mainformoverride=None):
        """Initialize an application.

        Args:
            app_version: Version of application.
            form_list_path: Path to file with forms listed.
        """

        self.app_version = app_version
        clear_logs()

        # Initialize run interfaces
        self.running_forms = []
        if mainformoverride:
            self.main_form = FormRunInterface(mainformoverride+'.py', mainformoverride)
        else:
            self.main_form = None
        self.run_interfaces = []
        for form in open(form_list_path):
            form = form.strip()
            form_runner = FormRunInterface(form+'.py', form)
            setattr(self, form, form_runner)
            if self.main_form is None:
                self.main_form = form_runner
            self.run_interfaces.append(form_runner)

        self.run()

    def run(self):
        """Run an application."""
        self.main_form.run()
        self.running_forms.append(self.main_form.name)
        while True:
            for interface in self.run_interfaces:
                if interface.scan_for_run():
                    if interface.name not in self.running_forms:
                        print('Launching ' + interface.name )
                        interface.run()
                        self.running_forms.append(interface.name)
                    else:
                        print('Warning: '+interface.name+' already started.')
                    print('Active forms: ', self.running_forms)
                if interface.scan_for_killed():
                    print('Killing ' + interface.name)
                    if interface.name in self.running_forms:
                        self.running_forms.remove(interface.name)
                    print('Active forms: ', self.running_forms)
                    interface.reset()
            if self.running_forms.__len__() == 0:
                self.terminate()
                break
            time.sleep(scan_interval)

    def terminate(self):
        """Join remaining processes."""
        for interface in self.run_interfaces:
            kill_timer_by_name(interface.name)
            if interface.main_process.is_alive():
                interface.main_process.join()
