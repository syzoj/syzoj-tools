import os
import subprocess
import tempfile
import shutil

class LojChecker:
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

        try:
            self.workdir = tempfile.mkdtemp()
            shutil.copy(case.input_data, os.path.join(self.workdir, "input"))
            shutil.copy(outfile, os.path.join(self.workdir, "user_out"))
            shutil.copy(case.answer_data, os.path.join(self.workdir, "answer"))
            process = subprocess.run([os.path.abspath(os.path.join(self.problem.path, self.checker_executable))], cwd=self.workdir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            shutil.rmtree(self.workdir)
            return (True, int(process.stdout))
        except subprocess.CalledProcessError:
            return (False, "Judgement failed")

