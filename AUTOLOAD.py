import sqlite3

from converter import Config
import yaml
import csv

n = sqlite3.connect('fbb')
c = n.cursor()

def load_data(folder, years=None):
    if years is None:
        # delete any preexisting data
        delete_sql = u'DELETE FROM {0}'.format(folder)
        c.execute(delete_sql)
        n.commit()
        # load the config
        cfg_yaml = yaml.load(open(u'./{0}/cfg.yaml'.format(folder), 'rb'))
        cfg = Config(cfg_yaml)
        # insert new data
        insert_sql = cfg.sqlite3_insert(folder)
        csv_file_name = u'./{0}/{0}.csv'.format(folder)
        reader = csv.DictReader(open(csv_file_name, 'rb'))
        for row in reader:
            new_row = cfg(row)
            try:
                ___ = c.execute(insert_sql, new_row.values())
            except sqlite3.IntegrityError:
                print new_row
                raise
        n.commit()
    else:
        for year in years:
            # delete any preexisting data for the year
            delete_sql = u'DELETE FROM {0} WHERE year = {1}'.format(folder, year)
            c.execute(delete_sql)
            n.commit()
            # load the config
            cfg_yaml = yaml.load(open(u'./{0}/cfg.yaml'.format(folder), 'rb'))
            cfg_yaml[0]['default'] = year
            cfg = Config(cfg_yaml)
            # insert new data for the year
            insert_sql = cfg.sqlite3_insert(folder)
            csv_file_name = u'./{0}/{1}.csv'.format(folder, year)
            reader = csv.DictReader(open(csv_file_name, 'rb'))
            for row in reader:
                new_row = cfg(row)
                try:
                    ___ = c.execute(insert_sql, new_row.values())
                except sqlite3.IntegrityError:
                    print new_row
                    raise
            n.commit()

def create_table(folder):
    cfg_yaml = yaml.load(open(u'./{0}/cfg.yaml'.format(folder), 'rb'))
    cfg = Config(cfg_yaml)
    ddl = cfg.sqlite3_ddl(folder)
    c.execute(ddl)


folders = (
    'pit_basic',
    'pit_pfx',
    'bat_basic',
    'bat_pfx',
)

for folder in folders:
    print 'refreshing {0} for 2014'.format(folder)
    load_data(folder, range(2014, 2015))
