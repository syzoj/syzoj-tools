#!/usr/bin/python3
import argparse
import logging
from .problem import Problem
from .contest import Contest

def main():
    parser = argparse.ArgumentParser(prog="syzoj")
    subparser = parser.add_subparsers(dest="subcommands")
    parser.add_argument("--path", dest="path", default=".")
    parser.add_argument('-v', '--verbose', action='count', default=0)
    
    parser_config = subparser.add_parser("config", help="creates/edits the config")
    parser_config.set_defaults(func=cmd_config)
    
    parser_build = subparser.add_parser("build", help="builds the problem resources", description="Builds the problem resources and prepares it for deployment")
    parser_build.set_defaults(func=cmd_build)
    
    parser_test = subparser.add_parser("test", help="verifys the problem")
    parser_test.set_defaults(func=cmd_test)
    
    parser_judge = subparser.add_parser("judge", help="judge submissions")
    parser_judge.set_defaults(func=cmd_judge)
    parser_judge.add_argument("--nolazy", default=True, dest="lazy", action="store_const", const=False, help="Judge every testcase and don't be lazy")
    parser_judge.add_argument("prog", nargs="+")

    parser_contest = subparser.add_parser("contest", help="contest related commands")
    parser_contest.set_defaults(func=cmd_contest)
    subparser_contest = parser_contest.add_subparsers(dest="contest_subcommands")
    parser_contest_judge = subparser_contest.add_parser("judge", help="judges contest players")
    parser_contest_judge.set_defaults(func_contest=cmd_contest_judge)
    parser_contest_judge.add_argument("-f", "--force", default=False, dest="contest_judge_force", action="store_const", const=True, help="Judge even if judged")
    parser_contest_judge.add_argument("contest_judge_players", metavar="players", nargs="*", help="List of players to judge (empty to judge all)")
    parser_contest_export = subparser_contest.add_parser("export", help="exports contest result")
    parser_contest_export.set_defaults(func_contest=cmd_contest_export)
    parser_contest_export.add_argument("export_file", default="result.csv", nargs="?", help="The file to export to, must be CSV")

    args = parser.parse_args()
    if args.subcommands == None:
        print("No subcommand supplied")
        parser.print_help()
        exit(1)
    elif args.subcommands == "contest" and args.contest_subcommands == None:
        print("No subcommand supplied")
        parser_contest.print_help()
        exit(1)

    logging.addLevelName(15, "VERBOSE")
    logging.VERBOSE = 15
    def verbose(self, message, *args, **kwargs):
        self.log(logging.VERBOSE, message, *args, **kwargs)
    logging.Logger.verbose = verbose

    if args.verbose == 0:
        logging.basicConfig(level=logging.INFO)
    elif args.verbose == 1:
        logging.basicConfig(level=logging.VERBOSE)
    elif args.verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    args.func(args)

def cmd_config(args):
    problem = Problem(args.path)
    
def cmd_build(args):
    problem = Problem(args.path)
    problem.build(force=True)
    
def cmd_test(args):
    problem = Problem(args.path)
    test = problem.test()
    if test:
        print("All tests passed")
    else:
        print("Some tests failed, check for \"Assertion %d failed\" above")

    if not test:
        exit(1)
    
def cmd_judge(args):
    problem = Problem(args.path)
    for prog in args.prog:
        result = problem.judge(prog, lazy=args.lazy)
        if result.success:
            print("Score: %d" % result.score)
        else:
            print("Failed: %s" % result.message)
        print("Detailed result: ", result)

def cmd_contest(args):
    args.func_contest(args)

def cmd_contest_judge(args):
    contest = Contest(args.path)
    players = args.contest_judge_players
    try:
        contest.scan()
        if len(players) == 0:
            contest.judge_all(force=args.contest_judge_force)
        else:
            for player in players:
                contest.judge_player(player, force=args.contest_judge_force)
    finally:
        contest.save()

def cmd_contest_export(args):
    contest = Contest(args.path)
    contest.export(args.export_file)
