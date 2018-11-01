import yaml
import os

class Problem:
    def __init__(self, path="."):
        self.path = path
    
    def load(self):
        with open(os.path.join(self.path, "problem.yml"), 'r') as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError:
                raise
        
        self.data = []
        for index, data in enumerate(self.config["cases"], start=1):
            self.data.append(ProblemCase(self, index, data))
    
    def build(self):
        for data in self.data:
            data.build()
    
    def test(self):
        print("test")
    
    def judge(self, prog):
        print("judge")
    
    def deploy(self):
        print("deploy")

class ProblemCase:
    def __init__(self, problem, index, config):
        self.config = config
        self.index = index
        self.problem = problem
        self.name = self.config.get("name", str(self.index))
        self.input_file = os.path.join(self.problem.path, self.config.get("input-data", "data/%s.in" % self.name))
        self.output_file = os.path.join(self.problem.path, self.config.get("output-data", "data/%s.out" % self.name))
        
    def load(self):
        pass
    
    def build(self):
        if not os.path.exists(self.input_file):
            print("Input file not found")
        
        if not os.path.exists(self.output_file):
            print("Output file not found")