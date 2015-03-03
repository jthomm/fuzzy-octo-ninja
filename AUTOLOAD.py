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


"""
  CREATE VIEW v_mrcs80_stmr20 AS
  SELECT t.fg_id AS fg_id,
         0.2*t.pa + 0.8*u.pa AS pa,
         0.2*t.ab/t.pa + 0.8*u.ab/u.pa AS ab_pa,
         0.2*t.h/t.pa + 0.8*u.h/u.pa AS h_pa,
         0.2*t.b2/t.pa + 0.8*u.b2/u.pa AS b2_pa,
         0.2*t.b3/t.pa + 0.8*u.b3/u.pa AS b3_pa,
         0.2*t.hr/t.pa + 0.8*u.hr/u.pa AS hr_pa,
         0.2*t.r/t.pa + 0.8*u.r/u.pa AS r_pa,
         0.2*t.rbi/t.pa + 0.8*u.rbi/u.pa AS rbi_pa,
         0.2*t.bb/t.pa + 0.8*u.bb/u.pa AS bb_pa,
         0.2*t.so/t.pa + 0.8*u.so/u.pa AS so_pa,
         0.2*t.sb/t.pa + 0.8*u.sb/u.pa AS sb_pa
    FROM bat_stmr t,
         bat_mrcs u
   WHERE t.fg_id = u.fg_id
;


  CREATE VIEW v_stmr65_zips35 AS
  SELECT t.fg_id AS fg_id,
         0.1*t.pa + 0.9*u.pa AS pa,
         0.35*t.ab/t.pa + 0.65*u.ab/u.pa AS ab_pa,
         0.35*t.h/t.pa + 0.65*u.h/u.pa AS h_pa,
         0.35*t.b2/t.pa + 0.65*u.b2/u.pa AS b2_pa,
         0.35*t.b3/t.pa + 0.65*u.b3/u.pa AS b3_pa,
         0.35*t.hr/t.pa + 0.65*u.hr/u.pa AS hr_pa,
         0.35*t.r/t.pa + 0.65*u.r/u.pa AS r_pa,
         0.35*t.rbi/t.pa + 0.65*u.rbi/u.pa AS rbi_pa,
         0.35*t.bb/t.pa + 0.65*u.bb/u.pa AS bb_pa,
         0.35*t.so/t.pa + 0.65*u.so/u.pa AS so_pa,
         0.35*t.sb/t.pa + 0.65*u.sb/u.pa AS sb_pa
    FROM bat_zips t,
         bat_stmr u
   WHERE t.fg_id = u.fg_id
;


  SELECT fg_id,
         pa,
         pa*ab_pa AS ab,
         pa*h_pa AS h,
         pa*b2_pa AS b2,
         pa*b3_pa AS b3,
         pa*hr_pa AS hr,
         pa*r_pa AS r,
         pa*rbi_pa AS rbi,
         pa*bb_pa AS bb,
         pa*so_pa AS so,
         pa*sb_pa AS sb
    FROM (
  SELECT IFNULL (t_fg_id, u_fg_id) AS fg_id,
         IFNULL (t_pa, u_pa) AS pa,
         IFNULL (t_ab_pa, u_ab_pa) AS ab_pa,
         IFNULL (t_h_pa, u_h_pa) AS h_pa,
         IFNULL (t_b2_pa, u_b2_pa) AS b2_pa,
         IFNULL (t_b3_pa, u_b3_pa) AS b3_pa,
         IFNULL (t_hr_pa, u_hr_pa) AS hr_pa,
         IFNULL (t_r_pa, u_r_pa) AS r_pa,
         IFNULL (t_rbi_pa, u_rbi_pa) AS rbi_pa,
         IFNULL (t_bb_pa, u_bb_pa) AS bb_pa,
         IFNULL (t_so_pa, u_so_pa) AS so_pa,
         IFNULL (t_sb_pa, u_sb_pa) AS sb_pa
    FROM (
  SELECT t.fg_id AS t_fg_id,
         t.pa AS t_pa,
         t.ab_pa AS t_ab_pa,
         t.h_pa AS t_h_pa,
         t.b2_pa AS t_b2_pa,
         t.b3_pa AS t_b3_pa,
         t.hr_pa AS t_hr_pa,
         t.r_pa AS t_r_pa,
         t.rbi_pa AS t_rbi_pa,
         t.bb_pa AS t_bb_pa,
         t.so_pa AS t_so_pa,
         t.sb_pa AS t_sb_pa,
         u.fg_id AS u_fg_id,
         u.pa AS u_pa,
         u.ab_pa AS u_ab_pa,
         u.h_pa AS u_h_pa,
         u.b2_pa AS u_b2_pa,
         u.b3_pa AS u_b3_pa,
         u.hr_pa AS u_hr_pa,
         u.r_pa AS u_r_pa,
         u.rbi_pa AS u_rbi_pa,
         u.bb_pa AS u_bb_pa,
         u.so_pa AS u_so_pa,
         u.sb_pa AS u_sb_pa
    FROM v_mrcs80_stmr20 t
    LEFT
   OUTER
    JOIN v_stmr65_zips35 u
      ON t.fg_id = u.fg_id
   UNION
     ALL
  SELECT t.fg_id AS t_fg_id,
         t.pa AS t_pa,
         t.ab_pa AS t_ab_pa,
         t.h_pa AS t_h_pa,
         t.b2_pa AS t_b2_pa,
         t.b3_pa AS t_b3_pa,
         t.hr_pa AS t_hr_pa,
         t.r_pa AS t_r_pa,
         t.rbi_pa AS t_rbi_pa,
         t.bb_pa AS t_bb_pa,
         t.so_pa AS t_so_pa,
         t.sb_pa AS t_sb_pa,
         u.fg_id AS u_fg_id,
         u.pa AS u_pa,
         u.ab_pa AS u_ab_pa,
         u.h_pa AS u_h_pa,
         u.b2_pa AS u_b2_pa,
         u.b3_pa AS u_b3_pa,
         u.hr_pa AS u_hr_pa,
         u.r_pa AS u_r_pa,
         u.rbi_pa AS u_rbi_pa,
         u.bb_pa AS u_bb_pa,
         u.so_pa AS u_so_pa,
         u.sb_pa AS u_sb_pa
    FROM v_stmr65_zips35 u
    LEFT
   OUTER
    JOIN v_mrcs80_stmr20 t
      ON u.fg_id = t.fg_id
   WHERE t.fg_id IS NULL
         )
         )
;
"""
