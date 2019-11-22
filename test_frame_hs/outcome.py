from datetime import datetime
import os


class Outcome:
    def __init__(self):
        print(os.getcwd())
        self.log_file = open('logging/outcome.log', 'w')
        print(os.getcwd())

    def start_test(self, file_name):
        msg = str(datetime.now()) + ' - ' + 'Testing of the {} started\r'.format(file_name)
        self.log_file.write(msg)

    def start_test_case(self, test_name):
        msg = str(datetime.now()) + ' - ' + 'Testing of the {} started\r'.format(test_name)
        self.log_file.write(msg)

    def write_pass(self, query, actual_result):
        msg = str(datetime.now()) + ' - ' + 'PASSED. Result is {}. Query: {}\r'.format(actual_result, query)
        self.log_file.write(msg)

    def write_faile(self, query, actual_result, expected_result):
        msg = str(datetime.now()) + ' - ' + 'FAILED.  Actual result is {} when expected is {}. Query: {}\r'.format(actual_result, expected_result, query)
        self.log_file.write(msg)

    def finish(self):
        self.log_file.close()



