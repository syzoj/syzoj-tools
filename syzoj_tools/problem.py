import yaml
import os

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
        if not os.path.isfile(config_file):
            raise ProblemException("File {file} doesn't exist, run `syzoj config` first".format(file=config_file))

        with open(config_file, 'r') as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError:
                raise

        self.cases = []
        cases_global = self.config.get("cases-global", {})
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
    
    def judge(self, source):
        session = self.type.judge_session(source)
        pre_judge_result = session.pre_judge()
        if pre_judge_result != None:
            return (False, pre_judge_result)

        cases_result = {}
        score_sum = 0.
        for i, subtask in enumerate(self.subtasks):
            print("Judging subtask %d" % i)
            score = 1.

            for j in subtask.testcases:
                if j in cases_result:
                    print("Skipping testcase %s because it is already judged" % j)
                else:
                    case = self.cases[self.case_by_name[j]]
                    cases_result[j] = session.do_judge(case)

                (success, case_score) = cases_result[j]
                if success:
                    score = min(score, case_score)
                    continue
                else:
                    score = 0.
                    break

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
