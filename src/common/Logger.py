import logging.config
import os
from common.readConfig import log_path
from common.readConfig import cfg_path


class Logger(object):

    def __init__(self, log_name):
        self.log_name = log_name
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        logging.config.fileConfig(
            "{}/logger_{}.conf".format(cfg_path, self.log_name))

    # config = {    "key1":"value1"     }
    def logger(self):
        return logging.getLogger(self.log_name)
