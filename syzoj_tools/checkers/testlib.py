import os
from . import run_testlib_checker

class TestlibChecker:
    def __init__(self, problem, config):
        self.config = config
        self.problem = problem
        if "checker" not in self.config:
            raise ProblemException("checker field not found in checker")
        self.checker_source = self.config["checker"]
        if not os.path.isfile(os.path.join(self.problem.path, self.checker_source)):
            raise ProblemException("Checker file not found: %s", self.checker_source)
        (self.checker_executable, ext) = os.path.splitext(self.checker_source)
        if not ext in [".c", ".cpp"]:
            raise ProblemException("Unsupported checker extension %s" % ext)

    def compile(self):
        (self.checker_executable, ext) = os.path.splitext(self.checker_source)
        if ext == ".c":
            try:
                subprocess.run(["gcc", os.path.join(self.problem.path, self.checker_source), "-o", os.path.join(self.problem.path, self.checker_executable), "-O2"], check=True)
            except subprocess.CalledProcessError as e:
                raise ProblemException("checker compilation failed") from e
        elif ext == ".cpp":
            try:
                subprocess.run(["g++", os.path.join(self.problem.path, self.checker_source), "-o", os.path.join(self.problem.path, self.checker_executable), "-O2"], check=True)
            except subprocess.CalledProcessError as e:
                raise ProblemException("checker compilation failed") from e

    def check(self, case, outfile):
        if not os.path.isfile(os.path.join(self.problem.path, self.checker_executable)):
            self.compile()

        return run_testlib_checker(os.path.join(self.problem.path, self.checker_executable), case.input_data, outfile, case.answer_data)
