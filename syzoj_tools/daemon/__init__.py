import os
import base64
import websocket
import urllib
import json
import tempfile
from ..problem import Problem, ProblemException
from ruamel.yaml import YAML
import time
import shutil

import grpc
from . import judge_pb2
from . import judge_pb2_grpc

class DaemonException(BaseException):
    pass

class Daemon:
    def __init__(self, path=""):
        self.path = path
        self.yaml = YAML()
        config_file = os.path.join(self.path, "daemon.yml")
        try:
            with open(config_file, "r") as stream:
                self.config = self.yaml.load(stream)
        except FileNotFoundError as e:
            raise DaemonException("daemon.yml does not exist")

        self.unsafe = self.config.get("unsafe", False)
        if self.unsafe != True:
            raise DaemonException("Non unsafe mode is currently not supported")

        self.data_path = os.path.join(self.path, "data")
        self.temp_path = os.path.join(self.path, "temp")
        self.parse_remote()

    def parse_remote(self):
        remote_config = self.config["remote"]
        self.url = remote_config["url"]
        self.client_id = remote_config["client-id"]
        self.token = remote_config["token"]
        quote_client_id = urllib.parse.quote_plus(bytes(self.client_id, "utf-8"))
        quote_token = urllib.parse.quote_plus(bytes(self.token, "utf-8"))
        auth_data = base64.b64encode(bytes("%s:%s" % (quote_client_id, quote_token), "utf-8")).decode("ascii")
        self.auth_header = "Authorization: Basic %s" % auth_data

    def run(self):
        channel = grpc.insecure_channel(self.url)
        self.stub = judge_pb2_grpc.JudgeStub(channel)
        while True:
            try:
                result = self.stub.FetchTask(judge_pb2.JudgeRequest(judger_id=self.client_id, judger_token=self.token))
                if result.success:
                    task = result.task
                    self.process_task(task)
                else:
                    time.sleep(1)
            except Exception as e:
                # TODO: Better exception handling
                print("Failed to process task: ", e)
    
    def send_result(self, task, result):
        self.stub.SetTaskResult(judge_pb2.SetTaskResultMessage(judger_id=self.client_id, judger_token=self.token, task_tag=task.task_tag, result=result))

    def process_task(self, task):
        print("Processing task %s" % task)
        try:
            problem = Problem(os.path.join(self.data_path, task.problem_id))
        except ProblemException as e:
            print("Failed to judge task %s: " % task.task_tag, e)
            self.send_result(task, judge_pb2.TaskResult(result="ERROR", score=0))
            return

        shutil.rmtree(self.temp_path, True)
        os.makedirs(self.temp_path, exist_ok=True)
        if task.language == "cpp":
            filename = os.path.join(self.temp_path, "file.cpp")
        elif task.language == "c":
            filename = os.path.join(self.temp_path, "file.c")
        elif task.language == "pas":
            filename = os.path.join(self.temp_path, "file.pas")
        else:
            print("Failed to judge task %s: unknown language" % task.task_tag)
            self.send_result(task, judge_pb2.TaskResult(result="ERROR", score=0))
            return

        with open(filename, "w") as f:
            f.write(task.code)
        result = problem.judge(filename)
        print(result)
        self.send_result(task, judge_pb2.TaskResult(result="Done", score=result.score))
