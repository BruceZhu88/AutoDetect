"""Waves Data Process
Features: Judge LED waves if it is pulse or flash
Notes: You need to change your arguments with your data sampling rate
"""
__author__ = 'Bruce.Zhu'

import re
from itertools import dropwhile
from common.Logger import Logger


class DataProcess(object):
    """docstring for DataProcess"""

    def __init__(self):
        self.log = Logger('main').logger()

    def verify_data(self, data_path, data_type, exp):
        """
        """
        self.log.info('Verifing data [{}]'.format(data_type))
        data, t, k1, k2 = self.split_data(data_path)
        count = 3
        wave_range = [150, 200]
        if float(exp[0]) <= 1 and float(exp[1]) <= 1:
            count = 6
        if data_type == 'data':
            result = self.led_status(data, [k1, k2], exp)
            self.log.info(result)
            return result
        elif data_type == 'pulse':
            # compared_num = 100  # if sampling rate range is 500-800
            # counting = 500  # if sampling rate range is 500-800
            act = self.led_pulse(data, count, [k1, k2])
            return int(exp[0]) <= act[0] and int(exp[1]) <= act[1]
        elif data_type == 'flash':
            period = [float(exp[0]), float(exp[1])]
            result = self.led_flash(data, t, wave_range, [k1, k2], period)
            return result
            # return int(exp[0]) <= act[0] and int(exp[1]) <= act[1]
        elif data_type == 'transition':
            act = self.led_transition(data, count, [k1, k2])
            return act[0] == int(exp[0]) and act[1] == int(exp[1])
        elif data_type == 'audio_cue':
            act = self.audio_cue(data, [k1, k2])
            return int(exp[0]) <= act[0] and int(exp[1]) <= act[1]

    """
    def peak_vally():
        path = './CA17_power_on_LED_600.txt'
        data = []
        t1 = '2018-02-08 13:20:11'
        t2 = '2018-02-08 13:20:59'
        k1, k2 = 0, 0
        with open(path, 'r') as f:
            for k, line in enumerate(dropwhile(lambda line: line.startswith('#'), f)):
                value = int(re.findall(r': (.*)\n', line)[0])
                t = re.findall(r'(.*):', line)[0]
                if t1 in t:
                    k1 = k
                elif t2 in t:
                    k2 = k
                data.append(value)
        # print(min(data))
        # print(min(data[k1:k2]))
        top, bottom = 0, 0
        counting = 80
        if k1 != 0 and k2 != 0:
            max_power_on = max(data[k1:k2])
            min_power_on = min(data[k1:k2])
            avg_power_on = sum(data[k1:k2]) / len(data[k1:k2])
            print('max:{}, min:{}'.format(max_power_on, min_power_on))
            flag = 0
            i = 0
            for k, d in enumerate(data[k1:k2]):
                i += 1
                if d > avg_power_on:
                    if flag == -1 and i > counting:
                        bottom += 1
                        i = 0
                    flag = 1
                else:
                    if flag == 1 and i > counting:
                        top += 1
                        i = 0
                    flag = -1

        print('peak={}, vally={}'.format(top, bottom))

    """
    @staticmethod
    def split_time(t):
        a, b, c = t.split(':')
        s, ms = c.split('.')
        ms = int(ms) * 0.0001
        return int(s), ms

    def time_diff(self, t1, t2):
        """Just for seconds, and t2 > t1"""
        s1, ms1 = self.split_time(t1)
        s2, ms2 = self.split_time(t2)
        s = 0
        if s1 > s2:
            s2 += 60
        if ms1 > ms2:
            ms2 += 1
            s = -1
        s = s2 - s1 + s
        ms = ms2 - ms1
        return (s + round(ms, 4))

    @staticmethod
    def split_data(data_path, t1=None, t2=None):
        """
        :param data_path: strings
        :param t1: strings, time of head
        :param t2: strings, time of end
        """
        data, t = [], []
        k1, k2 = 0, 0
        with open(data_path, 'r') as f:
            for k, line in enumerate(dropwhile(
                    lambda line: line.startswith('#'), f)):
                value = int(re.findall(r': (.*)\n', line)[0])
                value_t = re.findall(r'(.*):', line)[0]
                if t1 and t1 in value_t:
                    k1 = k
                elif t2 and t2 in value_t:
                    k2 = k
                data.append(value)
                t.append(value_t)
        return data, t, k1, k2

    def check_data(self, data, drange):
        new_data = []
        if drange[0] == 0 or drange[1] == 0:
            new_data = data
        elif drange[1] > drange[0]:
            new_data = data[drange[0]:drange[1]]
        else:
            self.log.info('Something wrong with your data range!')
        return new_data

    def led_status(self, data, drange, srange):
        """
        :param data: list
        :param drange: list, data range between time1 and time2
        :param srange: list, status range
        :return on or off
        """
        new_data = self.check_data(data, drange)
        avg = round(sum(new_data) / len(new_data))
        self.log.info('data avg = {}, range = {}'.format(avg, srange))
        if avg in range(int(srange[0]), int(srange[1])):
            return True
        else:
            return False

    def led_pulse(self, data, counting, drange, compared_num=100):
        """Judge LED data waves if it's a pulse behavior  /\/\/\
        :param data: list
        :param compared_num: int, numbers of compared data(countinuous data)
        :param counting: int, continuous times of meet requirement
        :param drange: list, data range between time1 and time2
        :return (up, down): numbers of continuous rise of fall
        """
        num = compared_num
        flag, count, up, down = 0, 0, 0, 0
        new_data = self.check_data(data, drange)
        for i in range(len(new_data) - num * 2):
            avg1 = round(sum(new_data[i:i + (num - 1)]) /
                         len(new_data[i:i + (num - 1)]))
            avg2 = round(sum(new_data[i + num:i + (num * 2 - 1)]) /
                         len(new_data[i + num:i + (num * 2 - 1)]))
            # print('{} {} {}'.format(avg1, avg2, count))
            count += 1
            if avg1 > avg2:
                if flag == 1 and count > counting:
                    count = 0
                    up += 1
                flag = -1
            elif avg1 < avg2:
                if flag == -1 and count > counting:
                    count = 0
                    down += 1
                flag = 1
            else:
                if flag == 1 and count > counting:
                    count = 0
                    up += 1
                if flag == -1 and count > counting:
                    count = 0
                    down += 1
                count = 0
                flag = 0
        self.log.info('led actual results: up={}, down={}'.format(up, down))
        return up, down

    def led_flash(self, data, t, wrange, drange, period):
        """Judge LED data waves if it's a flash behavior
        :param data: list
        :param wrange: list, max - min
        :param drange: list, data range between time1 and time2
        :return (up, down): numbers of continuous rise of fall
        """
        flag, count, up, down = 0, 0, 0, 0
        tmp = []
        new_data = self.check_data(data, drange)
        r = range(wrange[0], wrange[1])
        r1 = range(-wrange[1], -wrange[0])
        for i in range(len(new_data) - 5):
            v1 = new_data[i + 1] - new_data[i]
            v2 = new_data[i + 2] - new_data[i]
            v3 = new_data[i + 3] - new_data[i]
            v4 = new_data[i + 4] - new_data[i]
            # self.log.info('{} {} {} {}'.format(v1, v2, v3, v4))
            if v1 in r or v2 in r or v3 in r or v4 in r:
                if flag == 1:
                    # print('{} {} {}'.format(new_t[i], flag, new_data[i]))
                    down += 1
                    tmp.append(t[i])
                flag, count = -1, 0
            elif v1 in r1 or v2 in r1 or v3 in r1 or v4 in r1:
                if flag == -1:
                    # print('{} {} {}'.format(new_t[i], flag, new_data[i]))
                    up += 1
                    tmp.append(t[i])
                flag, count = 1, 0
            count += 1
        k = 0
        while k < len(tmp) - 1:
            t_d = self.time_diff(tmp[k], tmp[k + 1])
            if not period[0] < t_d < period[1]:
                # self.log.info(t_d)
                self.log.info('{}, {}'.format(tmp[k], tmp[k + 1]))
                return False
            k += 1
        return True
        # self.log.info('led actual results: up={}, down={}'.format(up, down))
        # return up, down

    def led_transition(self, data, counting, drange, compared_num=100):
        """Judge LED data waves if it's a transition behavior
        :param data: list
        :param compared_num: int, numbers of compared data(countinuous data)
        :param counting: int, continuous times of meet requirement
        :param drange: list, data range between time1 and time2
        :return (up, down): numbers of continuous rise of fall
        """
        num = compared_num
        count, up, down = 0, 0, 0
        new_data = self.check_data(data, drange)
        i = 0
        while i < (len(new_data) - num * 2):
            avg1 = round(sum(new_data[i:i + (num - 1)]) /
                         len(new_data[i:i + (num - 1)]))
            avg2 = round(sum(new_data[i + num:i + (num * 2 - 1)]) /
                         len(new_data[i + num:i + (num * 2 - 1)]))
            # print('{} {} {}'.format(avg1, avg2, count))
            count += 1
            if avg1 - avg2 < -20:
                if count > counting:
                    count = 0
                    up += 1
            elif avg1 - avg2 > 20:
                if count > counting:
                    count = 0
                    down += 1
            else:
                count = 0
            i = i + num
        self.log.info('led actual results: up={}, down={}'.format(up, down))
        return up, down

    def audio_cue(self, data, drange):
        """sound getting smaller
        :param data: list
        :param drange: list, data range between time1 and time2
        :return bottom: int, numbers of bottom with countinuous rise
        """
        new_data = self.check_data(data, drange)
        avg = sum(new_data) / len(new_data)
        top = 0
        low = 0
        for d in new_data:
            if d - avg > 2:
                top += 1
            elif d - avg < -2:
                low += 1
        self.log.info('sound actual results: top={} low={}'.format(top, low))
        return top, low

    def audio_cue2(self, data, compared_num, drange):
        """sound getting smaller
        :param data: list
        :param compared_num: int, numbers of compared data(countinuous data)
        :param drange: list, data range between time1 and time2
        :return bottom: int, numbers of bottom with countinuous rise
        """
        num = compared_num
        new_data = self.check_data(data, drange)
        count = 0
        i = 0
        bottom = 0
        while i < len(new_data) - 10:
            for j in range(1, num + 1):
                if new_data[i + j] - new_data[i + j - 1] > 0:
                    count += 1
                else:
                    count = 0
                if count >= num:
                    # print('{} {}'.format(new_data[i + j], new_data[i + j - 1]))
                    bottom += 1
                    i += num
            i += 1
        self.log.info('sound actual results: bottom={}'.format(bottom))
        return bottom

    @staticmethod
    def compare(exp, act):
        """
        :param exp: list or tuple, expected results
        :param act: list or tuple, actual results
        :return True/Flase: results of comparison between exp and act
        """
        return exp[0] <= act[0] and exp[1] <= act[1]


'''

# CA19_power_on_led_600.txt CA17_power_on_LED_600.txt
data_path = './CA17_power_on_LED_600.txt'
compared_num = 100  # if sampling rate range is 500-800
counting = 500  # if sampling rate range is 500-800
exp_value = [5, 5]
data, t, k1, k2 = split_data(data_path)
act_value = led_pulse(data, compared_num, counting, [k1, k2])

print(compare(exp_value, act_value))
'''

'''
data_path = './CA19_power_on_led_600.txt'
t1 = '2018-02-08 10:39:10'
t2 = '2018-02-08 10:39:29'
wave_range = [180, 200]
data, t, k1, k2 = split_data(data_path, t1=t1, t2=t2)
exp_value = [2, 2]
act_value = led_flash(data, wave_range, [k1, k2])
print(act_value)
print(compare(exp_value, act_value))
'''

"""
data_path = './CA19_audio_cue_600.txt'
t1 = '2018-02-08 10:39:18'
t2 = '2018-02-08 10:39:28'
data, t, k1, k2 = split_data(data_path, t1=t1, t2=t2)

compared_num = 5
exp_value = 3
act_value = audio_cue(data, compared_num, [k1, k2])
if act_value >= exp_value:
    print(True)
"""
