import traceback


class ErrorHandler:
    def __init__(self, form_name):
        self.form_name = form_name

    def __call__(self, exctype, value, tb, *args, **kwargs):
        for trace in traceback.format_tb(tb):
            print(trace)
        print('Exception Information')
        print('Type:', exctype)
        print('Value:', value)
        print('Exception occured in: '+self.form_name)
