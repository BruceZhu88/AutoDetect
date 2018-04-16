
import time
import random
from common.readConfig import main_cfg_path
from common.Logger import Logger
from common.SerialHelper import SerialHelper
from common.Config import Config


class Relay(object):
    def __init__(self):
        self.log = Logger("main").logger()
        config = Config(main_cfg_path)
        config.cfg_load()
        self.port_name = config.cfg.get('Relay', 'port_name')
        self.port = None
        self.ser = None

    def init_relay(self):
        """Before operating relay, you must initialize it first.
        """
        self.ser = SerialHelper()
        if self.port_name is not None:
            port = self.ser.serial_port(self.port_name)
        elif self.port is not None:
            port = self.port_name
        else:
            self.log.error('Missing parameter[port or port_name]')
            return False
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

    def press(self, key, t):
        """Press and release relay port
        :param key: tuple type,
                    That means you also could control many ports simultaneously
        :param t: string type, the time of press
        :return None
        """
        if not self.ser.alive:
            return
        k = '00'
        for v in key:
            a, b = v, k
            k = hex(int(a, 16) ^ int(b, 16))
        if len(k) == 3:
            k = k.replace('0x', '0x0')
        if "-" in t:
            val = t.split("-")
            delay = round(random.uniform(float(val[0]), float(val[1])), 4)
        else:
            delay = float(t)
        # close relay
        self.ser.write(k.encode('utf-8'))
        # How long do you need to press
        time.sleep(delay)
        # release relay
        self.ser.write('0x00'.encode('utf-8'))
