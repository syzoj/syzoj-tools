import os
import subprocess
import tempfile
from ..problem import ProblemException
from . import CheckerResult

class LemonChecker:
    def __init__(self, problem, config):
        self.config = config
        self.problem = problem
        if "checker" not in self.config:
            raise ProblemException("checker field not found in checker")
        self.checker_source = os.path.join(self.problem.path, self.config["checker"])
        if not os.path.isfile(self.checker_source):
            raise ProblemException("Checker file not found: %s", self.checker_source)
        (self.checker_executable, ext) = os.path.splitext(self.checker_source)
        self.language = get_language(ext)
        if self.language == None:
            raise ProblemException("Unsupported checker extension %s" % ext)
        self.score = self.config.get("score", 100)

    def compile(self):
        self.language.compile(self.checker_source, self.checker_executable)

    def check(self, case, outfile):
        if not os.path.isfile(self.checker_executable) or os.path.getmtime(self.checker_executable) < os.path.getmtime(self.checker_source):
            self.compile()

        try:
            self.workdir = tempfile.mkdtemp()
            with open(os.path.join(self.workdir, "full_score"), "w") as f_score:
                f_score.write(str(self.score))
            process = subprocess.run([
                os.path.abspath(self.checker_executable),
                os.path.abspath(case.input_data),
                os.path.abspath(outfile),
                os.path.abspath(case.answer_data),
                os.path.join(self.workdir, "full_score"),
                os.path.join(self.workdir, "score"),
                os.path.join(self.workdir, "report")
            ], cwd=self.workdir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            with open(os.path.join(self.workdir, "score"), "r") as f_score:
                if self.score == 0:
                    score = 0
                else:
                    score = float(f_score.read()) / self.score
            try:
                with open(os.path.join(self.workdir, "report"), "r") as f_report:
                    report = f_report.read()
            except FileNotFoundError:
                report = None

            shutil.rmtree(self.workdir)
            return CheckerResult(True, score=score, message=report)
        except (FileNotFoundError, subprocess.CalledProcessError, ValueError) as e:
            return CheckerResult(False, message="Judgement failed", error=e)

