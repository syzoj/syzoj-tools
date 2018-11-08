import subprocess
import os
import tempfile
import logging
from ..languages import all_languages
from ..checkers.builtin import BuiltinChecker
from ..checkers.testlib import TestlibChecker
from ..checkers.loj import LojChecker
from ..validators.builtin import BuiltinValidator
from ..validators.testlib import TestlibValidator
logger = logging.getLogger("problem-traditional")

class ProblemTraditional:
    all_checkers = {
        "builtin": BuiltinChecker,
        "testlib": TestlibChecker,
        "loj": LojChecker
    }
    all_validators = {
        "builtin": BuiltinValidator,
        "testlib": TestlibValidator
    }

    def __init__(self, problem):
        self.problem = problem
        self.path = self.problem.path
        self.languages = {}
        if not "languages" in self.problem.config:
            for ext, lang in all_languages.items():
                self.languages[ext] = lang(self, {})
        else:
            for ext, config in self.problem.config["languages"].items():
                if not ext in all_languages:
                    raise ProblemException("Unsupported language {ext}".format(ext=ext))
                self.languages[ext] = all_languages[ext](self, config)

        checker_config = self.problem.config.get("checker", {
            "type": "builtin",
            "name": "wcmp"
        })
        checker_type = ProblemTraditional.all_checkers[checker_config["type"]]
        self.checker = checker_type(self, checker_config)

        validator_config = self.problem.config.get("validator")
        if validator_config:
            validator_type = ProblemTraditional.all_validators[validator_config["type"]]
            self.validator = validator_type(self, validator_config)
        else:
            self.validator = None

    def test(self):
        success = True
        if self.validator:
            for case in self.problem.cases:
                logger.info("Running validator for case %s" % case.name)
                validator_result = self.validator.check(case)
                if not validator_result.success:
                    logger.info("Case %s: input validation failed" % case.name)
                    success = False
                else:
                    logger.info("Case %s: input validation success" % case.name)
        return success

    def judge_session(self, source):
        return ProblemTraditionalJudgeSession(self, source)

class ProblemTraditionalJudgeSession:
    def __init__(self, parent, source):
        self.parent = parent
        self.source = source

    def pre_judge(self):
        ext = os.path.splitext(self.source)[1]
        if not ext in self.parent.languages:
            return "Undefined language %s" % ext
        language = self.parent.languages[ext]
        self.session = language.judge_session(self.source)
        return self.session.pre_judge()

    def do_judge(self, case):
        logger.verbose("Running testcase %s" % case.name)
        try:
            run_result = self.session.run_judge(case)
            if not run_result.success:
                logger.verbose("Test case %s failed: %s" % (case.name, run_result))
                return TestcaseResult(success=False, score=0., run_result=run_result)
            else:
                checker_result = self.parent.checker.check(case, run_result.outfile)
                if not checker_result.success:
                    logger.verbose("Test case %s didn't pass check: %s" % (case.name, checker_result))
                    return TestcaseResult(success=False, score=0., run_result=run_result, checker_result=checker_result)
                else:
                    logger.verbose("Test case %s succeeded: %s" % (case.name, checker_result))
                    return TestcaseResult(success=True, score=checker_result.score, run_result=run_result, checker_result=checker_result)
        finally:
            self.session.cleanup_judge()

    def post_judge(self):
        self.session.post_judge()

class TestcaseResult:
    def __init__(self, success=False, score=0, message=None, **kv):
        self.success = success
        self.score = score
        self.message = message
        self.__dict__.update(kv)

    def __repr__(self):
        return "TestcaseResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))
