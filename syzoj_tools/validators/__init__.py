import subprocess
import tempfile

class ValidatorResult:
    def __init__(self, success, message=None, testOverviewLog=None):
        self.success = success
        self.message = message
        self.testOverviewLog = testOverviewLog

    def __repr__(self):
        return "ValidatorResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

def run_testlib_validator(checker, input, testset=None, group=None):
    print("Running validator %s" % checker)
    testOverviewLogFile = tempfile.NamedTemporaryFile()
    args = [checker]
    if testset != None:
        args.append("--testset")
        args.append(testset)
    if group != None:
        args.append("--group")
        args.append(group)
    args.append("--testOverviewLogFileName")
    args.append(testOverviewLogFile.name)

    try:
        result = subprocess.run([checker], check=True, stdin=open(input, "rb"), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print("Success")
        return ValidatorResult(True, result.stderr, testOverviewLogFile.read())
    except subprocess.CalledProcessError as err:
        print("Fail")
        return ValidatorResult(False, err.stderr, testOverviewLogFile.read())
    