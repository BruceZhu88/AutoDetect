
import time
import sys
from src.common.Arduino import Arduino
from src.common.Logger import Logger
from src.common.Config import Config
from src.common.relay import relay
from src.common.DataProcess import DataProcess

main_cfg_path = './config/main.ini'


class powerCycle(object):
    """docstring for powerCycle"""

    def __init__(self):
        self.log = Logger("main").logger()
        self.ard = Arduino()
        self.process = DataProcess()
        config = Config('./config/{}.ini'.format(self.ard.project))
        config.cfg_load()
        self.led_num = config.cfg.getint('config', 'led')
        self.press_on = config.cfg.get('config', 'press_on')
        self.press_off = config.cfg.get('config', 'press_off')
        self.power_button = config.cfg.get('config', 'power_button')
        self.power_on_time = config.cfg.get('config', 'power_on_time')
        m_cfg = Config(main_cfg_path)
        m_cfg.cfg_load()
        self.led1_data = m_cfg.cfg.get('Data', 'led1')

    def run(self):
        '''
        r = relay()
        if not r.init_relay():
            self.log.error('Something is wrong with your relay!')
            sys.exit()
        '''
        self.ard.Thread_detect_data(self.led_num, self.power_on_time)
        # r.press(self.power_button, self.press_on)
        time.sleep(20)
        exp = [1, 1]
        compared_num = 100
        counting = 500
        # self.process.verify_data(self.led1_data, 'pulse', compared_num, counting, exp)
