#!/usr/bin/python3
import os
import tempfile
import subprocess
import shutil

class CompiledLanguageJudgeSession:
    def __init__(self, language, source):
        self.language = language
        self.source = source

    def pre_judge(self):
        print("Compiling source code %s" % self.source)
        self.tempdir = tempfile.mkdtemp()
        self.prog = os.path.join(self.tempdir, "prog")
        try:
            subprocess.run(self.get_compile_command(self.source, self.prog), check=True)
        except subprocess.CalledProcessError:
            print("Compilation failed")
            return "Compilation Error"

    def run_judge(self, case):
        self.workdir = tempfile.mkdtemp()
        if not "input-file" in case.config:
            stdin = open(case.input_data, "rb")
        else:
            shutil.copyfile(case.config["input-data"], os.path.join(self.workdir, case.config["input-file"]))
            stdin = subprocess.DEVNULL

        if not "output-file" in case.config:
            stdout = tempfile.NamedTemporaryFile()
        else:
            outfile = os.path.join(self.workdir, case.config["output-file"])
            stdout = subprocess.DEVNULL
        
        try:
            subprocess.run([self.prog], stdin=stdin, stdout=stdout, cwd=self.workdir, check=True)
        except subprocess.CalledProcessError:
            return (False, "Runtime error")
        
        if not "output-file" in case.config:
            return (True, stdout.name)
        else:
            if not os.path.isfile(outfile):
                return (False, "No output")
            else:
                return (True, outfile)

    def cleanup_judge(self):
        shutil.rmtree(self.workdir)
    
    def post_judge(self):
        shutil.rmtree(self.tempdir)

class ProblemCppLanguage:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config

    def judge_session(self, source):
        return ProblemCppLanguageJudgeSession(self, source)

class ProblemCppLanguageJudgeSession(CompiledLanguageJudgeSession):
    def get_compile_command(self, source, prog):
        return ["g++", source, "-o", prog]

class ProblemCLanguage:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config

    def judge_session(self, source):
        return ProblemCLanguageJudgeSession(self, source)

class ProblemCLanguageJudgeSession(CompiledLanguageJudgeSession):
    def get_compile_command(self, source, prog):
        return ["gcc", source, "-o", prog]

class ProblemPasLanguage:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config

    def judge_session(self, source):
        return ProblemPasLanguageJudgeSession(self, source)

class ProblemPasLanguageJudgeSession(CompiledLanguageJudgeSession):
    def get_compile_command(self, source, prog):
        return ["fpc", source, "-o" + prog]
