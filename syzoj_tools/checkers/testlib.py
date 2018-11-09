import os
import subprocess
from ..problem import ProblemException
from ..languages import get_language
from . import run_testlib_checker

class TestlibChecker:
    def __init__(self, problem, config):
        self.config = config
        self.problem = problem
        if "checker" not in self.config:
            raise ProblemException("checker field not found in checker")
        self.checker_source = os.path.join(self.problem.path, self.config["checker"])
        if not os.path.isfile(self.checker_source):
            raise ProblemException("Checker file not found: %s", self.checker_source)
        (self.checker_executable, ext) = os.path.splitext(self.checker_source)
        language_class = get_language(ext)
        if language_class == None:
            raise ProblemException("Unsupported checker extension %s" % ext)
        self.language = language_class(problem=self.problem)

    def compile(self):
        self.language.compile(self.checker_source, self.checker_executable)

    def check(self, case, outfile):
        if not os.path.isfile(self.checker_executable) or os.path.getmtime(self.checker_executable) < os.path.getmtime(self.checker_source):
            self.compile()

        return run_testlib_checker(self.checker_executable, case.input_data, outfile, case.answer_data)
