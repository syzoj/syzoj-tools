#!/usr/bin/python3
import os
import select
import tempfile
import subprocess
import shutil
import resource
import time
import signal
import math
import logging
from ..problem import PreJudgeResult
logger = logging.getLogger("compiled-language")

class SIGCHLDException(BaseException):
    pass

def sigchld_handler(signal, stack):
    raise(SIGCHLDException())

class RunResult:
    def __init__(self, success, message=None, rusage=None, signal=None, exitcode=None, outfile=None, stderr=None):
        self.success = success
        self.message = message
        self.rusage = rusage
        self.signal = signal
        self.exitcode = exitcode
        self.outfile = outfile
        self.stderr = stderr

    def __repr__(self):
        return "RunResult(%s)" % ', '.join(map(lambda kv: "{key}={value}".format(key=kv[0], value=kv[1]), vars(self).items()))

class CompiledLanguage:
    def __init__(self, problem, config={}):
        self.problem = problem
        self.config = config
        self.flags = self.config.get("flags", [])

    def judge_session(self, source):
        return CompiledLanguageJudgeSession(self, source)

    def compile(self, source, prog):
        subprocess.run(self.get_compile_command(source, prog), check=True)

    def get_args(self, prog, *args):
        return [prog, *args]

class CompiledLanguageJudgeSession:
    def __init__(self, language, source):
        self.language = language
        self.source = source

    def pre_judge(self):
        logger.verbose("Compiling source code %s" % self.source)
        self.tempdir = tempfile.mkdtemp()
        self.prog = os.path.join(self.tempdir, "prog")
        try:
            result = subprocess.run(self.language.get_compile_command(self.source, self.prog), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            logger.verbose("Compilation success")
            return PreJudgeResult(True, result.stderr)
        except subprocess.CalledProcessError as e:
            logger.verbose("Compilation failed: %s" % e)
            return PreJudgeResult(False, e.stderr)

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

        stderr_file = tempfile.TemporaryFile()
        
        time_limit = case.time_limit / 1000
        memory_limit = int(case.memory_limit * 1024) + 32
        pid = os.fork()
        if pid == 0:
            os.dup2(stdin.fileno(), 0)
            os.dup2(stdout.fileno(), 1)
            os.dup2(stderr_file.fileno(), 2)
            os.chdir(self.workdir)
            resource.setrlimit(resource.RLIMIT_CPU, (math.ceil(time_limit), math.ceil(time_limit)))
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
            stderr = stderr_file.read()

            if rusage.ru_maxrss > case.memory_limit:
                return RunResult(success=False, message="Memory limit exceeded", rusage=rusage, signal=signalnum, exitcode=code, stderr=stderr)
            elif real_time > case.time_limit / 1000 or signalnum == 9:
                return RunResult(success=False, message="Time limit exceeded", rusage=rusage, signal=signalnum, exitcode=code, stderr=stderr)
            elif signalnum != 0:
                return RunResult(success=False, message="Runtime error", rusage=rusage, signal=signalnum, exitcode=code, stderr=stderr)
            elif code != 0:
                return RunResult(success=False, message="Runtime error", rusage=rusage, signal=signalnum, exitcode=code, stderr=stderr)
        
        if not "output-file" in case.config:
            return RunResult(success=True, outfile=stdout.name, rusage=rusage, signal=signalnum, exitcode=code, stderr=stderr)
        else:
            if not os.path.isfile(outfile):
                return RunResult(success=False, message="No output", rusage=rusage, signal=signalnum, exitcode=code, stderr=stderr)
            else:
                return RunResult(success=True, outfile=outfile, rusage=rusage, signal=signalnum, exitcode=code, stderr=stderr)

    def cleanup_judge(self):
        try:
            shutil.rmtree(self.workdir)
        except (AttributeError, FileNotFoundError):
            pass
        self.workdir = None

        try:
            self.tempfile.close()
        except (AttributeError, FileNotFoundError):
            pass
        self.tempfile = None
    
    def post_judge(self):
        shutil.rmtree(self.tempdir)

class ProblemCppLanguage(CompiledLanguage):
    def get_compile_command(self, source, prog):
        return ["g++", source, "-o", prog, *self.flags]

class ProblemCLanguage(CompiledLanguage):
    def get_compile_command(self, source, prog):
        return ["gcc", source, "-o", prog, *self.flags]

class ProblemPasLanguage(CompiledLanguage):
    def get_compile_command(self, source, prog):
        return ["fpc", source, "-o" + prog, *self.flags]

