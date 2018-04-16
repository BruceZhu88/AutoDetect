
import os
import datetime
from common.Config import Config
from runner.testrunner import TestRunner

main_cfg_path = '../config/main.ini'


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


config = Config(main_cfg_path)
config.cfg_load()
prj_name = config.cfg.get('Project', 'name')
report_path = config.cfg.get('Result', 'path')
testlist = config.cfg.get('TestCase', 'list')


make_dir(report_path)
reprot_name = '{}/{}_test_report_{}.html'.format(
    report_path, prj_name, datetime.datetime.now().strftime('%m%d%H%M%S'))
title = '{} Automation Test Report'.format(prj_name)
description = 'Test Execution Details:'

TR = TestRunner(reprot_name, title, description, testlist)
TR.run()
'''
TC = TestCase()
case_path = r'..\testfile\testcase\{}_test_case.csv'.format(prj_name)
with open(case_path, 'r') as cf:
    for k, row in enumerate(csv.reader(cf)):
        if TC.run(row):
            print('Test Case {}: Pass'.format(k))
        else:
            print('Test Case {}: Fail'.format(k))
        if k == 0:
            break
'''
# r = powerCycle()
# r.run()
