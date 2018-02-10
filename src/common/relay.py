
import time
import random

from src.common.Logger import Logger
from src.common.SerialHelper import SerialHelper
from src.common.Config import Config

path = './config/main.ini'


class relay(object):
    def __init__(self):
        self.log = Logger("main").logger()
        config = Config(path)
        config.cfg_load()
        self.port_name = config.cfg.get('Relay', 'port_name')
        self.ser = None

    def init_relay(self):
        self.ser = SerialHelper()
        port = self.ser.serial_port(self.port_name)
        if port != '':
            self.ser.port = port
            self.ser.start()
        if self.ser.alive:
            try:
                time.sleep(0.5)
                self.ser.write('50'.encode('utf-8'), isHex=True)
                time.sleep(0.5)
                self.ser.write('51'.encode('utf-8'), isHex=True)
                time.sleep(0.5)
                return True
            except Exception as e:
                self.log.info(e)
        return False

    def press(self, n, t):
        if "-" in t:
            val = t.split("-")
            t_delay = round(random.uniform(float(val[0]), float(val[1])), 4)
        else:
            t_delay = float(t)
        self.ser.write(n.encode('utf-8'), isHex=True)
        time.sleep(t_delay)
        self.ser.write('00'.encode('utf-8'), isHex=True)
