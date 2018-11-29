import os
from . import CheckerResult

class DefaultChecker:
    def __init__(self, problem, config):
        self.config = config
        self.problem = problem

    def check(self, case, outfile):
        with open(case.answer_data, "rb") as answer_file:
            answer_lines = list(map(lambda s: s.rstrip(), answer_file.readlines()))
        with open(outfile, "rb") as out_file:
            out_lines = list(map(lambda s: s.rstrip(), out_file.readlines()))

        answer_cnt = len(answer_lines)
        while len(answer_lines[answer_cnt-1]) == 0 and answer_cnt > 0:
            answer_cnt -= 1
        out_cnt = len(out_lines)
        while len(out_lines[out_cnt-1]) == 0 and out_cnt > 0:
            out_cnt -= 1
        answer_lines = answer_lines[:answer_cnt]
        out_lines = out_lines[:out_cnt]

        if out_lines == answer_lines:
            return CheckerResult(True, message="Accepted", score=1.)
        else:
            return CheckerResult(False, message="Wrong Answer", score=0.)
