import os
import base64
import websocket
import urllib
import json
import tempfile
from .problem import Problem, ProblemException
from ruamel.yaml import YAML

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
        self.socket = websocket.WebSocketApp(self.url,
            header=[self.auth_header],
            on_message = self.ws_on_message,
            on_error = self.ws_on_error,
            on_close = self.ws_on_close,
            on_open = self.ws_on_open)
        self.socket.run_forever()

    def ws_on_message(self, message):
        data = json.loads(message)
        print(data)
        try:
            with tempfile.NamedTemporaryFile() as source_file:
                source_file.write(bytes(data["code"], "utf-8"))
                prob = Problem(os.path.join("problem", data["problem_id"]))
                result = prob.judge(source_file.name, data["language"])
                self.send_message({"tag": data["tag"], "result": {"status": result.score}})
        except ProblemException as e:
            print("Failed to judge problem %s" % data["problem_id"])
            print(e)
            self.send_message({"tag": data["tag"], "result": {"status": "error %s" % e}})

    def send_message(self, message):
        self.socket.send(json.dumps(message))

    def ws_on_error(self, error):
        print(error)

    def ws_on_open(self):
        print("Daemon open")

    def ws_on_close(self):
        print("Daemon close")
