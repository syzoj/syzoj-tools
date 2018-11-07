import os
import subprocess
from . import run_testlib_validator

class BuiltinValidator:
    builtin_validators = ["bipartite-graph-validator", "ival", "nval", "sval", "undirected-graph-validator", "undirected-tree-validator"]

    def __init__(self, problem, config):
        self.config = config
        self.problem = problem
        if not self.config["name"] in BuiltinValidator.builtin_validators:
            raise ProblemException("Unknown builtin validator: %s" % self.config["name"])
        self.name = self.config["name"]

    def check(self, case):
        cpp_file = os.path.join(os.path.dirname(__file__), "%s.cpp" % self.name)
        validator_file = os.path.join(os.path.dirname(__file__), "%s" % self.name)
        return run_testlib_validator(validator_file, case.input_data)
