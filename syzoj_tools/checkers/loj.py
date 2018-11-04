import os
import subprocess
import tempfile
import shutil
from . import CheckerResult

class LojChecker:
    def __init__(self, problem, config):
        self.config = config
        self.problem = problem
        if "checker" not in self.config:
            raise ProblemException("checker field not found in checker")
        self.checker_source = os.path.join(self.problem.path, self.config["checker"])
        if not os.path.isfile(self.checker_source):
            raise ProblemException("Checker file not found: %s", self.checker_source)
        (self.checker_executable, ext) = os.path.splitext(os.path.join(self.problem.path, self.checker_source))
        if not ext in [".c", ".cpp"]:
            raise ProblemException("Unsupported checker extension %s" % ext)

    def compile(self):
        (self.checker_executable, ext) = os.path.splitext(self.checker_source)
        if ext == ".c":
            try:
                subprocess.run(["gcc", self.checker_source, "-o", self.checker_executable, "-O2"], check=True)
            except subprocess.CalledProcessError as e:
                raise ProblemException("checker compilation failed") from e
        elif ext == ".cpp":
            try:
                subprocess.run(["g++", self.checker_source, "-o", self.checker_executable, "-O2"], check=True)
            except subprocess.CalledProcessError as e:
                raise ProblemException("checker compilation failed") from e
        else:
            raise ProblemException("Checker extension %s not supported" % ext)

    def check(self, case, outfile):
        if not os.path.isfile(self.checker_executable) or os.path.getmtime(self.checker_executable) < os.path.getmtime(self.checker_source):
            self.compile()

        try:
            self.workdir = tempfile.mkdtemp()
            shutil.copy(case.input_data, os.path.join(self.workdir, "input"))
            shutil.copy(outfile, os.path.join(self.workdir, "user_out"))
            shutil.copy(case.answer_data, os.path.join(self.workdir, "answer"))
            process = subprocess.run([os.path.abspath(self.checker_executable)], cwd=self.workdir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            shutil.rmtree(self.workdir)
            return CheckerResult(True, score=float(process.stdout) / 100.)
        except subprocess.CalledProcessError:
            return CheckerResult(False, message="Judgement failed")

