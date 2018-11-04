import subprocess
import tempfile

def run_testlib_checker(checker, input, output, answer):
    result_file = tempfile.NamedTemporaryFile()
    try:
        subprocess.run([checker, input, output, answer, result_file.name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        code = 0
    except subprocess.CalledProcessError as err:
        code = err.returncode
    
    if code == 0:
        return (True, 1.)
    elif code == 1:
        return (False, "Wrong Answer")
    elif code == 2:
        return (False, "Presentation Error")
    elif code == 3:
        return (False, "Judgement Failed")
    elif code == 4:
        return (False, "_dirt")
    elif code == 5:
        return (False, "_points")
    elif code == 8:
        return (False, "Unexpcted EOF")
    elif code >= 16 and code <= 116:
        return (True, (code - 16.) / 100)

