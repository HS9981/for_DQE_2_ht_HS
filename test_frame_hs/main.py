from sys import argv
from configurator import Config
from datetime import datetime
from connector import Connector
from outcome import Outcome
from test_flow import TestFlow

print(datetime.now())
# print(Config(argv[1]))

def run():
    config = Config(argv[1])
    print(config.config)

    db_url = config.get_db_url()
    print(db_url)

    connect = Connector(db_url)

    logger = Outcome()

    test = TestFlow(config, connect, logger)

    test.run_test()

    logger.finish()


if __name__ == '__main__':
    run()