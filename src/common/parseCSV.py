
import csv


class ParseCSV(object):
    """docstring for ParseCSV"""

    def __init__(self, path):
        self.path = path

    def get_row(self, key):
        d = {}
        with open(self.path, 'r') as cf:
            for row in csv.DictReader(cf):
                if key in row['action']:
                    d['power_button_press'] = row['power_button_press']
                    d['time_wait'] = int(row['time_wait'])
                    d['audio_cue'] = row['audio_cue']
                    d['led1'] = row['led1']
                    break
        return d
