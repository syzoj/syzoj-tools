import yaml
import os
import tempfile
import subprocess

from .languages.cpp import ProblemCppLanguage
from .languages.c import ProblemCLanguage

class ProblemException(BaseException):
    pass

def run_testlib_checker(checker, input, output, answer):
    result_file = tempfile.NamedTemporaryFile()
    try:
        subprocess.run([checker, input, output, answer, result_file.name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        code = 0
    except subprocess.CalledProcessError as err:
        code = err.returncode
    
    if code == 0:
        return (True, 1.)
    elif code == 1:
        return (False, "Wrong Answer")
    elif code == 2:
        return (False, "Presentation Error")
    elif code == 3:
        return (False, "Judgement Failed")
    elif code == 4:
        return (False, "_dirt")
    elif code == 5:
        return (False, "_points")
    elif code == 8:
        return (False, "Unexpcted EOF")
    elif code >= 16 and code <= 116:
        return (True, (code - 16.) / 100)

class BuiltinChecker:
    builtin_checkers = ["acmp", "caseicmp", "casencmp", "casewcmp", "dcmp", "fcmp", "hcmp", "icmp", "lcmp", "ncmp", "pointscmp", "rcmp", "rcmp4", "rcmp6", "rcmp9", "rncmp", "uncmp", "wcmp", "yesno"]

    def __init__(self, problem, config):
        self.config = config
        self.problem = problem
        if not self.config["name"] in BuiltinChecker.builtin_checkers:
            raise ProblemException("Unknown builtin checker: %s" % self.config["name"])
        self.name = self.config["name"]

    def check(self, case, outfile):
        cpp_file = os.path.join(os.path.dirname(__file__), "../checkers/%s.cpp" % self.name)
        checker_file = os.path.join(os.path.dirname(__file__), "../checkers/%s" % self.name)
        if not os.path.exists(checker_file):
            print("Builtin checker %s not found, compiling" % self.name)
            subprocess.run(["g++", cpp_file, "-o", checker_file, "-O2"], check=True)

        return run_testlib_checker(checker_file, case.input_data, outfile, case.answer_data)

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

    def check(self, outfile):
        if not os.path.isfile(os.path.join(self.problem.path, self.checker_executable)):
            self.compile()

        return run_testlib_checker(self.checker_executable, case.input_data, outfile, case.answer_data)

class Problem:
    def __init__(self, path="."):
        self.path = path
        self.has_loaded = False
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    all_languages = {
        ".c": ProblemCLanguage,
        ".cpp": ProblemCppLanguage
    }

    all_checkers = {
        "builtin": BuiltinChecker,
        "testlib": TestlibChecker
    }
    
    def load(self):
        config_file = os.path.join(self.path, "problem.yml")
        if not os.path.isfile(config_file):
            raise ProblemException("File {file} doesn't exist, run `syzoj config` first".format(file=config_file))

        with open(config_file, 'r') as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError:
                raise
        
        self.cases = []
        for index, config in enumerate(self.config["cases"]):
            merged_config = self.config.get("cases-global", {}).copy()
            merged_config.update(config)
            self.cases.append(ProblemCase(self, index, merged_config))

        self.case_by_name = {}
        for index, case in enumerate(self.cases):
            self.case_by_name[case.name] = index

        self.subtasks = []
        for index, config in enumerate(self.config["subtasks"]):
            subtask = ProblemSubtask(self, index, config)
            for case in subtask.testcases:
                if not case in self.case_by_name:
                    raise ProblemException("Subtask %d: Test case with name %s does not exist" % (index, case))
            self.subtasks.append(subtask)

        self.languages = {}
        for ext, config in self.config["languages"].items():
            if not ext in Problem.all_languages:
                raise ProblemException("Unsupported language {ext}".format(ext=ext))
            self.languages[ext] = Problem.all_languages[ext](self, config)

        checker_type = Problem.all_checkers[self.config["checker"]["type"]]
        self.checker = checker_type(self, self.config["checker"])

        self.has_loaded = True

    def close(self):
        pass
    
    def build(self):
        if not self.has_loaded:
            raise ProblemException("Cannot build before problem is loaded")
            exit(1)
        print("Not Implemented")
    
    def test(self):
        print("test")
    
    def judge(self, source):
        ext = os.path.splitext(source)[1]
        if not ext in self.languages:
            return (False, "Undefined language %s" % ext)
        language = self.languages[ext]

        session = language.judge_session(source)
        pre_judge_result = session.pre_judge()
        if pre_judge_result != None:
            return pre_judge_result

        cases_result = {}
        score_sum = 0.
        for i, subtask in enumerate(self.subtasks):
            print("Judging subtask %d" % i)
            score = 1.

            for j in subtask.testcases:
                if j in cases_result:
                    print("Skipping testcase %s because it is already judged" % j)
                    (success, case_score) = cases_result[j]
                    if success:
                        score = min(score, case_score)
                        continue
                    else:
                        score = 0.
                        break

                case = self.cases[self.case_by_name[j]]
                print("  Running testcase %s" % case.name)
                try:
                    (success, result) = session.run_judge(case)
                    if not success:
                        print("    Test case %s failed: %s" % (case.name, result))
                        cases_result[j] = (False, result)
                        score = 0.
                        break
                    else:
                        (success, checker_result) = self.checker.check(case, result)
                        if not success:
                            print("    Test case %s failed: %s" % (case.name, checker_result))
                            cases_result[j] = (False, result)
                            score = 0
                            break
                        else:
                            print("    Test case %s succeeded: %s" % (case.name, checker_result))
                            cases_result[j] = (True, checker_result)
                            score = min(score, checker_result)
                            continue
                finally:
                    session.cleanup_judge()

            print("Subtask %d result: %s" % (i, score))
            score_sum += score * subtask.score

        session.post_judge()
        return (True, score_sum)
    
    def deploy(self):
        print("deploy")

class ProblemCase:
    def __init__(self, problem, index, config):
        self.config = config
        self.index = index
        self.problem = problem

        self.name = self.config.get("name", str(self.index + 1))
        self.input_data = os.path.join(self.problem.path, self.config.get("input-data", "data/%s.in" % self.name))
        self.answer_data = os.path.join(self.problem.path, self.config.get("answer-data", "data/%s.out" % self.name))

class ProblemSubtask:
    def __init__(self, problem, index, config):
        self.config = config
        self.index = index
        self.problem = problem

        self.name = str(self.config.get("name", self.index + 1))
        self.testcases = list(map(str, self.config["testcases"]))
        self.score = self.config.get("score", 100)

