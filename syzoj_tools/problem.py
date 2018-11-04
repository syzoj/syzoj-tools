import yaml
import os
from collections import namedtuple

from .types.traditional import ProblemTraditional

class ProblemException(BaseException):
    pass


class Problem:
    all_types = {
        "traditional": ProblemTraditional
    }

    def __init__(self, path=".", config=None):
        self.path = path
        config_file = os.path.join(self.path, "problem.yml")
        try:
            with open(config_file, 'r') as stream:
                try:
                    self.config = yaml.load(stream)
                except yaml.YAMLError:
                    raise
        except FileNotFoundError as e:
            raise ProblemException("File {file} doesn't exist, run `syzoj config` first".format(file=config_file)) from e

        self.cases = []
        cases = self.config["cases"]
        cases_global = self.config.get("cases-global", {})
        if isinstance(cases, int):
            self.cases = [ProblemCase(self, i, cases_global.copy()) for i in range(cases)]
        else:
            for index, config in enumerate(self.config["cases"]):
                merged_config = cases_global.copy()
                merged_config.update(config)
                self.cases.append(ProblemCase(self, index, merged_config))

        self.case_by_name = {}
        for index, case in enumerate(self.cases):
            self.case_by_name[case.name] = index

        self.subtasks = []
        if not "subtasks" in self.config:
            subtask_count = len(self.cases)
            subtask_score = 100. / subtask_count
            for index, case in enumerate(self.cases):
                config = {
                    "score": subtask_score,
                    "testcases": [case.name]
                }
                subtask = ProblemSubtask(self, index, config)
                self.subtasks.append(subtask)
        else:
            for index, config in enumerate(self.config["subtasks"]):
                subtask = ProblemSubtask(self, index, config)
                for case in subtask.testcases:
                    if not case in self.case_by_name:
                        raise ProblemException("Subtask %d: Test case with name %s does not exist" % (index, case))
                self.subtasks.append(subtask)

        type_id = self.config.get("type", "traditional")
        if not type_id in Problem.all_types:
            raise ProblemException("Unsupported problem type %s" % type_id)
        self.type = Problem.all_types[type_id](self)

    
    def build(self):
        print("Not Implemented")
    
    def test(self):
        print("test")
    
    def judge(self, source, lazy=True):
        session = self.type.judge_session(source)
        pre_judge_result = session.pre_judge()
        if pre_judge_result != None:
            return JudgeResult(success=False, score=0, message=pre_judge_result)

        case_result = {}
        subtask_result = []
        score_sum = 0.
        if not lazy:
            for case in self.cases:
                case_result[case.name] = session.do_judge(case)

        for i, subtask in enumerate(self.subtasks):
            print("Judging subtask %d" % i)
            score = 1.
            last_case = None

            for j in subtask.testcases:
                if j in case_result:
                    if lazy:
                        print("Skipping testcase %s because it is already judged" % j)
                else:
                    case = self.cases[self.case_by_name[j]]
                    case_result[j] = session.do_judge(case)

                result = case_result[j]
                if result.success:
                    score = min(score, result.score)
                    continue
                else:
                    score = 0.
                    last_case = j
                    break

            print("Subtask %d result: %s" % (i, score))
            subtask_result.append(SubtaskResult(score, last_case))
            score_sum += score * subtask.score

        session.post_judge()
        return JudgeResult(success=True, case_result=case_result, subtask_result=subtask_result, score=score_sum)
    
    def deploy(self):
        print("deploy")

class ProblemCase:
    def __init__(self, problem, index, config):
        self.config = config
        self.index = index
        self.problem = problem

        self.name = self.config.get("name", str(self.index + 1))
        self.input_data = os.path.join(self.problem.path, self.config.get("input-data", "data/{name}.in").format(name=self.name))
        self.answer_data = os.path.join(self.problem.path, self.config.get("answer-data", "data/{name}.out").format(name=self.name))
        
        self.time_limit = ProblemCase.parse_time_limit(self.config["time-limit"])
        self.memory_limit = ProblemCase.parse_memory_limit(self.config["memory-limit"])

    def parse_time_limit(val):
        if val.endswith("ms"):
            return float(val[:-2])
        elif val.endswith("us"):
            return float(val[:-2]) / 100
        elif val.endswith("s"):
            return float(val[:-1]) * 1000
        else:
            raise ProblemException("Invalid time limit: %s" % val)
    
    def parse_memory_limit(val):
        if val.endswith("KB"):
            return float(val[:-2])
        elif val.endswith("MB"):
            return float(val[:-2]) * 1024
        elif val.endswith("GB"):
            return float(val[:-2]) * 1048576

class ProblemSubtask:
    def __init__(self, problem, index, config):
        self.config = config
        self.index = index
        self.problem = problem

        self.name = str(self.config.get("name", self.index + 1))
        self.testcases = list(map(str, self.config["testcases"]))
        self.score = self.config["score"]

class JudgeResult:
    def __init__(self, success=False, score=0, case_result=None, subtask_result=None, message=None):
        self.success = success
        self.score = score
        self.case_result = case_result
        self.subtask_result = subtask_result
        self.message = message
        
    def __repr__(self):
        return "JudgeResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

class SubtaskResult:
    def __init__(self, score, last_case):
        self.score = score
        self.last_case = last_case
        
    def __repr__(self):
        return "SubtaskResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))
