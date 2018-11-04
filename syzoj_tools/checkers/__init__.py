import subprocess
import tempfile

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

