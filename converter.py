from __future__ import division

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





'''
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert CSV files')
    parser.add_argument('-s', '--strict', required=False, action='store_true')
    parser.add_argument('--yaml')
    parser.add_argument('--csv')
    args = parser.parse_args()
    ### Ok ###
'''

'''
import sqlite3

n = sqlite3.connect('fbb')
c = n.cursor()

from converter import Config
import yaml
import csv

folder = 'pit_fans'

cfg_yaml = yaml.load(open('./' + folder + '/cfg.yaml', 'rb'))
cfg = Config(cfg_yaml)

c.execute('DELETE FROM ' + folder)
n.commit()

ddl = cfg.sqlite3_ddl(folder)
c.execute(ddl)

insert_sql = cfg.sqlite3_insert(folder)
csv_file_name = './' + folder + '/' + folder + '.csv'
reader = csv.DictReader(open(csv_file_name, 'rb'))
for row in reader:
    new_row = cfg(row)
    c.execute(insert_sql, new_row.values())

n.commit()

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

"""
import sqlite3
from collections import OrderedDict

def unique_key(dct, key):
    if key in dct:
        return unique_key(dct, '_{0}'.format(key))
    else:
        return key

def ordered_dict_factory(cursor, row):
    dct = OrderedDict()
    for i, column_name in enumerate(cursor.description):
        key = unique_key(dct, column_name[0])
        dct[key] = row[i]
    return dct

n = sqlite3.connect('fbb')
n.row_factory = ordered_dict_factory

c = n.cursor()

c.execute('''
  SELECT t.*,
         u.g + v.g g,
         u.ab + v.ab ab,
         u.pa + v.pa pa,
         u.h + v.h h,
         u.b1 + v.b1 b1,
         u.b2 + v.b2 b2,
         u.b3 + v.b3 b3,
         u.hr + v.hr hr,
         u.r + v.r r,
         u.rbi + v.rbi rbi,
         u.bb + v.bb bb,
         u.ibb + v.ibb ibb,
         u.so + v.so so,
         u.hbp + v.hbp hbp,
         u.sf + v.sf sf,
         u.sh + v.sh sh,
         u.gdp + v.gdp gdp,
         u.sb + v.sb sb,
         u.cs + v.cs cs,
         u.gb + v.gb gb,
         u.ld + v.ld ld,
         u.fb + v.fb fb,
         u.iffb + v.iffb iffb,
         u.ifh + v.ifh ifh,
         u.bu + v.bu bu,
         u.buh + v.buh buh,
         u.balls + v.balls balls,
         u.strikes + v.strikes strikes,
         u.pitches + v.pitches pitches,
         u.o_sw_miss + v.o_sw_miss o_sw_miss,
         u.o_sw_cont + v.o_sw_cont o_sw_cont,
         u.o_look + v.o_look o_look,
         u.z_sw_miss + v.z_sw_miss z_sw_miss,
         u.z_sw_cont + v.z_sw_cont z_sw_cont,
         u.z_look + v.z_look z_look
    FROM bat_basic_ext t,
         bat_basic_ext u,
         bat_basic_ext v
   WHERE     1 = 1
         AND t.fg_id = u.fg_id
         AND u.fg_id = v.fg_id
         AND t.year - 1 = u.year
         AND u.year - 1 = v.year
         AND t.pa >= 250
         AND u.pa >= 250
         AND v.pa >= 250
''')

data = c.fetchall()



from scipy.stats.stats import pearsonr
from scipy.special import logit
from math import sqrt, exp


def correlate(x, y):
    # Ensure equal length iterables
    if not len(x) == len(y):
        raise ValueError('Unequal lengths')
    # Initialize values
    n = len(x)
    sx = sum(x)
    sy = sum(y)
    sxx = sum(val**2 for val in x)
    sxy = sum(x_val*y_val for x_val, y_val in zip(x, y))
    det = sxx*n - sx**2
    # Calculate m, b
    m = (sxy*n - sy*sx)/det
    b = (sxx*sy - sx*sxy)/det
    # Calculate r squared
    err = sum((val - sy/n)**2 for val in y)
    res = sum((y_val - m*x_val - b)**2 for x_val, y_val in zip(x, y))
    r = sqrt(1 - res/err)
    # Return parameters and correlation
    return dict(m=m, b=b, r=r)



so = {

    'x': lambda d: (
        d['_so']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d: (
        d['so']
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}


ubb = {

    'x': lambda d: (
        d['_bb'] - d['_ibb']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['bb'] - d['ibb']
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}


gb = {

    'x': lambda d: (
        d['_gb']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['gb']
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}


ld = {

    'x': lambda d: (
        d['_ld']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['ld']
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}


offb = {

    'x': lambda d: (
        d['_fb'] - d['_iffb'] - d['_sf']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['fb'] - d['iffb'] - d['sf']
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}


iffb = {

    'x': lambda d: (
        d['_iffb'] + 0.001
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['iffb'] + 0.001
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

for f in (so, ubb, gb, ld, offb, iffb,):
    c = correlate(map(logit, map(f['x'], data)), map(logit, map(f['y'], data)))
    print u','.join(map(str, [c['m'], c['b'], c['r']]))

print ''



batted = {

    'x': lambda d: (
        d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['gb'] + d['ld'] + d['fb'] - d['sf']
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

for f in (batted,):
    c = correlate(map(logit, map(f['x'], data)), map(logit, map(f['y'], data)))
    print u','.join(map(str, [c['m'], c['b'], c['r']]))

print ''



gb_batted = {

    'x': lambda d: (
        d['_gb']
        ) / (
        d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['gb']
        ) / (
        d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

ld_batted = {

    'x': lambda d: (
        d['_ld']
        ) / (
        d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['ld']
        ) / (
        d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

offb_batted = {

    'x': lambda d: (
        d['_fb'] - d['_sf'] - d['_iffb']
        ) / (
        d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['fb'] - d['sf'] - d['iffb']
        ) / (
        d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

iffb_batted = {

    'x': lambda d: (
        d['_iffb'] + 0.001
        ) / (
        d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['iffb'] + 0.001
        ) / (
        d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

for f in (gb_batted, ld_batted, offb_batted, iffb_batted,):
    c = correlate(map(logit, map(f['x'], data)), map(logit, map(f['y'], data)))
    print u','.join(map(str, [c['m'], c['b'], c['r']]))

print ''



nonbatted = {

    'x': lambda d: (
        d['_so'] + d['_bb'] - d['_ibb']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['so'] + d['bb'] - d['ibb']
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

for f in (nonbatted,):
    c = correlate(map(logit, map(f['x'], data)), map(logit, map(f['y'], data)))
    print u','.join(map(str, [c['m'], c['b'], c['r']]))

print ''



so_nonbatted = {

    'x': lambda d: (
        d['_so']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb']
    ),

    'y': lambda d:  (
        d['so']
        ) / (
        d['so'] + d['bb'] - d['ibb']
    ),

}

ubb_nonbatted = {

    'x': lambda d: (
        d['_bb'] - d['_ibb']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb']
    ),

    'y': lambda d:  (
        d['bb'] - d['ibb']
        ) / (
        d['so'] + d['bb'] - d['ibb']
    ),

}

for f in (so_nonbatted, ubb_nonbatted,):
    c = correlate(map(logit, map(f['x'], data)), map(logit, map(f['y'], data)))
    print u','.join(map(str, [c['m'], c['b'], c['r']]))

print ''



nongb = {

    'x': lambda d: (
        d['_ld'] + d['_fb'] - d['_sf']
        ) / (
        d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['ld'] + d['fb'] - d['sf']
        ) / (
        d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

for f in (nongb,):
    c = correlate(map(logit, map(f['x'], data)), map(logit, map(f['y'], data)))
    print u','.join(map(str, [c['m'], c['b'], c['r']]))

print ''



ld_nongb = {

    'x': lambda d: (
        d['_ld']
        ) / (
        d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['ld']
        ) / (
        d['ld'] + d['fb'] - d['sf']
    ),

}

offb_nongb = {

    'x': lambda d: (
        d['_fb'] - d['_iffb'] - d['_sf']
        ) / (
        d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['fb'] - d['iffb'] - d['sf']
        ) / (
        d['ld'] + d['fb'] - d['sf']
    ),

}

iffb_nongb = {

    'x': lambda d: (
        d['_iffb'] + 0.001
        ) / (
        d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['iffb'] + 0.001
        ) / (
        d['ld'] + d['fb'] - d['sf']
    ),

}


for f in (ld_nongb, offb_nongb, iffb_nongb,):
    c = correlate(map(logit, map(f['x'], data)), map(logit, map(f['y'], data)))
    print u','.join(map(str, [c['m'], c['b'], c['r']]))

print ''



hr_rpa = {

    'x': lambda d: (
        d['_hr']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d: (
        d['hr']
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

hr_batted = {

    'x': lambda d: (
        d['_hr']
        ) / (
        d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['hr']
        ) / (
        d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}


hr_nongb = {

    'x': lambda d: (
        d['_hr']
        ) / (
        d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['hr']
        ) / (
        d['ld'] + d['fb'] - d['sf']
    ),

}

hr_ldoffb = {

    'x': lambda d: (
        d['_hr']
        ) / (
        d['_ld'] + d['_fb'] - d['_sf'] - d['_iffb']
    ),

    'y': lambda d:  (
        d['hr']
        ) / (
        d['ld'] + d['fb'] - d['sf'] - d['iffb']
    ),

}

hr_offb = {

    'x': lambda d: (
        d['_hr']
        ) / (
        d['_fb'] - d['_sf'] - d['_iffb']
    ),

    'y': lambda d:  (
        d['hr']
        ) / (
        d['fb'] - d['sf'] - d['iffb']
    ),

}


for f in (hr_rpa, hr_batted, hr_nongb, hr_ldoffb, hr_offb):
    c = correlate(map(logit, map(f['x'], data)), map(logit, map(f['y'], data)))
    print u','.join(map(str, [c['m'], c['b'], c['r']]))

print ''

batted_cont = {

    'x': lambda d: (
        d['_gb'] + d['_ld'] + d['_fb'] + d['_bu']
        ) / (
        d['_o_sw_cont'] + d['_z_sw_cont']
    ),

    'y': lambda d:  (
        d['gb'] + d['ld'] + d['fb'] + d['bu']
        ) / (
        d['o_sw_cont'] + d['z_sw_cont']
    ),

}

batted_rpa = {

    'x': lambda d: (
        d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
        ) / (
        d['_so'] + d['_bb'] - d['_ibb'] + d['_gb'] + d['_ld'] + d['_fb'] - d['_sf']
    ),

    'y': lambda d:  (
        d['gb'] + d['ld'] + d['fb'] - d['sf']
        ) / (
        d['so'] + d['bb'] - d['ibb'] + d['gb'] + d['ld'] + d['fb'] - d['sf']
    ),

}

for f in (batted_cont, batted_rpa):
    c = correlate(map(logit, map(f['x'], data)), map(logit, map(f['y'], data)))
    print u','.join(map(str, [c['m'], c['b'], c['r']]))

print ''
"""
