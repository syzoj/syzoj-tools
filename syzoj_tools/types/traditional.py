import subprocess
import os
import tempfile
from ..languages.compiled import ProblemCppLanguage, ProblemCLanguage, ProblemPasLanguage
from ..checkers.builtin import BuiltinChecker
from ..checkers.testlib import TestlibChecker
from ..checkers.loj import LojChecker

class ProblemTraditional:
    all_checkers = {
        "builtin": BuiltinChecker,
        "testlib": TestlibChecker,
        "loj": LojChecker
    }

    all_languages = {
        ".c": ProblemCLanguage,
        ".cpp": ProblemCppLanguage,
        ".pas": ProblemPasLanguage
    }

    def __init__(self, problem):
        self.problem = problem
        self.path = self.problem.path
        self.languages = {}
        if not "languages" in self.problem.config:
            for ext, lang in ProblemTraditional.all_languages.items():
                self.languages[ext] = lang(self, {})
        else:
            for ext, config in self.problem.config["languages"].items():
                if not ext in ProblemTraditional.all_languages:
                    raise ProblemException("Unsupported language {ext}".format(ext=ext))
                self.languages[ext] = ProblemTraditional.all_languages[ext](self, config)

        checker_config = self.problem.config.get("checker", {
            "type": "builtin",
            "name": "wcmp"
        })
        checker_type = ProblemTraditional.all_checkers[checker_config["type"]]
        self.checker = checker_type(self, checker_config)

    def judge_session(self, source):
        ext = os.path.splitext(source)[1]
        if not ext in self.languages:
            return (False, "Undefined language %s" % ext)
        language = self.languages[ext]
        return ProblemTraditionalJudgeSession(language.judge_session(source), self.checker)

class ProblemTraditionalJudgeSession:
    def __init__(self, session, checker):
        self.session = session
        self.checker = checker

    def pre_judge(self):
        self.session.pre_judge()

    def do_judge(self, case):
        print("  Running testcase %s" % case.name)
        try:
            (success, result) = self.session.run_judge(case)
            if not success:
                print("    Test case %s failed: %s" % (case.name, result))
                return (False, result)
            else:
                (success, checker_result) = self.checker.check(case, result)
                if not success:
                    print("    Test case %s didn't pass check: %s" % (case.name, checker_result))
                    return (False, result)
                else:
                    print("    Test case %s succeeded: %s" % (case.name, checker_result))
                    return (True, checker_result)
        finally:
            self.session.cleanup_judge()

    def post_judge(self):
        self.session.post_judge()
