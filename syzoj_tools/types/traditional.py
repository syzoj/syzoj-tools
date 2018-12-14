import subprocess
import os
import tempfile
import logging
from ..languages import get_all_languages, get_language, guess_language
from ..checkers import get_checker
from ..validators import get_validator
from ..problem import PreJudgeResult, ProblemException, TestcaseResult
logger = logging.getLogger("problem-traditional")

class ProblemTraditional:
    def __init__(self, problem):
        self.problem = problem
        self.path = self.problem.path
        self.languages = {}
        if not "languages" in self.problem.config:
            all_languages = get_all_languages()
            for typ, lang in all_languages.items():
                self.languages[typ] = lang(self, {})
        else:
            for typ, config in self.problem.config["languages"].items():
                language_class = get_language(typ)
                if language_class == None:
                    raise ProblemException("Unsupported language type {typ}".format(typ=typ))
                self.languages[typ] = language_class(self, config)

        checker_config = self.problem.config.get("checker", {
            "type": "default"
        })
        checker_type = get_checker(checker_config["type"])
        if checker_type == None:
            raise ProblemException("Unsupported checker type: %s" % checker_config["type"])
        self.checker = checker_type(self, checker_config)

        validator_config = self.problem.config.get("validator")
        if validator_config:
            validator_type = get_validator(validator_config["type"])
            if validator_type == None:
                raise ProblemException("Unsupported validator type: %s" % validator_config["type"])
            self.validator = validator_type(self, validator_config)
        else:
            self.validator = None

        self.build_config = ProblemBuild(self, self.problem.config.get("build", {}))
        has_gen_input = False
        has_gen_answer = False
        for case in self.problem.cases:
            self.parse_case(case)
            if case.gen_input:
                has_gen_input = True
                if self.build_config.input_gen == None:
                    raise ProblemException("Case %s requires input generation but input generator is not defined" % case.name)
            if case.gen_answer:
                has_gen_answer = True
                if self.build_config.answer_gen == None:
                    raise ProblemException("Case %s requires answer generation but answer generator is not defined" % case.name)
        if not has_gen_input and self.build_config.input_gen != None:
            logger.warning("Input generator configured but no test case use it; try adding gen-input: true")
        if not has_gen_answer and self.build_config.answer_gen != None:
            logger.warning("Answer generator configured but no test case use it; try adding gen-answer: true")

    def parse_case(self, case):
        case.input_data = os.path.join(case.problem.path, case.config.get("input-data", "data/{name}.in").format(name=case.name))
        case.answer_data = os.path.join(case.problem.path, case.config.get("answer-data", "data/{name}.out").format(name=case.name))
        case.gen = case.config.get("gen", False)
        case.gen_input = case.config.get("gen-input", case.gen)
        case.gen_answer = case.config.get("gen-answer", case.gen)
        if case.gen_input:
            case.build_args = list(map(lambda s: s.format(name=case.name), case.config.get("args", ["{name}"])))
        
        case.time_limit = ProblemTraditional.parse_time_limit(case.config["time-limit"])
        case.memory_limit = ProblemTraditional.parse_memory_limit(case.config["memory-limit"])

        if not case.gen_input and not os.path.isfile(case.input_data):
            raise ProblemException("Input file %s for testcase %s doesn't exist" % (case.input_data, case.name))
        if not case.gen_answer and not os.path.isfile(case.answer_data):
            raise ProblemException("Answer file %s for testcase %s doesn't exist" % (case.answer_data, case.name))


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

    def build(self, force=True):
        if self.build_config.input_gen != None:
            input_gen_path, _ = os.path.splitext(self.build_config.input_gen)
            lang = self.build_config.input_gen_lang(self)
            if not os.path.isfile(input_gen_path) or os.path.getmtime(input_gen_path) < os.path.getmtime(self.build_config.input_gen):
                logger.info("Input generator executable not found, compiling")
                lang.compile(self.build_config.input_gen, input_gen_path)
                force = True

        if self.build_config.answer_gen != None:
            answer_gen_path, _ = os.path.splitext(self.build_config.answer_gen)
            lang = self.build_config.answer_gen_lang(self)
            if not os.path.isfile(answer_gen_path) or os.path.getmtime(input_gen_path) < os.path.getmtime(self.build_config.answer_gen):
                logger.info("Answer generator executable not found, compiling")
                lang.compile(self.build_config.answer_gen, answer_gen_path)
                force = True

        for case in self.problem.cases:
            if case.gen_input and (force or not os.path.isfile(case.input_data)):
                logger.info("Generating input for case %s" % case.name)
                args = lang.get_args(input_gen_path, *case.build_args)
                with open(case.input_data, "wb") as input_file:
                    subprocess.run(args, stdin=subprocess.DEVNULL, stdout=input_file, check=True)

            if case.gen_answer and (force or not os.path.isfile(case.answer_data)):
                logger.info("Generating answer for case %s" % case.name)
                args = lang.get_args(answer_gen_path)
                with open(case.input_data, "rb") as input_file:
                    with open(case.answer_data, "wb") as answer_file:
                        subprocess.run(args, stdin=input_file, stdout=answer_file, check=True)

    def test(self):
        success = True
        if self.validator:
            for case in self.problem.cases:
                logger.info("Running validator for case %s" % case.name)
                validator_result = self.validator.check(case)
                if not validator_result.success:
                    logger.info("Case %s: input validation failed" % case.name)
                    success = False
                else:
                    logger.info("Case %s: input validation success" % case.name)
        return success

    def judge_session(self, source, language=None):
        if os.name != "posix":
            logger.warning("Cannot judge problems on platforms other than posix; skipping")
            return NullJudgeSession()
        return ProblemTraditionalJudgeSession(self, source, language=language)

class NullJudgeSession:
    def pre_judge(self):
        return PreJudgeResult(false, "Unsupported platform")

class ProblemTraditionalJudgeSession:
    def __init__(self, parent, source, language=None):
        self.parent = parent
        self.source = source
        self.language = language or guess_language(os.path.splitext(self.source)[1])
        if self.language == None:
            return PreJudgeResult(False, "Cannot determine language for extension %s" % typ)
        if not self.language in self.parent.languages:
            return PreJudgeResult(False, "Undefined language %s" % self.language)

    def pre_judge(self):
        language = self.parent.languages[self.language]
        self.session = language.judge_session(self.source)
        return self.session.pre_judge()

    def do_judge(self, case):
        logger.verbose("Running testcase %s" % case.name)
        try:
            run_result = self.session.run_judge(case)
            if not run_result.success:
                logger.verbose("Test case %s failed: %s" % (case.name, run_result))
                return TestcaseResult(success=False, score=0., run_result=run_result, message=run_result.message)
            else:
                checker_result = self.parent.checker.check(case, run_result.outfile)
                if not checker_result.success:
                    logger.verbose("Test case %s didn't pass check: %s" % (case.name, checker_result))
                    return TestcaseResult(success=False, score=0., run_result=run_result, checker_result=checker_result, message=checker_result.message)
                else:
                    logger.verbose("Test case %s succeeded: %s" % (case.name, checker_result))
                    return TestcaseResult(success=True, score=checker_result.score, run_result=run_result, checker_result=checker_result, message=checker_result.message)
        finally:
            self.session.cleanup_judge()

    def post_judge(self):
        self.session.post_judge()

class ProblemBuild:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config
        if "input-gen" in self.config:
            self.input_gen = os.path.join(self.problem.path, self.config["input-gen"])
            typ = guess_language(os.path.splitext(self.input_gen)[1])
            if typ == None:
                raise ProblemException("Invalid input gen: unsupported language extension")
            self.input_gen_lang = get_language(typ)
            if self.input_gen_lang == None:
                raise ProblemException("Invalid input gen: unsupported language")
        else:
            self.input_gen = None

        if "answer-gen" in self.config:
            self.answer_gen = os.path.join(self.problem.path, self.config["answer-gen"])
            typ = guess_language(os.path.splitext(self.answer_gen)[1])
            if typ == None:
                raise ProblemException("Invalid answer gen: unsupported language extension")
            self.answer_gen_lang = get_language(typ)
            if self.answer_gen_lang == None:
                raise ProblemException("Invalid answer gen: unsupported language")
        else:
            self.answer_gen = None
