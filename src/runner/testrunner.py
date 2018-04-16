
import unittest
from runner.HTMLTestRunner import HTMLTestRunner


class TestRunner(object):
    """docstring for TestRunner"""

    def __init__(self, path, title, description, casepath):
        self.path = path
        self.title = title
        self.description = description
        self.casepath = casepath
        self.caseList = []

    def set_case_list(self, file_name):
        with open(file_name) as fb:
            for value in fb.readlines():
                if value != '' and not value.startswith("#"):
                    self.caseList.append(value.replace("\n", ""))

    def set_case_suite(self):
        self.set_case_list(self.casepath)
        test_suite = unittest.TestSuite()
        suite_model = []
        for case in self.caseList:
            case_file = './testsuit'
            discover = unittest.defaultTestLoader.discover(
                case_file, pattern='{}.py'.format(case), top_level_dir=None)
            suite_model.append(discover)

        if len(suite_model) > 0:
            for suite in suite_model:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        # test_suite.addTest(unittest.makeSuite(TestNothing))
        return test_suite

    def run(self):
        suite = self.set_case_suite()
        if suite is not None:
            with open(self.path, 'wb') as file:
                runner = HTMLTestRunner(
                    stream=file,
                    title=self.title,
                    description=self.description,
                    verbosity=2)
                runner.run(suite)
