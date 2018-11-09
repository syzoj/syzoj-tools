import subprocess
import tempfile

all_checkers = None

def load_checkers():
    global all_checkers
    if all_checkers == None:
        from .builtin import BuiltinChecker
        from .testlib import TestlibChecker
        from .loj import LojChecker
        all_checkers = {
            "builtin": BuiltinChecker,
            "testlib": TestlibChecker,
            "loj": LojChecker
        }

def get_all_checkers():
    global all_checkers
    load_checkers()
    return all_checkers

def get_checker(name):
    global all_checkers
    load_checkers()
    return all_checkers.get(name)

class CheckerResult:
    def __init__(self, success, score=0, message=None):
        self.success = success
        self.score = score
        self.message = message

    def __repr__(self):
        return "CheckerResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

def run_testlib_checker(checker, input, output, answer):
    result_file = tempfile.NamedTemporaryFile()
    try:
        subprocess.run([checker, input, output, answer, result_file.name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        code = 0
    except subprocess.CalledProcessError as err:
        code = err.returncode
    
    if code == 0:
        return CheckerResult(success=True, score=1.)
    elif code == 1:
        return CheckerResult(success=False, message="Wrong Answer")
    elif code == 2:
        return CheckerResult(success=False, message="Presentation Error")
    elif code == 3:
        return CheckerResult(success=False, message="Judgement Failed")
    elif code == 4:
        return CheckerResult(success=False, message="_dirt")
    elif code == 5:
        return CheckerResult(success=False, message="_points")
    elif code == 8:
        return CheckerResult(success=False, message="Unexpcted EOF")
    elif code >= 16 and code <= 116:
        return CheckerResult(success=True, score=(code - 16.) / 100)

