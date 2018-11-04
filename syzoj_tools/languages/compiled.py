#!/usr/bin/python3
import os
import select
import tempfile
import subprocess
import shutil
import resource
import time
import signal

class SIGCHLDException(BaseException):
    pass

def sigchld_handler(signal, stack):
    raise(SIGCHLDException())

class RunResult:
    def __init__(self, success, message=None, rusage=None, signal=None, exitcode=None, outfile=None):
        self.success = success
        self.message = message
        self.rusage = rusage
        self.signal = signal
        self.exitcode = exitcode
        self.outfile = outfile

    def __repr__(self):
        return "RunResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

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
            shutil.copyfile(case.input_data, os.path.join(self.workdir, case.config["input-file"]))
            stdin = open(os.devnull, "r")

        if not "output-file" in case.config:
            stdout = self.tempfile = tempfile.NamedTemporaryFile()
        else:
            outfile = os.path.join(self.workdir, case.config["output-file"])
            stdout = open(os.devnull, "w")
        
        time_limit = int(case.time_limit / 1000) + 1
        memory_limit = int(case.memory_limit * 1024) + 32
        pid = os.fork()
        if pid == 0:
            os.dup2(stdin.fileno(), 0)
            os.dup2(stdout.fileno(), 1)
            os.chdir(self.workdir)
            resource.setrlimit(resource.RLIMIT_CPU, (time_limit, time_limit))
            resource.setrlimit(resource.RLIMIT_DATA, (memory_limit, memory_limit))
            resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))
            resource.setrlimit(resource.RLIMIT_STACK, (memory_limit, memory_limit))
            os.execlp(self.prog, self.prog)
            os._exit(1)
        else:
            start_time = time.time()
            while True:
                (_pid, status, rusage) = os.wait4(pid, os.WNOHANG)
                if _pid == pid:
                    break
                real_time = time.time() - start_time
                if real_time > time_limit:
                    os.kill(pid, signal.SIGKILL)
                try:
                    org_handler = signal.getsignal(signal.SIGCHLD)
                    signal.signal(signal.SIGCHLD, sigchld_handler)
                    select.select([], [], [], max(time_limit - real_time, 0.1))
                except SIGCHLDException:
                    pass
                finally:
                    signal.signal(signal.SIGCHLD, org_handler)
           
            real_time = time.time() - start_time
            signalnum, code = status & 0xFF, status >> 8
            print(rusage, signalnum, code)

            if rusage.ru_maxrss > case.memory_limit:
                return RunResult(success=False, message="Memory limit exceeded", rusage=rusage, signal=signalnum, exitcode=code)
            elif real_time > case.time_limit / 1000 or signalnum == 9:
                return RunResult(success=False, message="Time limit exceeded", rusage=rusage, signal=signalnum, exitcode=code)
            elif signalnum != 0:
                return RunResult(success=False, message="Runtime error", rusage=rusage, signal=signalnum, exitcode=code)
            elif code != 0:
                return RunResult(success=False, message="Runtime error", rusage=rusage, signal=signalnum, exitcode=code)
        
        if not "output-file" in case.config:
            return RunResult(success=True, outfile=stdout.name, rusage=rusage, signal=signalnum, exitcode=code)
        else:
            if not os.path.isfile(outfile):
                return RunResult(success=False, message="No output", rusage=rusage, signal=signalnum, exitcode=code)
            else:
                return RunResult(success=True, outfile=outfile, rusage=rusage, signal=signalnum, exitcode=code)

    def cleanup_judge(self):
        try:
            shutil.rmtree(self.workdir)
            del(self.workdir)
        except AttributeError:
            pass

        try:
            self.tempfile.close()
            del(self.tempfile)
        except AttributeError:
            pass
    
    def post_judge(self):
        shutil.rmtree(self.tempdir)

class ProblemCppLanguage:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config
        self.flags = self.config.get("flags", [])

    def judge_session(self, source):
        return ProblemCppLanguageJudgeSession(self, source)

class ProblemCppLanguageJudgeSession(CompiledLanguageJudgeSession):
    def get_compile_command(self, source, prog):
        return ["g++", source, "-o", prog, *self.language.flags]

class ProblemCLanguage:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config
        self.flags = self.config.get("flags", [])

    def judge_session(self, source):
        return ProblemCLanguageJudgeSession(self, source)

class ProblemCLanguageJudgeSession(CompiledLanguageJudgeSession):
    def get_compile_command(self, source, prog):
        return ["gcc", source, "-o", prog, *self.language.flags]

class ProblemPasLanguage:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config
        self.flags = self.config.get("flags", [])

    def judge_session(self, source):
        return ProblemPasLanguageJudgeSession(self, source)

class ProblemPasLanguageJudgeSession(CompiledLanguageJudgeSession):
    def get_compile_command(self, source, prog):
        return ["fpc", source, "-o" + prog, *self.language.flags]
