import subprocess
import tempfile
import logging
logger = logging.getLogger("testlib-validator")

all_validators = None

def load_validators():
    global all_validators
    if all_validators == None:
        from .builtin import BuiltinValidator
        from .testlib import TestlibValidator
        all_validators = {
            "builtin": BuiltinValidator,
            "testlib": TestlibValidator
        }

def get_all_validators():
    global all_validators
    load_validators()
    return all_validators

def get_validator(name):
    global all_validators
    load_validators()
    return all_validators.get(name)

class ValidatorResult:
    def __init__(self, success, message=None, testOverviewLog=None):
        self.success = success
        self.message = message
        self.testOverviewLog = testOverviewLog

    def __repr__(self):
        return "ValidatorResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

def run_testlib_validator(checker, input, testset=None, group=None):
    logger.verbose("Running validator %s" % checker)
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
        logger.verbose("Validator result: success")
        return ValidatorResult(True, result.stderr, testOverviewLogFile.read())
    except subprocess.CalledProcessError as err:
        logger.verbose("Validator result: fail")
        return ValidatorResult(False, err.stderr, testOverviewLogFile.read())
    
