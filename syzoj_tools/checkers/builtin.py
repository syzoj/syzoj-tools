import os
import subprocess
from ..problem import ProblemException
from . import run_testlib_checker

class BuiltinChecker:
    builtin_checkers = ["acmp", "caseicmp", "casencmp", "casewcmp", "dcmp", "fcmp", "hcmp", "icmp", "lcmp", "ncmp", "pointscmp", "rcmp", "rcmp4", "rcmp6", "rcmp9", "rncmp", "uncmp", "wcmp", "yesno"]

    def __init__(self, problem, config):
        self.config = config
        self.problem = problem
        if not self.config["name"] in BuiltinChecker.builtin_checkers:
            raise ProblemException("Unknown builtin checker: %s" % self.config["name"])
        self.name = self.config["name"]

    def check(self, case, outfile):
        cpp_file = os.path.join(os.path.dirname(__file__), "%s.cpp" % self.name)
        checker_file = os.path.join(os.path.dirname(__file__), "%s" % self.name)
        if not os.path.exists(checker_file):
            print("Builtin checker %s not found, compiling" % self.name)
            subprocess.run(["g++", cpp_file, "-o", checker_file, "-O2"], check=True)
        return run_testlib_checker(checker_file, case.input_data, outfile, case.answer_data)
