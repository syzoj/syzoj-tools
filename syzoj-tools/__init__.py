#!/usr/bin/python
import argparse

def main():
    parser = argparse.ArgumentParser(prog = "syzoj")
    subparser = parser.add_subparsers()
    parser_build = subparser.add_parser("build", help="builds the problem resources", description = "Builds the problem resources and prepares it for deployment")
    parser_judge = subparser.add_parser("judge", help="judge submissions")
    parser_test = subparser.add_parser("test", help="verifys the problem")
    parser_deploy = subparser.add_parser("deploy", help="deploy the problem to SYZOJ")
    parser.parse_args()

main()
