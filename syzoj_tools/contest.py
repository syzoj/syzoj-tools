from ruamel.yaml import YAML
import os
import pickle
import glob
import errno
import csv
import copy
import time
from .problem import Problem, ProblemException

class Contest:
    def __init__(self, path="."):
        self.path = path
        self.yaml = YAML()
        config_file = os.path.join(self.path, "contest.yml")
        try:
            with open(config_file, "r") as stream:
                try:
                    self.config = self.yaml.load(stream)
                except yaml.YAMLError:
                    raise
        except FileNotFoundError as e:
            raise ProblemException("File %s doesn't exist, create `contest.yml` first" % config_file) from e

        self.dump_file = os.path.join(self.path, "contest.dat")
        try:
            with open(self.dump_file, "rb") as stream:
                self.data = pickle.load(stream)
        except FileNotFoundError as e:
            self.data = ContestData()

        self.problems = []
        for problem_config in self.config["problems"]:
            problem = ContestProblem(self, problem_config)
            self.problems.append(problem)

        try:
            os.mkdir(os.path.join(self.path, "players"))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def scan(self):
        players = os.listdir(os.path.join(self.path, "players"))
        for player in players:
            if not player in self.data.players:
                print("New player %s" % player)
                self.data.players[player] = ContestPlayer(player)

    def cleanup(self):
        players = set(os.listdir(os.path.join(self.path, "players")))
        for player in self.data.players:
            if not player in players:
                players.pop(player)
        
        for name, player in self.data.players.items():
            player.cleanup()

    def judge_all(self, force=False):
        for player_name in self.data.players:
            self.judge_player(player_name, force=force)

    def judge_player(self, player_name, force=False):
        if not player_name in self.data.players:
            raise ProblemException("Unknown player %s" % player_name)
        player = copy.deepcopy(self.data.players[player_name])
        for problem in self.problems:
            if force or not problem.name in player.judge_result:
                files = glob.glob(os.path.join(self.path, "players", player.name, problem.name + ".*"))
                if len(files) != 0:
                    player.judge_result[problem.name] = problem.problem.judge(files[0])

        player.score = sum(result.score for _, result in player.judge_result.items())
        player.judge_time = time.time()
        self.data.players[player_name] = player

    def save(self):
        with open(self.dump_file, "wb") as stream:
            pickle.dump(self.data, stream)

    def export(self, path):
        with open(path, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["player", *[problem.name for problem in self.problems], "score"])
            for _, player in self.data.players.items():
                row = [player.name]
                for problem in self.problems:
                    try:
                        row.append(player.judge_result[problem.name].score)
                    except:
                        row.append(None)
                row.append(player.score)
                writer.writerow(row)

class ContestProblem:
    def __init__(self, contest, config):
        self.contest = contest
        self.config = config

        self.name = config["name"]
        self.path = os.path.join(self.contest.path, config["path"])
        self.problem = Problem(self.path)

class ContestData:
    def __init__(self):
        self.players = {}

class ContestPlayer:
    def __init__(self, name):
        self.name = name
        self.judge_result = {}
        self.judge_time = None
        self.score = None
