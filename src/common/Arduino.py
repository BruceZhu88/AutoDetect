

import time
import sys
import datetime
import _thread
import os.path
from shutil import copyfile
from common.readConfig import main_cfg_path
from common.SerialHelper import SerialHelper
from common.Config import Config
from common.Logger import Logger


class Arduino(object):
    """docstring for ClassName"""

    def __init__(self):
        self.log = Logger('main').logger()
        config = Config(main_cfg_path)
        config.cfg_load()
        port = config.cfg.get('Arduino', 'port_name')
        baudrate = config.cfg.get('Arduino', 'baudrate')
        self.project = config.cfg.get('Project', 'name')
        self.tmp_data = config.cfg.get('Data', 'tmp')
        self.led1 = config.cfg.get('Data', 'led1')
        self.led2 = config.cfg.get('Data', 'led2')
        self.sound = config.cfg.get('Data', 'sound')
        self.data_backup = config.cfg.get('Log', 'data_backup')
        self.ser = SerialHelper()
        port_name = config.cfg.get('Arduino', 'port_name')
        port = self.ser.serial_port(port_name)
        if port != '':
            self.ser.port = port
            self.ser.baudrate = baudrate
            self.ser.start()
            if not self.ser.alive:
                self.log.error('Cannot open port {}!'.format(port))
                sys.exit()
        else:
            self.log.error('Cannot find port {}!'.format(port_name))
            sys.exit()
        # here must add sleep >= 2, will be cannot receive if not
        time.sleep(2)

    @staticmethod
    def write_file(path, type, text):
        with open(path, type) as f:
            f.write(text)

    @staticmethod
    def move_file(src, _dir):
        if not os.path.exists(_dir):
            os.mkdir(_dir)
        a, b = os.path.basename(src).rsplit('.')
        dst = _dir + a + \
            datetime.datetime.now().strftime('_%m%d%H%M%S') + '.' + b
        copyfile(src, dst)

    def relay(self, num, t):
        self.ser.write('{},{},{}'.format('relay', num, t).encode())

    def detect(self, name, num, t):
        self.log.info('Detecting sound and led data')
        self.write_file(self.tmp_data.format(name), 'w', '')
        self.ser.write('{},{},{}'.format(name, num, t).encode())
        # start = time.time()
        read_val = ''
        with open(self.tmp_data.format(name), 'a') as f:
            while True:   # time.time() - start < t
                try:
                    read_val = self.ser.readline().decode().replace("\r\n", "")
                except Exception as e:
                    self.log.error(e)
                if read_val != '':
                    value = datetime.datetime.now().strftime(
                        '%m-%d %H:%M:%S.%f')[:-2] + ": " + read_val
                    # print(value)
                    f.write(value + "\n")
                else:
                    break
        # print(time.time() - start)
        # print(read_val)

    def run_detect(self, name, num, t):
        self.detect(name, num, t)
        if name == 'all':
            self.log.info('Processing data')
            self.write_file(self.led1, 'w', '')
            self.write_file(self.led2, 'w', '')
            self.write_file(self.sound, 'w', '')
            with open(self.tmp_data.format(name), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if '1L' in line:
                        line = line.replace('1L', '')
                        self.write_file(self.led1, 'a', line)
                    elif '2L' in line:
                        line = line.replace('2L', '')
                        self.write_file(self.led2, 'a', line)
                    elif 'S' in line:
                        line = line.replace('S', '')
                        self.write_file(self.sound, 'a', line)
            self.move_file(self.led1, self.data_backup)
            self.move_file(self.led2, self.data_backup)
            self.move_file(self.sound, self.data_backup)

    def Thread_detect_data(self, num, t):
        try:
            _thread.start_new_thread(
                self.run_detect, ('all', num, t))
        except Exception as e:
            self.log.info(
                'Error when start Thread_detect_data: {0}'.format(e))
