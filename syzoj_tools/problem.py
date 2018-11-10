import os
import subprocess
import logging
from collections import namedtuple
from ruamel.yaml import YAML

from .languages import get_language
from .types import get_type

logger = logging.getLogger("problem")

class ProblemException(BaseException):
    pass


class Problem:
    def __init__(self, path=".", config=None):
        self.path = path
        self.yaml = YAML()
        config_file = os.path.join(self.path, "problem.yml")
        try:
            with open(config_file, 'r') as stream:
                try:
                    self.config = self.yaml.load(stream)
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

        self.assertions = []
        if "assertions" in self.config:
            for i, assertion_config in enumerate(self.config["assertions"]):
                assertion = ProblemAssertion(self, assertion_config)
                self.assertions.append(assertion)
                for case in assertion.testcases:
                    if not case in self.case_by_name:
                        raise ProblemException("Assertion %d: case %s doesn't exist" % (i, case))

        type_id = self.config.get("type", "traditional")
        type_class = get_type(type_id)
        if type_class == None:
            raise ProblemException("Unsupported problem type %s" % type_id)
        self.type = type_class(self)

    
    def build(self, *args, **kvargs):
        self.type.build(*args, **kvargs)
    
    def test(self):
        success = True
        for i, assertion in enumerate(self.assertions):
            logger.info("Running assertion %d" % i)
            result = self.judge(assertion.prog, lazy=False)
            if not result.success:
                logger.warning("Assertion %d failed: compile failed" % i)
                success = False
                continue

            if assertion.score and assertion.score != result.score:
                logger.warning("Assertion %d failed: score mismatch" % i)
                success = False

            for subtask in assertion.subtasks:
                subtask_result = result.subtask_result[subtask["id"]]
                if "passed" in subtask:
                    passed = subtask_result.last_case == None
                    if passed != subtask["passed"]:
                        logger.warning("Assertion %d failed: subtask %d: passed mismatch" % (i, subtask["id"]))
                        success = False
                if "score" in subtask:
                    real_score = subtask_result.score * self.subtasks[subtask["id"]].score
                    if real_score != subtask["score"]:
                        logger.warning("Assertion %d failed: subtask %d: score mismatch, expected %f, got %f" % (i, subtask["id"], subtask["score"], real_score))
                        success = False
                if "last-message" in subtask:
                    last_case = result.subtask_result[subtask["id"]].last_case
                    if last_case == None:
                        logger.warning("Assertion %d failed: subtask %d: passed but last-message is specified" % (i, subtask["id"]))
                        success = False
                    else:
                        message = result.case_result[last_case].run_result.message
                        if message != subtask["last-message"]:
                            logger.warning("Assertion %d failed: subtask %d: last-message mismatch: expected %s, got %s" % (i, subtask["id"], subtask["last-message"], result.case_result[last_case].message))
                            success = False

            for case in assertion.testcases:
                result = result.case_result[case["name"]]
                if "score" in case:
                    if result.score != case.score:
                        logger.warning("Assertion %d failed: case %s: score mismatch, expected %f, got %f" % (i, case.name, result.score, case.score))
                        success = False

        if not self.type.test():
            success = False
        return success

    def judge(self, source, lazy=True):
        session = self.type.judge_session(source)
        pre_judge_result = session.pre_judge()
        if not pre_judge_result.success:
            return JudgeResult(success=False, score=0, pre_judge_result=pre_judge_result)

        case_result = {}
        subtask_result = []
        score_sum = 0.
        if not lazy:
            for case in self.cases:
                case_result[case.name] = session.do_judge(case)

        for i, subtask in enumerate(self.subtasks):
            logger.verbose("Judging subtask %d" % i)
            score = 1.
            last_case = None

            for j in subtask.testcases:
                if j in case_result:
                    if lazy:
                        logger.verbose("Skipping testcase %s because it is already judged" % j)
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

            logger.verbose("Subtask %d result: %s" % (i, score))
            subtask_result.append(SubtaskResult(score, last_case))
            score_sum += score * subtask.score

        session.post_judge()
        return JudgeResult(success=True, pre_judge_result=pre_judge_result, case_result=case_result, subtask_result=subtask_result, score=score_sum)

class ProblemCase:
    def __init__(self, problem, index, config):
        self.config = config
        self.index = index
        self.problem = problem

        self.name = self.config.get("name", str(self.index + 1))

class ProblemSubtask:
    def __init__(self, problem, index, config):
        self.config = config
        self.index = index
        self.problem = problem

        self.name = str(self.config.get("name", self.index + 1))
        self.testcases = list(map(str, self.config["testcases"]))
        self.score = self.config["score"]

class PreJudgeResult:
    def __init__(self, success, message=None):
        self.success = success
        self.message = message
        
    def __repr__(self):
        return "PreJudgeResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

class JudgeResult:
    def __init__(self, success, score, case_result=None, subtask_result=None, pre_judge_result=None):
        self.success = success
        self.score = score
        self.case_result = case_result
        self.subtask_result = subtask_result
        self.pre_judge_result = pre_judge_result
        
    def __repr__(self):
        return "JudgeResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

class SubtaskResult:
    def __init__(self, score, last_case):
        self.score = score
        self.last_case = last_case
        
    def __repr__(self):
        return "SubtaskResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

class ProblemAssertion:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config
        self.prog = os.path.join(self.problem.path, self.config["prog"])
        self.score = self.config.get("score")
        self.subtasks = self.config.get("subtasks", [])
        self.testcases = self.config.get("testcases", [])

class TestcaseResult:
    def __init__(self, success=False, score=0, message=None, **kv):
        self.success = success
        self.score = score
        self.message = message
        self.__dict__.update(kv)

    def __repr__(self):
        return "TestcaseResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

