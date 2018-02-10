"""Waves Data Process
Features: Judge LED waves if it is pulse or flash
Notes: You need to change your arguments with your data sampling rate
"""
__author__ = 'Bruce.Zhu'

import re
from itertools import dropwhile


class DataProcess(object):
    """docstring for DataProcess"""
    def __init__(self):
        pass

    def verify_data(self, data_path, data_type, compared_num, counting, exp):
        if data_type == 'pulse':
            # compared_num = 100  # if sampling rate range is 500-800
            # counting = 500  # if sampling rate range is 500-800
            data, t, k1, k2 = self.split_data(data_path)
            act_value = self.led_pulse(data, compared_num, counting, [k1, k2])
            print(act_value)
            print(self.compare(exp, act_value))

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

    @staticmethod
    def led_pulse(data, compared_num, counting, drange):
        """Judge LED data waves if it's a pulse behavior  /\/\/\
        :param data: list
        :param compared_num: int, numbers of compared data(countinuous data)
        :param counting: int, continuous times of meet requirement
        :param drange: list, data range between time1 and time2
        :return (up, down): numbers of continuous rise of fall
        """
        num = compared_num
        flag, count, up, down = 0, 0, 0, 0
        if drange[0] == 0 or drange[1] == 0:
            new_data = data
        elif drange[1] > drange[0]:
            new_data = data[drange[0]:drange[1]]
        else:
            print('Some thing wrong with your data range!')
            return
        for i in range(len(new_data) - num * 2):
            avg1 = round(sum(new_data[i:i + (num - 1)]) /
                         len(new_data[i:i + (num - 1)]))
            avg2 = round(sum(new_data[i + num:i + (num * 2 - 1)]) /
                         len(new_data[i + 100:i + (num * 2 - 1)]))
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

        return up, down

    @staticmethod
    def led_flash(data, wrange, drange):
        """Judge LED data waves if it's a flash behavior
        :param data: list
        :param wrange: list, max - min
        :param drange: list, data range between time1 and time2
        :return (up, down): numbers of continuous rise of fall
        """
        flag, count, up, down = 0, 0, 0, 0
        if drange[0] == 0 or drange[1] == 0:
            new_data = data
        elif drange[1] > drange[0]:
            new_data = data[drange[0]:drange[1]]
        else:
            print('Some thing wrong with your data range!')
            return
        r = range(wrange[0], wrange[1])
        r1 = range(-wrange[1], -wrange[0])
        for i in range(len(new_data) - 5):
            v1 = new_data[i + 1] - new_data[i]
            v2 = new_data[i + 2] - new_data[i]
            v3 = new_data[i + 3] - new_data[i]
            v4 = new_data[i + 4] - new_data[i]
            if v1 in r or v2 in r or v3 in r or v4 in r:
                if flag == 1:
                    # print('{} {} {}'.format(new_t[i], flag, new_data[i]))
                    down += 1
                flag, count = -1, 0
            elif v1 in r1 or v2 in r1 or v3 in r1 or v4 in r1:
                if flag == -1:
                    # print('{} {} {}'.format(new_t[i], flag, new_data[i]))
                    up += 1
                flag, count = 1, 0
            count += 1
        return up, down

    @staticmethod
    def audio_cue(data, compared_num, drange):
        """sound getting smaller
        :param data_path: strings
        :param compared_num: int, numbers of compared data(countinuous data)
        :param drange: list, data range between time1 and time2
        :return bottom: int, numbers of bottom with countinuous rise
        """
        num = compared_num
        if drange[0] == 0 or drange[1] == 0:
            new_data = data
        elif drange[1] > drange[0]:
            new_data = data[drange[0]:drange[1]]
        else:
            print('Some thing wrong with your data range!')
            return
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
        i = 0
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