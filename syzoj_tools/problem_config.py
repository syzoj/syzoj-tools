import os
from ruamel.yaml import YAML

class ProblemConfig:
    def __init__(self, path):
        self.path = path
        self.config_path = os.path.join(self.path, "problem.yml")
        self.yaml = YAML()
        try:
            with open(self.config_path, "rb") as stream:
                self.config = self.yaml.load(stream)
        except FileNotFoundError:
            self.config = {}

    def interactive_config(self):
        cases_global = self.config.get("cases-global", {})
        default_memory_limit = cases_global.get("memory-limit", "256MB")
        while True:
            memory_limit = input("Input memory limit (must end with KB, MB or GB) [%s]:" % default_memory_limit) or default_memory_limit
            parsed_memory_limit = ProblemConfig.parse_memory_limit(memory_limit)
            if parsed_memory_limit == None:
                print("Invalid memory limit")
            else:
                break
        cases_global["memory-limit"] = memory_limit
        default_time_limit = cases_global.get("time-limit", "1s")
        while True:
            time_limit = input("Input time limit (must end with ms, us or s) [%s]:" % default_time_limit) or default_time_limit
            parsed_time_limit = ProblemConfig.parse_time_limit(time_limit)
            if parsed_time_limit == None:
                print("Invalid time limit")
            else:
                break
        cases_global["time-limit"] = time_limit
        self.config["cases-global"] = cases_global

    def parse_memory_limit(val):
        try:
            if val.endswith("KB"):
                return float(val[:-2])
            elif val.endswith("MB"):
                return float(val[:-2]) * 1024
            elif val.endswith("GB"):
                return float(val[:-2]) * 1048576
        except ValueError:
            pass

    def parse_time_limit(val):
        try:
            if val.endswith("ms"):
                return float(val[:-2])
            elif val.endswith("us"):
                return float(val[:-2]) / 1000
            elif val.endswith("s"):
                return float(val[:-1]) * 1000
        except ValueError:
            pass
    
    def save(self):
        with open(self.config_path, "wb") as stream:
            self.yaml.dump(self.config, stream)
