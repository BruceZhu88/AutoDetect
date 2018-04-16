
import time
import sys
import re
from common.readConfig import main_cfg_path
from common.Arduino import Arduino
from common.Logger import Logger
from common.Config import Config
from common.relay import Relay
from common.DataProcess import DataProcess
from common.parseCSV import ParseCSV


class Speaker(object):
    """docstring for Speaker"""

    def __init__(self):
        self.log = Logger("main").logger()
        self.ard = Arduino()
        self.process = DataProcess()
        self.r = Relay()
        self.keyword = ParseCSV(
            '../testfile/testcase/{}_keyword.csv'.format(self.ard.project))
        config = Config('../config/{}.ini'.format(self.ard.project))
        config.cfg_load()
        self.led_num = config.cfg.getint('config', 'led')
        self.power_button = config.cfg.get('config', 'power_button')
        m_cfg = Config(main_cfg_path)
        m_cfg.cfg_load()
        self.led1_data = m_cfg.cfg.get('Data', 'led1')
        self.sound_data = m_cfg.cfg.get('Data', 'sound')
        if not self.r.init_relay():
            self.log.error('Something is wrong with your relay!')
            sys.exit()

    def behave(self, name):
        row = self.keyword.get_row(name)
        self.log.info(name)
        button = row.get('power_button_press')
        time_wait = row.get('time_wait')
        audio_cue = row.get('audio_cue')
        tmp = re.findall(r'[^()]+', row.get('led1'))
        exp_led = tmp[1].split('-')
        if 'n/a' not in button.lower():
            if 'data' != tmp[0]:
                self.ard.Thread_detect_data(self.led_num, time_wait)
                self.r.press(self.power_button, button)
            else:
                self.r.press(self.power_button, button)
                time.sleep(time_wait)
                self.ard.Thread_detect_data(self.led_num, time_wait)
            time.sleep(time_wait * 2)
            assert self.process.verify_data(self.led1_data, tmp[0], exp_led)
            if 'y' in audio_cue.lower():
                exp = re.findall(r'[^()]+', audio_cue)[1].split('-')
                assert self.process.verify_data(
                    self.sound_data, 'audio_cue', exp)
        else:
            time.sleep(time_wait - 25)
            self.ard.Thread_detect_data(self.led_num, 25)
            time.sleep(25 * 1.5)
            if 'y' in audio_cue.lower():
                exp = re.findall(r'[^()]+', audio_cue)[1].split('-')
                assert self.process.verify_data(
                    self.sound_data, 'audio_cue', exp)
            time.sleep(2)
            self.ard.Thread_detect_data(self.led_num, 3)
            time.sleep(3 * 2)
            assert self.process.verify_data(self.led1_data, tmp[0], exp_led)

    def power_on(self):
        self.behave('power on')

    def power_off(self):
        self.behave('power off')

    def bt_pairing(self):
        self.behave('BT pairing')

    def bt_cancel_pairing(self):
        self.behave('BT cancel pairing')

    def bt_pairing_timeout(self):
        self.behave('BT pairing timeout')
