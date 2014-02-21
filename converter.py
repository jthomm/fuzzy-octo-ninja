import yaml
from collections import OrderedDict



class FieldConverter(object):

    def __init__(self, config):
        self.config = config

    @property
    def header(self):
        return self.config['header']

    @property
    def name(self):
        return self.config.get('name', self.config['header'].lower())

    @property
    def none_value(self):
        return self.config.get('none', '')

    @property
    def type_converter(self):
        if 'type' not in self.config:
            return unicode
        elif self.config['type'] == 'str':
            return str
        elif self.config['type'] == 'int':
            return int
        elif self.config['type'] == 'float':
            return float
        else:
            return unicode

    def __call__(self, value):
        new_value = self.type_converter(value)
        return None if new_value == self.none_value else new_value



DATA_TYPES = {'unicode': unicode,
              'str': str,
              'int': int,
              'float': float,}

SQLITE3_TYPES = {'unicode': 'TEXT',
                 'str': 'TEXT',
                 'int': 'INTEGER',
                 'float': 'REAL',}



class FieldConfig(object):

    def __init__(self, config):
        self.config = config

    @property
    def header(self):
        return self.config['header']

    @property
    def name(self):
        return self.config.get('name', self.header.lower())

    @property
    def none(self):
        return self.config.get('none', '')

    @property
    def default(self):
        return self.config.get('default', None)

    @property
    def type_str(self):
        return self.config.get('type', 'unicode')

    @property
    def data_type(self):
        return DATA_TYPES[self.type_str]

    @property
    def rstrip(self):
        return self.config.get('rstrip', None)

    @property
    def sqlite3_type(self):
        return SQLITE3_TYPES[self.type_str]

    @property
    def sqlite3_field_declaration(self):
        return u'{0} {1}'.format(self.name, self.sqlite3_type)

    def __call__(self, value):
        if value == self.none:
            return None
        else:
            if value is None:
                value = self.default
            if self.rstrip is not None:
                value = value.rstrip(self.rstrip)
            return self.data_type(value)



class Config(object):

    def __init__(self, config):
        self.field_configs = map(FieldConfig, config)

    def get(self, header):
        for cfg in self.field_configs:
            if cfg.header == header:
                return cfg
        raise Exception('No such header: {0}'.format(header))

    def sqlite3_ddl(self, table_name):
        field_declarations = u', '.join([fc.sqlite3_field_declaration \
                                         for fc in self.field_configs])
        return u'CREATE TABLE {0} ({1})'.format(table_name, field_declarations)

    def sqlite3_insert(self, table_name):
        question_marks = u', '.join([u'?']*len(self.field_configs))
        return u'INSERT INTO {0} VALUES ({1})'.format(table_name, question_marks)

    def __call__(self, dct):
        new_dct = OrderedDict()
        for cfg in self.field_configs:
            new_dct[cfg.name] = cfg(dct.get(cfg.header, None))
        return new_dct






if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert CSV files')
    parser.add_argument('-s', '--strict', required=False, action='store_true')
    parser.add_argument('--yaml')
    parser.add_argument('--csv')
    args = parser.parse_args()
    ### Ok ###

'''
import sqlite3

n = sqlite3.connect('fbb')
c = n.cursor()

from converter import Config
import yaml
import csv

folder = 'pit_pfx'

cfg_yaml = yaml.load(open('./' + folder + '/cfg.yaml', 'rb'))
cfg = Config(cfg_yaml)
ddl = cfg.sqlite3_ddl(folder)
c.execute(ddl)

for year in range(2007, 2014):
    cfg_yaml = yaml.load(open('./' + folder + '/cfg.yaml', 'rb'))
    cfg_yaml[0]['default'] = year
    cfg = Config(cfg_yaml)
    insert_sql = cfg.sqlite3_insert(folder)
    csv_file_name = './' + folder + '/' + str(year) + '.csv'
    reader = csv.DictReader(open(csv_file_name, 'rb'))
    for row in reader:
        new_row = cfg(row)
        _ = c.execute(insert_sql, new_row.values())
    n.commit()


cfg_yaml = yaml.load(open('./cor/cfg.yaml', 'rb'))
cfg = Config(cfg_yaml)
ddl = cfg.sqlite3_ddl('cor')
c.execute(ddl)

for side in ('pit', 'bat',):
    cfg_yaml = yaml.load(open('./cor/cfg.yaml', 'rb'))
    cfg_yaml[0]['default'] = side
    cfg = Config(cfg_yaml)
    insert_sql = cfg.sqlite3_insert('cor')
    csv_file_name = './cor/' + side + '_cor.csv'
    reader = csv.DictReader(open(csv_file_name, 'rb'))
    for row in reader:
        new_row = cfg(row)
        _ = c.execute(insert_sql, new_row.values())
    n.commit()


'''


