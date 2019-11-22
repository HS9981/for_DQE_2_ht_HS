import os


class Config:
    def __init__(self, env):
        print(os.getcwd())
        with open('/test_frame_hs/config.json') as f:
            print(os.getcwd())
            self.config = eval(f.read())
            print(os.getcwd())
        self.config = self.config[env]
        print(os.getcwd())

    def get_db_url(self):
        return self.config['database']

    def get_test_data_folder(self):
        return self.config['test_data']


