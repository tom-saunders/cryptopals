#!/usr/bin/env python

import argparse
import json
import os
import sys
import unittest

import xmlrunner

import util

def setup():
    argparser = argparse.ArgumentParser(
            description = 'Handler to run cryptopals tasks, and the testing around them')
    argparser.add_argument(
            '-t',
            '--tasks',
            action = 'append',
            type = str,
            required = False)
    argparser.add_argument(
            '-l',
            '--level',
            action = 'store',
            choices = ['task', 'full'],
            default = 'task',
            type = str,
            required = False)
    argparser.add_argument(
            '-v',
            '--verbose',
            action = 'count',
            default = 1,
            required = False)
    argparser.add_argument(
            '-o',
            '--output',
            default = 'test-reports',
            type = str,
            required = False)

    args = argparser.parse_args()

    util.set_tasks(args.tasks)
    util.set_task_level(args.level)

    return args

if __name__ == '__main__':
    args = setup()
    unittest.main(
            module = None,
            argv = [sys.argv[0]],
            testRunner=xmlrunner.XMLTestRunner(output=args.output),
            verbosity = args.verbose)
