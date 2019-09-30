import sys

js_function_syntax = "function"  # ECMAScript 2017


class JSCaller:
    def __init__(self, function_name, browser):
        self.function_name = function_name
        self.browser = browser

    def __call__(self, *args, **kwargs):
        self.browser.ExecuteFunction(self.function_name, *args)


def set_py_functions(js_files, html_files, browser):
    """Make JavaScript functions available in Python."""
    for source in js_files + html_files:
        try:
            for line in open(source):
                if js_function_syntax in line:
                    js_function_name = get_js_function_name(line)
                    if js_function_name:
                        if js_function_name != "print":
                            setattr(sys.modules['__main__'], js_function_name, JSCaller(js_function_name, browser))
                            sys.modules['__main__'].localform.js_functions[js_function_name] = JSCaller(js_function_name, browser)
        except UnicodeDecodeError:
            pass


def get_js_function_name(line):
    """Returns JavaScript function name from line"""
    f_name_start_pos = line.find(js_function_syntax)+js_function_syntax.__len__()
    f_name_stop_pos = line.find("(")
    if f_name_stop_pos > f_name_start_pos:
        return line[f_name_start_pos:f_name_stop_pos].replace(" ", "")
    else:
        return None


def get_js_sources(source):
    result = []
    for line in source.split("\n"):
        if "<script" in line:
            if "src=" in line:
                src_inline = line.split('src=')[1]
                xml_char = src_inline[0]
                src_inline = src_inline.split(xml_char)[1]
                result.append(src_inline)
    return result