class Problem:
    def __init__(self, path="."):
        self.path = path
    
    def load(self):
        print("load")
    
    def build(self):
        print("build")
    
    def test(self):
        print("test")
    
    def judge(self):
        print("judge")
    
    def deploy(self):
        print("deploy")