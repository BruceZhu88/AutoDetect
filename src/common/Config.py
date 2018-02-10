import configparser


class Config(object):
    def __init__(self, file):
        self.file = file
        self.cfg = configparser.ConfigParser()

    def cfg_load(self):
        self.cfg.read(self.file)

    def cfg_dump(self):
        values = []
        se_list = self.get_section()
        for se in se_list:
            values.append(self.cfg.items(se))
        return values

    def get_section(self):
        return self.cfg.sections()

    def get_sections(self):
        return self.cfg._sections

    def delete_item(self, se, key):
        self.cfg.remove_option(se, key)

    def delete_section(self, se):
        self.cfg.remove_section(se)

    def add_section(self, se):
        sections = self.get_section()
        for s in sections:
            if s == se:
                return
        self.cfg.add_section(se)

    def set_item(self, se, key, value):
        self.cfg.set(se, key, value)

    def save(self):
        fd = open(self.file, 'w')
        self.cfg.write(fd)
        fd.close()

    def print_values(self):
        print('*' * 100)
        se_list = self.get_section()
        for sec in self.cfg:
            for value in self.cfg[sec]:
                print(sec + "." + value + " = " + self.cfg[sec][value])
        print('*' * 100)

    def set_items(self, data):
        for v in data.keys():
            for sec in self.cfg:
                if v in self.cfg[sec]:
                    self.set_item(sec, v, str(data[v]))