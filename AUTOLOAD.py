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
  CREATE VIEW v_bat_mrcs80_stmr20 AS
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


  CREATE VIEW v_bat_stmr65_zips35 AS
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

  CREATE VIEW v_pit_mrcs80_stmr20 AS
  SELECT t.fg_id AS fg_id,
         0.2*t.ip + 0.8*u.ip AS ip,
         0.2*t.w/t.ip + 0.8*u.w/u.ip AS w_ip,
         0.2*t.sv/t.ip + 0.8*u.sv/u.ip AS sv_ip,
         0.2*t.h/t.ip + 0.8*u.h/u.ip AS h_ip,
         0.2*t.so/t.ip + 0.8*u.so/u.ip AS so_ip,
         0.2*t.bb/t.ip + 0.8*u.bb/u.ip AS bb_ip,
         0.2*t.er/t.ip + 0.8*u.er/u.ip AS er_ip
    FROM pit_stmr t,
         pit_mrcs u
   WHERE t.fg_id = u.fg_id
     AND t.ip > 1
;

  CREATE VIEW v_pit_stmr65_zips35 AS
  SELECT t.fg_id AS fg_id,
         0.1*t.ip + 0.9*u.ip AS ip,
         0.35*t.w/t.ip + 0.65*u.w/u.ip AS w_ip,
         1.0*u.sv/u.ip AS sv_ip,
         0.35*t.h/t.ip + 0.65*u.h/u.ip AS h_ip,
         0.35*t.so/t.ip + 0.65*u.so/u.ip AS so_ip,
         0.35*t.bb/t.ip + 0.65*u.bb/u.ip AS bb_ip,
         0.35*t.er/t.ip + 0.65*u.er/u.ip AS er_ip
    FROM pit_zips t,
         pit_stmr u
   WHERE t.fg_id = u.fg_id
     AND u.ip > 1
;



  CREATE VIEW v_pit_mrcs_stmr_zips AS
  SELECT fg_id,
         ip,
         ip*w_ip AS w,
         ip*sv_ip AS sv,
         ip*h_ip AS h,
         ip*so_ip AS so,
         ip*bb_ip AS bb,
         ip*er_ip AS er
    FROM (
  SELECT IFNULL (t_fg_id, u_fg_id) AS fg_id,
         IFNULL (t_ip, u_ip) AS ip,
         IFNULL (t_w_ip, u_w_ip) AS w_ip,
         IFNULL (t_sv_ip, u_sv_ip) AS sv_ip,
         IFNULL (t_h_ip, u_h_ip) AS h_ip,
         IFNULL (t_so_ip, u_so_ip) AS so_ip,
         IFNULL (t_bb_ip, u_bb_ip) AS bb_ip,
         IFNULL (t_er_ip, u_er_ip) AS er_ip
    FROM (
  SELECT t.fg_id AS t_fg_id,
         t.ip AS t_ip,
         t.w_ip AS t_w_ip,
         t.sv_ip AS t_sv_ip,
         t.h_ip AS t_h_ip,
         t.so_ip AS t_so_ip,
         t.bb_ip AS t_bb_ip,
         t.er_ip AS t_er_ip,
         u.fg_id AS u_fg_id,
         u.ip AS u_ip,
         u.w_ip AS u_w_ip,
         u.sv_ip AS u_sv_ip,
         u.h_ip AS u_h_ip,
         u.so_ip AS u_so_ip,
         u.bb_ip AS u_bb_ip,
         u.er_ip AS u_er_ip
    FROM v_pit_mrcs80_stmr20 t
    LEFT
   OUTER
    JOIN v_pit_stmr65_zips35 u
      ON t.fg_id = u.fg_id
   UNION
     ALL
  SELECT t.fg_id AS t_fg_id,
         t.ip AS t_ip,
         t.w_ip AS t_w_ip,
         t.sv_ip AS t_sv_ip,
         t.h_ip AS t_h_ip,
         t.so_ip AS t_so_ip,
         t.bb_ip AS t_bb_ip,
         t.er_ip AS t_er_ip,
         u.fg_id AS u_fg_id,
         u.ip AS u_ip,
         u.w_ip AS u_w_ip,
         u.sv_ip AS u_sv_ip,
         u.h_ip AS u_h_ip,
         u.so_ip AS u_so_ip,
         u.bb_ip AS u_bb_ip,
         u.er_ip AS u_er_ip
    FROM v_pit_stmr65_zips35 u
    LEFT
   OUTER
    JOIN v_pit_mrcs80_stmr20 t
      ON u.fg_id = t.fg_id
   WHERE t.fg_id IS NULL
         )
         )
;

  CREATE VIEW v_bat_mrcs_stmr_zips AS
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
    FROM v_bat_mrcs80_stmr20 t
    LEFT
   OUTER
    JOIN v_bat_stmr65_zips35 u
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
    FROM v_bat_stmr65_zips35 u
    LEFT
   OUTER
    JOIN v_bat_mrcs80_stmr20 t
      ON u.fg_id = t.fg_id
   WHERE t.fg_id IS NULL
         )
         )
;



  SELECT t.fg_id AS fg_id,
         u.fg_name AS fg_name,
         u.yh_pos AS yh_pos,
         -0.0044*t.ab + 0.0157*t.h + 0.0123*t.r + 0.0218*t.hr + 0.0093*t.rbi + 0.0165*t.sb - 2.0477 AS value
    FROM v_bat_mrcs_stmr_zips t,
         id_map u
   WHERE t.fg_id = u.fg_id
   UNION
     ALL
  SELECT t.fg_id AS fg_id,
         u.fg_name AS fg_name,
         u.yh_pos AS yh_pos,
         0.0376*t.w + 0.0130*t.sv + 0.0036*t.so + 0.0188*t.ip - 0.0110*(t.bb + t.h) - 0.0200*t.er - 0.9874 AS value
    FROM v_pit_mrcs_stmr_zips t,
         id_map u
   WHERE t.fg_id = u.fg_id
"""
