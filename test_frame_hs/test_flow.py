import glob


class TestFlow:
    def __init__(self, config, connect, logger):
        self.config = config
        self.connect = connect
        self.logger = logger

    def run_test(self):
        test_files = self.check_test_folder()

        for f in test_files:
            self.do_tests(f)

    def check_test_folder(self):
        test_data_folder = self.config.get_test_data_folder()
        return [f for f in glob.glob(test_data_folder + '/*.json', recursive=True)]

    def do_tests(self, file_name):
        self.logger.start_test(file_name)

        with open(file_name) as f:
            test_data = eval(f.read())

        for test in test_data['tests']:
            self.logger.start_test_case(test['name'])

            query = test['query']
            expected_result = test['expected']
            actual_result = self.connect.execute(query)

            if actual_result == expected_result:
                self.logger.write_pass(query, actual_result)
            else:
                self.logger.write_faile(query, actual_result, expected_result)




