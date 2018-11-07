import os
import subprocess
from .. import problem as m_problem
from . import run_testlib_validator

class TestlibValidator:
    def __init__(self, problem, config):
        self.config = config
        self.problem = problem
        if "validator" not in self.config:
            raise m_problem.ProblemException("validator field not found in validator")
        self.validator_source = os.path.join(self.problem.path, self.config["validator"])
        if not os.path.isfile(self.validator_source):
            raise m_problem.ProblemException("Validator file not found: %s", self.validator_source)
        (self.validator_executable, ext) = os.path.splitext(self.validator_source)
        if not ext in [".c", ".cpp"]:
            raise m_problem.ProblemException("Unsupported validator extension %s" % ext)

    def compile(self):
        (_, ext) = os.path.splitext(self.validator_source)
        if ext == ".c":
            try:
                subprocess.run(["gcc", self.validator_source, "-o", self.validator_executable, "-O2"], check=True)
            except subprocess.CalledProcessError as e:
                raise m_problem.ProblemException("validator compilation failed") from e
        elif ext == ".cpp":
            try:
                subprocess.run(["g++", self.validator_source, "-o", self.validator_executable, "-O2"], check=True)
            except subprocess.CalledProcessError as e:
                raise m_problem.ProblemException("validator compilation failed") from e

    def check(self, case):
        if not os.path.isfile(self.validator_executable) or os.path.getmtime(self.validator_executable) < os.path.getmtime(self.validator_source):
            self.compile()

        return run_testlib_validator(self.validator_executable, case.input_data)
