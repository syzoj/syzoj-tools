#!/usr/bin/python3
import argparse
from .problem import Problem

def main():
    parser = argparse.ArgumentParser(prog = "syzoj")
    subparser = parser.add_subparsers(dest="subcommands")
    parser.add_argument("--path", dest="path", default=".")
    
    parser_config = subparser.add_parser("config", help="creates/edits the config")
    parser_config.set_defaults(func=cmd_config)
    
    parser_build = subparser.add_parser("build", help="builds the problem resources", description = "Builds the problem resources and prepares it for deployment")
    parser_build.set_defaults(func=cmd_build)
    
    parser_test = subparser.add_parser("test", help="verifys the problem")
    parser_test.set_defaults(func=cmd_test)
    
    parser_judge = subparser.add_parser("judge", help="judge submissions")
    parser_judge.set_defaults(func=cmd_judge)
    parser_judge.add_argument("prog")
    
    parser_deploy = subparser.add_parser("deploy", help="deploy the problem to SYZOJ")
    parser_deploy.set_defaults(func=cmd_deploy)
    args = parser.parse_args()
    if not 'func' in args:
        print("No subcommand supplied")
        exit()
    args.func(args)

def cmd_config(args):
    problem = Problem(args.path)
    
def cmd_build(args):
    problem = Problem(args.path)
    problem.build()
    
def cmd_test(args):
    problem = Problem(args.path)
    problem.test()
    
def cmd_judge(args):
    problem = Problem(args.path)
    (success, result) = problem.judge(args.prog)
    if success:
        print("Score: %d" % result)
    else:
        print("Failed: %s" % result)

def cmd_deploy(args):
    problem = Problem(args.path)
    problem.deploy()
