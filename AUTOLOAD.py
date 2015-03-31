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



  CREATE VIEW v_mrcs_stmr_zips AS
  SELECT t.fg_id AS fg_id,
         u.fg_name AS fg_name,
         u.yh_pos AS yh_pos,
         -0.00419*t.ab + 0.01517*t.h + 0.01224*t.r + 0.02187*t.hr + 0.00929*t.rbi + 0.01701*t.sb - 2.08361 AS value
    FROM v_bat_mrcs_stmr_zips t,
         id_map u
   WHERE t.fg_id = u.fg_id
   UNION
     ALL
  SELECT t.fg_id AS fg_id,
         u.fg_name AS fg_name,
         u.yh_pos AS yh_pos,
         0.03909*t.w + 0.01335*t.sv + 0.00367*t.so + 0.01993*t.ip - 0.01132*(t.bb + t.h) - 0.02011*t.er - 0.98791 AS value
    FROM v_pit_mrcs_stmr_zips t,
         id_map u
   WHERE t.fg_id = u.fg_id
;



  SELECT *
    FROM (
  SELECT IFNULL (v.orank, (SELECT MAX (orank) FROM (SELECT * FROM bat_yhoo UNION ALL SELECT * FROM pit_yhoo))) AS orank,
         t.fg_name,
         t.yh_pos,
         ROUND (100*t.value, 0) + 225 AS val
    FROM v_mrcs_stmr_zips t
    LEFT
    JOIN id_map u
      ON t.fg_id = u.fg_id
    LEFT
    JOIN (SELECT * FROM bat_yhoo UNION ALL SELECT * FROM pit_yhoo) v
      ON u.yh_id = v.yh_id
         )
ORDER BY orank, val DESC
;





  CREATE VIEW v_bat_sreg_pa AS
  SELECT t.fg_id,
         1.0*u.g/t.pa g,
         t.pa pa,
         1.0*v.ab/v.pa ab,
         1.0*(v.h - v.b2 - v.b3 - v.hr)/v.pa b1,
         1.0*v.b2/v.pa b2,
         1.0*v.b3/v.pa b3,
         1.0*v.hr/v.pa hr,
         1.0*v.r/v.pa r,
         1.0*v.rbi/v.pa rbi,
         1.0*v.bb/v.pa bb,
         1.0*v.so/v.pa so,
         1.0*v.sb/v.pa sb,
         1.0*v.cs/v.pa cs
    FROM bat_stmr t,
         bat_fgdc u,
         bat_sreg v
   WHERE t.fg_id = u.fg_id
     AND t.fg_id = v.fg_id
     AND t.pa > 1
;

  CREATE VIEW v_bat_stmr_pa AS
  SELECT t.fg_id,
         1.0*u.g/t.pa g,
         t.pa pa,
         1.0*t.ab/t.pa ab,
         1.0*(t.h - t.b2 - t.b3 - t.hr)/t.pa b1,
         1.0*t.b2/t.pa b2,
         1.0*t.b3/t.pa b3,
         1.0*t.hr/t.pa hr,
         1.0*t.r/t.pa r,
         1.0*t.rbi/t.pa rbi,
         1.0*t.bb/t.pa bb,
         1.0*t.so/t.pa so,
         1.0*t.sb/t.pa sb,
         1.0*t.cs/t.pa cs
    FROM bat_stmr t,
         bat_fgdc u
   WHERE t.fg_id = u.fg_id
     AND t.pa > 1
;

  CREATE VIEW v_bat_clay_pa AS
  SELECT u.fg_id,
         NULL g,
         t.pa pa,
         1.0*t.ab/t.pa ab,
         1.0*(t.h - t.b2 - t.b3 - t.hr)/t.pa b1,
         1.0*t.b2/t.pa b2,
         1.0*t.b3/t.pa b3,
         1.0*t.hr/t.pa hr,
         1.0*t.r/t.pa r,
         1.0*t.rbi/t.pa rbi,
         1.0*t.bb/t.pa bb,
         1.0*t.so/t.pa so,
         1.0*t.sb/t.pa sb,
         1.0*t.cs/t.pa cs
    FROM bat_clay t,
         id_map u
   WHERE t.howe_id = u.howe_id
;

  CREATE VIEW v_bat_zips_pa AS
  SELECT t.fg_id,
         1.0*t.g/t.pa g,
         t.pa pa,
         1.0*t.ab/t.pa ab,
         1.0*(t.h - t.b2 - t.b3 - t.hr)/t.pa b1,
         1.0*t.b2/t.pa b2,
         1.0*t.b3/t.pa b3,
         1.0*t.hr/t.pa hr,
         1.0*t.r/t.pa r,
         1.0*t.rbi/t.pa rbi,
         1.0*t.bb/t.pa bb,
         1.0*t.so/t.pa so,
         1.0*t.sb/t.pa sb,
         1.0*t.cs/t.pa cs
    FROM bat_zips t
;

  CREATE VIEW v_bat_cairo_pa AS
  SELECT u.fg_id,
         1.0*t.g/t.pa g,
         t.pa pa,
         1.0*t.ab/t.pa ab,
         1.0*(t.h - t.b2 - t.b3 - t.hr)/t.pa b1,
         1.0*t.b2/t.pa b2,
         1.0*t.b3/t.pa b3,
         1.0*t.hr/t.pa hr,
         1.0*t.r/t.pa r,
         1.0*t.rbi/t.pa rbi,
         1.0*t.bb/t.pa bb,
         1.0*t.so/t.pa so,
         1.0*t.sb/t.pa sb,
         1.0*t.cs/t.pa cs
    FROM bat_cairo t,
         id_map u
   WHERE t.mlb_id = u.mlb_id
;

  CREATE VIEW v_bat_razz_pa AS
  SELECT t.fg_id,
         1.0*t.g/t.pa g,
         t.pa pa,
         1.0*t.ab/t.pa ab,
         1.0*(t.h - t.b2 - t.b3 - t.hr)/t.pa b1,
         1.0*t.b2/t.pa b2,
         1.0*t.b3/t.pa b3,
         1.0*t.hr/t.pa hr,
         1.0*t.r/t.pa r,
         1.0*t.rbi/t.pa rbi,
         1.0*t.bb/t.pa bb,
         1.0*t.so/t.pa so,
         1.0*t.sb/t.pa sb,
         1.0*t.cs/t.pa cs
    FROM bat_razz t
;

  CREATE VIEW v_bat_composite_pa AS
  SELECT t.fg_id AS fg_id,
         (  IFNULL (t.g, 0)
          + IFNULL (u.g, 0)
          + IFNULL (v.g, 0)
          + IFNULL (w.g, 0)
          + IFNULL (x.g, 0)) /
         (  CASE WHEN t.g IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.g IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.g IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.g IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.g IS NULL THEN 0 ELSE 1 END) AS g,
         (  IFNULL (t.pa, 0)
          + 0.5*IFNULL (u.pa, 0)
          + 1.2*IFNULL (v.pa, 0)
          + IFNULL (w.pa, 0)
          + 0.2*IFNULL (x.pa, 0)) /
         (  CASE WHEN t.pa IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.pa IS NULL THEN 0 ELSE 0.5 END
          + CASE WHEN v.pa IS NULL THEN 0 ELSE 1.2 END
          + CASE WHEN w.pa IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.pa IS NULL THEN 0 ELSE 0.2 END) AS pa,
         (  IFNULL (t.ab, 0)
          + IFNULL (u.ab, 0)
          + IFNULL (v.ab, 0)
          + IFNULL (w.ab, 0)
          + IFNULL (x.ab, 0)) /
         (  CASE WHEN t.ab IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.ab IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.ab IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.ab IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.ab IS NULL THEN 0 ELSE 1 END) AS ab,
         (  IFNULL (t.b1, 0)
          + IFNULL (u.b1, 0)
          + IFNULL (v.b1, 0)
          + IFNULL (w.b1, 0)
          + IFNULL (x.b1, 0)) /
         (  CASE WHEN t.b1 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.b1 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.b1 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.b1 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.b1 IS NULL THEN 0 ELSE 1 END) AS b1,
         (  IFNULL (t.b2, 0)
          + IFNULL (u.b2, 0)
          + IFNULL (v.b2, 0)
          + IFNULL (w.b2, 0)
          + IFNULL (x.b2, 0)) /
         (  CASE WHEN t.b2 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.b2 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.b2 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.b2 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.b2 IS NULL THEN 0 ELSE 1 END) AS b2,
         (  IFNULL (t.b3, 0)
          + IFNULL (u.b3, 0)
          + IFNULL (v.b3, 0)
          + IFNULL (w.b3, 0)
          + IFNULL (x.b3, 0)) /
         (  CASE WHEN t.b3 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.b3 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.b3 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.b3 IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.b3 IS NULL THEN 0 ELSE 1 END) AS b3,
         (  IFNULL (t.hr, 0)
          + IFNULL (u.hr, 0)
          + IFNULL (v.hr, 0)
          + IFNULL (w.hr, 0)
          + IFNULL (x.hr, 0)) /
         (  CASE WHEN t.hr IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.hr IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.hr IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.hr IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.hr IS NULL THEN 0 ELSE 1 END) AS hr,
         (  IFNULL (t.r, 0)
          + IFNULL (u.r, 0)
          + IFNULL (v.r, 0)
          + IFNULL (w.r, 0)
          + IFNULL (x.r, 0)) /
         (  CASE WHEN t.r IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.r IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.r IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.r IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.r IS NULL THEN 0 ELSE 1 END) AS r,
         (  IFNULL (t.rbi, 0)
          + IFNULL (u.rbi, 0)
          + IFNULL (v.rbi, 0)
          + IFNULL (w.rbi, 0)
          + IFNULL (x.rbi, 0)) /
         (  CASE WHEN t.rbi IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.rbi IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.rbi IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.rbi IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.rbi IS NULL THEN 0 ELSE 1 END) AS rbi,
         (  IFNULL (t.bb, 0)
          + IFNULL (u.bb, 0)
          + IFNULL (v.bb, 0)
          + IFNULL (w.bb, 0)
          + IFNULL (x.bb, 0)) /
         (  CASE WHEN t.bb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.bb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.bb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.bb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.bb IS NULL THEN 0 ELSE 1 END) AS bb,
         (  IFNULL (t.so, 0)
          + IFNULL (u.so, 0)
          + IFNULL (v.so, 0)
          + IFNULL (w.so, 0)
          + IFNULL (x.so, 0)) /
         (  CASE WHEN t.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.so IS NULL THEN 0 ELSE 1 END) AS so,
         (  IFNULL (t.so, 0)
          + IFNULL (u.so, 0)
          + IFNULL (v.so, 0)
          + IFNULL (w.so, 0)
          + IFNULL (x.so, 0)) /
         (  CASE WHEN t.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.so IS NULL THEN 0 ELSE 1 END) AS so,
         (  IFNULL (t.sb, 0)
          + IFNULL (u.sb, 0)
          + IFNULL (v.sb, 0)
          + IFNULL (w.sb, 0)
          + IFNULL (x.sb, 0)) /
         (  CASE WHEN t.sb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.sb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.sb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.sb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.sb IS NULL THEN 0 ELSE 1 END) AS sb,
         (  IFNULL (t.cs, 0)
          + IFNULL (u.cs, 0)
          + IFNULL (v.cs, 0)
          + IFNULL (w.cs, 0)
          + IFNULL (x.cs, 0)) /
         (  CASE WHEN t.cs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.cs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.cs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.cs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.cs IS NULL THEN 0 ELSE 1 END) AS cs,
            CASE WHEN t.so IS NOT NULL THEN ',STMR' ELSE '' END
         || CASE WHEN u.so IS NOT NULL THEN ',ZIPS' ELSE '' END
         || CASE WHEN v.so IS NOT NULL THEN ',RAZZ' ELSE '' END
         || CASE WHEN w.so IS NOT NULL THEN ',CLAY' ELSE '' END
         || CASE WHEN x.so IS NOT NULL THEN ',CAIR' ELSE '' END AS mix
    FROM v_bat_sreg_pa t
    LEFT
    JOIN v_bat_zips_pa u
      ON t.fg_id = u.fg_id
    LEFT
    JOIN v_bat_razz_pa v
      ON t.fg_id = v.fg_id
    LEFT
    JOIN v_bat_clay_pa w
      ON t.fg_id = w.fg_id
    LEFT
    JOIN v_bat_cairo_pa x
      ON t.fg_id = x.fg_id
   WHERE t.fg_id IS NOT NULL --steamer is present (always true)
     AND u.fg_id IS NOT NULL --zpas is present (almost always true)
;

  CREATE VIEW v_bat_composite AS
  SELECT t.fg_id fg_id,
         u.fg_last fg_last,
         u.fg_first fg_first,
         IFNULL (v.pa, t.pa)*t.g g,
         IFNULL (v.pa, t.pa) pa,
         IFNULL (v.pa, t.pa)*t.ab ab,
         IFNULL (v.pa, t.pa)*t.b1 b1,
         IFNULL (v.pa, t.pa)*t.b2 b2,
         IFNULL (v.pa, t.pa)*t.b3 b3,
         IFNULL (v.pa, t.pa)*t.hr hr,
         IFNULL (v.pa, t.pa)*t.r r,
         IFNULL (v.pa, t.pa)*t.rbi rbi,
         IFNULL (v.pa, t.pa)*t.bb bb,
         IFNULL (v.pa, t.pa)*t.so so,
         IFNULL (v.pa, t.pa)*t.sb sb,
         IFNULL (v.pa, t.pa)*t.cs cs
    FROM v_bat_composite_pa t,
         id_map u
    LEFT
    JOIN bat_overrides v
      ON t.fg_id = v.fg_id
   WHERE t.fg_id = u.fg_id
;







  CREATE VIEW v_pit_stmr_ip AS
  SELECT t.fg_id,
         1.0*t.g/t.ip g,
         1.0*t.gs/t.ip gs,
         t.ip ip,
         1.0*t.h/t.ip h,
         1.0*t.er/t.ip er,
         1.0*t.bb/t.ip bb,
         1.0*t.so/t.ip so,
         1.0*t.hr/t.ip hr,
         1.0*t.w/t.ip w,
         1.0*t.l/t.ip l,
         1.0*t.sv/t.ip sv,
         NULL bsv,
         NULL hld,
         NULL qs
    FROM pit_stmr t
   WHERE t.ip > 1
;

  CREATE VIEW v_pit_sreg_ip AS
  SELECT t.fg_id,
         1.0*t.g/t.ip g,
         1.0*t.gs/t.ip gs,
         t.ip ip,
         1.0*u.h/u.ip h,
         1.0*u.er/u.ip er,
         1.0*u.bb/u.ip bb,
         1.0*u.so/u.ip so,
         1.0*u.hr/u.ip hr,
         1.0*u.w/u.ip w,
         1.0*u.l/u.ip l,
         1.0*u.sv/u.ip sv,
         NULL bsv,
         NULL hld,
         NULL qs
    FROM pit_stmr t,
         pit_sreg u
   WHERE t.fg_id = u.fg_id
     AND t.ip > 1
;

  CREATE VIEW v_pit_zips_ip AS
  SELECT t.fg_id,
         1.0*t.g/t.ip g,
         1.0*t.gs/t.ip gs,
         t.ip ip,
         1.0*t.h/t.ip h,
         1.0*t.er/t.ip er,
         1.0*t.bb/t.ip bb,
         1.0*t.so/t.ip so,
         1.0*t.hr/t.ip hr,
         1.0*t.w/t.ip w,
         1.0*t.l/t.ip l,
         NULL sv,
         NULL bsv,
         NULL hld,
         NULL qs
    FROM pit_zips t
;

  CREATE VIEW v_pit_clay_ip AS
  SELECT u.fg_id,
         1.0*t.g/t.ip g,
         1.0*t.gs/t.ip gs,
         t.ip ip,
         1.0*t.h/t.ip h,
         1.0*t.er/t.ip er,
         1.0*t.bb/t.ip bb,
         1.0*t.so/t.ip so,
         1.0*t.hr/t.ip hr,
         1.0*t.w/t.ip w,
         1.0*t.l/t.ip l,
         1.0*t.sv/t.ip sv,
         NULL bsv,
         NULL hld,
         NULL qs
    FROM pit_clay t,
         id_map u
   WHERE t.howe_id = u.howe_id
;

  CREATE VIEW v_pit_cairo_ip AS
  SELECT u.fg_id,
         1.0*t.g/t.ip g,
         1.0*t.gs/t.ip gs,
         t.ip ip,
         1.0*t.h/t.ip h,
         1.0*t.er/t.ip er,
         1.0*t.bb/t.ip bb,
         1.0*t.so/t.ip so,
         1.0*t.hr/t.ip hr,
         1.0*t.w/t.ip w,
         1.0*t.l/t.ip l,
         1.0*t.sv/t.ip sv,
         NULL bsv,
         NULL hld,
         NULL qs
    FROM pit_cairo t,
         id_map u
   WHERE t.mlb_id = u.mlb_id
;

  CREATE VIEW v_pit_razz_ip AS
  SELECT t.fg_id,
         1.0*t.g/t.ip g,
         1.0*t.gs/t.ip gs,
         t.ip ip,
         1.0*t.h/t.ip h,
         1.0*t.er/t.ip er,
         1.0*t.bb/t.ip bb,
         1.0*t.so/t.ip so,
         1.0*t.hr/t.ip hr,
         1.0*t.w/t.ip w,
         NULL l,
         1.0*t.sv/t.ip sv,
         NULL bsv,
         NULL hld,
         NULL qs
    FROM pit_razz t
;

  CREATE VIEW v_pit_composite_pa AS
  SELECT t.fg_id,
         (  IFNULL (t.g, 0)
          + IFNULL (u.g, 0)
          + IFNULL (v.g, 0)
          + IFNULL (w.g, 0)
          + IFNULL (x.g, 0)) /
         (  CASE WHEN t.g IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.g IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.g IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.g IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.g IS NULL THEN 0 ELSE 1 END) AS g,
         (  IFNULL (t.gs, 0)
          + IFNULL (u.gs, 0)
          + IFNULL (v.gs, 0)
          + IFNULL (w.gs, 0)
          + IFNULL (x.gs, 0)) /
         (  CASE WHEN t.gs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.gs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.gs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.gs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.gs IS NULL THEN 0 ELSE 1 END) AS gs,
         (  IFNULL (t.ip, 0)
          + 0.5*IFNULL (u.ip, 0)
          + 1.2*IFNULL (v.ip, 0)
          + IFNULL (w.ip, 0)
          + 0.2*IFNULL (x.ip, 0)) /
         (  CASE WHEN t.ip IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.ip IS NULL THEN 0 ELSE 0.5 END
          + CASE WHEN v.ip IS NULL THEN 0 ELSE 1.2 END
          + CASE WHEN w.ip IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.ip IS NULL THEN 0 ELSE 0.2 END) AS ip,
         (  IFNULL (t.h, 0)
          + IFNULL (u.h, 0)
          + IFNULL (v.h, 0)
          + IFNULL (w.h, 0)
          + IFNULL (x.h, 0)) /
         (  CASE WHEN t.h IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.h IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.h IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.h IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.h IS NULL THEN 0 ELSE 1 END) AS h,
         (  IFNULL (t.er, 0)
          + IFNULL (u.er, 0)
          + IFNULL (v.er, 0)
          + IFNULL (w.er, 0)
          + IFNULL (x.er, 0)) /
         (  CASE WHEN t.er IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.er IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.er IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.er IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.er IS NULL THEN 0 ELSE 1 END) AS er,
         (  IFNULL (t.bb, 0)
          + IFNULL (u.bb, 0)
          + IFNULL (v.bb, 0)
          + IFNULL (w.bb, 0)
          + IFNULL (x.bb, 0)) /
         (  CASE WHEN t.bb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.bb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.bb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.bb IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.bb IS NULL THEN 0 ELSE 1 END) AS bb,
         (  IFNULL (t.so, 0)
          + IFNULL (u.so, 0)
          + IFNULL (v.so, 0)
          + IFNULL (w.so, 0)
          + IFNULL (x.so, 0)) /
         (  CASE WHEN t.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.so IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.so IS NULL THEN 0 ELSE 1 END) AS so,
         (  IFNULL (t.hr, 0)
          + IFNULL (u.hr, 0)
          + IFNULL (v.hr, 0)
          + IFNULL (w.hr, 0)
          + IFNULL (x.hr, 0)) /
         (  CASE WHEN t.hr IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.hr IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.hr IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.hr IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.hr IS NULL THEN 0 ELSE 1 END) AS hr,
         (  IFNULL (t.w, 0)
          + IFNULL (u.w, 0)
          + IFNULL (v.w, 0)
          + IFNULL (w.w, 0)
          + IFNULL (x.w, 0)) /
         (  CASE WHEN t.w IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.w IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.w IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.w IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.w IS NULL THEN 0 ELSE 1 END) AS w,
         (  IFNULL (t.l, 0)
          + IFNULL (u.l, 0)
          + IFNULL (v.l, 0)
          + IFNULL (w.l, 0)
          + IFNULL (x.l, 0)) /
         (  CASE WHEN t.l IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.l IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.l IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.l IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.l IS NULL THEN 0 ELSE 1 END) AS l,
         (  IFNULL (t.sv, 0)
          + IFNULL (u.sv, 0)
          + IFNULL (v.sv, 0)
          + IFNULL (w.sv, 0)
          + 0*IFNULL (x.sv, 0)) /
         (  CASE WHEN t.sv IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.sv IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.sv IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.sv IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.sv IS NULL THEN 0 ELSE 0 END) AS sv,
         (  IFNULL (t.bsv, 0)
          + IFNULL (u.bsv, 0)
          + IFNULL (v.bsv, 0)
          + IFNULL (w.bsv, 0)
          + IFNULL (x.bsv, 0)) /
         (  CASE WHEN t.bsv IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.bsv IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.bsv IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.bsv IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.bsv IS NULL THEN 0 ELSE 1 END) AS bsv,
         (  IFNULL (t.hld, 0)
          + IFNULL (u.hld, 0)
          + IFNULL (v.hld, 0)
          + IFNULL (w.hld, 0)
          + IFNULL (x.hld, 0)) /
         (  CASE WHEN t.hld IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.hld IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.hld IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.hld IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.hld IS NULL THEN 0 ELSE 1 END) AS hld,
         (  IFNULL (t.qs, 0)
          + IFNULL (u.qs, 0)
          + IFNULL (v.qs, 0)
          + IFNULL (w.qs, 0)
          + IFNULL (x.qs, 0)) /
         (  CASE WHEN t.qs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN u.qs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN v.qs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN w.qs IS NULL THEN 0 ELSE 1 END
          + CASE WHEN x.qs IS NULL THEN 0 ELSE 1 END) AS qs,
            CASE WHEN t.so IS NOT NULL THEN ',STMR' ELSE '' END
         || CASE WHEN u.so IS NOT NULL THEN ',ZIPS' ELSE '' END
         || CASE WHEN v.so IS NOT NULL THEN ',RAZZ' ELSE '' END
         || CASE WHEN w.so IS NOT NULL THEN ',CLAY' ELSE '' END
         || CASE WHEN x.so IS NOT NULL THEN ',CAIR' ELSE '' END AS mix
    FROM v_pit_sreg_ip t
    LEFT
    JOIN v_pit_zips_ip u
      ON t.fg_id = u.fg_id
    LEFT
    JOIN v_pit_razz_ip v
      ON t.fg_id = v.fg_id
    LEFT
    JOIN v_pit_clay_ip w
      ON t.fg_id = w.fg_id
    LEFT
    JOIN v_pit_cairo_ip x
      ON t.fg_id = x.fg_id
   WHERE t.fg_id IS NOT NULL --steamer is present (always true)
     AND u.fg_id IS NOT NULL --zips is present (almost always true)
;

  CREATE VIEW v_pit_composite AS
  SELECT t.fg_id fg_id,
         u.fg_last fg_last,
         u.fg_first fg_first,
         IFNULL (v.ip, t.ip)*t.g g,
         IFNULL (v.ip, t.ip)*t.gs gs,
         IFNULL (v.ip, t.ip) ip,
         IFNULL (v.ip, t.ip)*t.h h,
         IFNULL (v.ip, t.ip)*t.er er,
         IFNULL (v.ip, t.ip)*t.bb bb,
         IFNULL (v.ip, t.ip)*t.so so,
         IFNULL (v.ip, t.ip)*t.hr hr,
         IFNULL (v.ip, t.ip)*t.w w,
         IFNULL (v.ip, t.ip)*t.l l,
         IFNULL (v.ip, t.ip)*t.sv sv,
         NULL bsv,
         NULL hld,
         NULL qs
    FROM v_pit_composite_pa t,
         id_map u
    LEFT
    JOIN pit_overrides v
      ON t.fg_id = v.fg_id
   WHERE t.fg_id = u.fg_id
; 








  CREATE VIEW v_fan_value AS
  SELECT t.fg_id,
         t.g,
           -2.08361
         + -0.00419*t.ab
         + 0.01517*(t.b1 + t.b2 + t.b3 + t.hr)
         + 0.01224*t.r
         + 0.00929*t.rbi
         + 0.02187*t.hr
         + 0.01701*t.sb AS total,
           -2.30050
         + -0.52934*t.ab/t.g
         + 1.89606*(t.b1 + t.b2 + t.b3 + t.hr)/t.g
         + 1.94821*t.r/t.g
         + 1.37459*t.rbi/t.g
         + 2.93426*t.hr/t.g
         + 1.85568*t.sb/t.g AS per_g
    FROM v_bat_composite t
   UNION
     ALL
  SELECT t.fg_id,
         t.g,
           -0.98791
         + 0.01993*t.ip
         + 0.00367*t.so
         + -0.01132*(t.h + t.bb)
         + -0.02011*t.er
         + 0.03909*t.w
         + 0.01335*t.sv AS total,
           -0.94116
         + 0.55025*t.ip/t.g
         + 0.10067*t.so/t.g
         + -0.32327*(t.h + t.bb)/t.g
         + -0.51771*t.er/t.g
         + 1.05688*t.w/t.g
         + 0.86711*t.sv/t.g AS per_g
    FROM v_pit_composite t
;

CREATE TABLE yh_overrides (yh_id TEXT PRIMARY KEY, rank FLOAT);
INSERT INTO yh_overrides (yh_id, rank) VALUES ('9095', 2000); --darvish
INSERT INTO yh_overrides (yh_id, rank) VALUES ('7963', 65); --pence

  CREATE VIEW v_yh_draft AS
  SELECT *
    FROM (
  SELECT t.year AS year,
         t.yh_id AS yh_id,
         t.name AS name,
         t.team AS team,
         t.pos AS pos,
         IFNULL (v.adp, u.adp) AS adp,
         t.owned AS owned,
         t.orank AS orank,
         t.owner AS owner
    FROM yh_orank t
    LEFT
    JOIN yh_research u
      ON t.yh_id = u.yh_id
    LEFT
    JOIN yh_overrides v
      ON t.yh_id = v.yh_id
         )
ORDER BY 7*ROUND (IFNULL (adp, 2000)/7.0, 0),
         IFNULL (orank, 2000)
;


CREATE TABLE yh_overrides (yh_id TEXT PRIMARY KEY, adp FLOAT);

INSERT INTO yh_overrides (yh_id, adp) VALUES ('9095', 4000); --darvish
INSERT INTO yh_overrides (yh_id, adp) VALUES ('7963', 75); --pence
INSERT INTO yh_overrides (yh_id, adp) VALUES ('7026', 175); --lee
INSERT INTO yh_overrides (yh_id, adp) VALUES ('9637', 4000); --stroman
INSERT INTO yh_overrides (yh_id, adp) VALUES ('9124', 4000); --wheeler
INSERT INTO yh_overrides (yh_id, adp) VALUES ('8167', 4000); --kuroda

CREATE TABLE t_yh_draft AS SELECT * FROM v_yh_draft WHERE owner IS NULL;


INSERT INTO bat_overrides (fg_id, pa) VALUES ('1327', 495); --werth
INSERT INTO bat_overrides (fg_id, pa) VALUES ('8252', 495); --pence
INSERT INTO bat_overrides (fg_id, pa) VALUES ('sa549381', 475); --bryant

INSERT INTO pit_overrides (fg_id, ip) VALUES ('1636', 52); --lee
INSERT INTO pit_overrides (fg_id, ip) VALUES ('3096', 45); --jansen
INSERT INTO pit_overrides (fg_id, ip) VALUES ('13074', 1); --darvish
INSERT INTO pit_overrides (fg_id, ip) VALUES ('10310', 1); --wheeler
INSERT INTO pit_overrides (fg_id, ip) VALUES ('13431', 1); --stroman

  CREATE VIEW v_drafter AS
  SELECT t.fg_id AS id,
         u.fg_name AS name,
         u.yh_pos AS pos,
         v.rowid + 42 AS adp,
         t.g AS g,
         ROUND (50*t.total, 0) + 110 AS total,
         ROUND (50*t.per_g, 0) + 110 AS per_g
    FROM v_fan_value t
    LEFT
    JOIN id_map u
      ON t.fg_id = u.fg_id
    LEFT
    JOIN t_yh_draft v
      ON u.yh_id = v.yh_id
   WHERE v.rowid IS NOT NULL
ORDER BY v.rowid
;


  CREATE VIEW v_bat_value AS
  SELECT t.fg_id AS fg_id,

         15.186*t.hr/t.g - 2.169 AS hrv_g,
         7.586*t.rbi/t.g - 3.974 AS rbiv_g,
         10.116*t.sb/t.g - 0.823 AS sbv_g,
         10.032*t.r/t.g - 5.423 AS rv_g,
         9.707*(t.b1 + t.b2 + t.b3 + t.hr)/t.g - 2.735*t.ab/t.g - 0.043 AS bav_g,

           -2.30050
         + -0.52934*t.ab/t.g
         + 1.89606*(t.b1 + t.b2 + t.b3 + t.hr)/t.g
         + 1.94821*t.r/t.g
         + 1.37459*t.rbi/t.g
         + 2.93426*t.hr/t.g
         + 1.85568*t.sb/t.g AS value_g,

         0.112*t.hr - 2.030 AS hrv,
         0.049*t.rbi - 3.515 AS rbiv,
         0.084*t.sb - 0.955 AS sbv,
         0.066*t.r - 4.855 AS rv,
         0.074*(t.b1 + t.b2 + t.b3 + t.hr) - 0.021*t.ab AS bav,

           -2.08361
         + -0.00419*t.ab
         + 0.01517*(t.b1 + t.b2 + t.b3 + t.hr)
         + 0.01224*t.r
         + 0.00929*t.rbi
         + 0.02187*t.hr
         + 0.01701*t.sb AS value
    FROM v_bat_composite t
;

  CREATE VIEW v_pit_value AS
  SELECT t.fg_id AS fg_id,

         4.750*t.w/t.g - 1.620 AS wv_g,
         4.346*t.sv/t.g - 0.506 AS svv_g,
         0.455*t.so/t.g - 1.931 AS sov_g,
         0.887*t.ip/t.g - 2.687*t.er/t.g - 0.093 AS erav_g,
         1.833*t.ip/t.g - 1.64*(t.h + t.bb)/t.g - 0.078 AS whipv_g,

           -0.94116
         + 0.55025*t.ip/t.g
         + 0.10067*t.so/t.g
         + -0.32327*(t.h + t.bb)/t.g
         + -0.51771*t.er/t.g
         + 1.05688*t.w/t.g
         + 0.86711*t.sv/t.g AS value_g,

         0.188*t.w - 1.713 AS wv,
         0.066*t.sv - 0.592 AS svv,
         0.017*t.so - 2.104 AS sov,
         0.037*t.ip - 0.114*t.er AS erav,
         0.070*t.ip - 0.063*(t.h + t.bb) AS whipv,

           -0.98791
         + 0.01993*t.ip
         + 0.00367*t.so
         + -0.01132*(t.h + t.bb)
         + -0.02011*t.er
         + 0.03909*t.w
         + 0.01335*t.sv AS value
    FROM v_pit_composite t
;

  CREATE VIEW v_test AS
  SELECT IFNULL (u.yh_pos, CASE WHEN t.role = 'PIT' THEN 'P' ELSE NULL END) AS pos,
         t.*
    FROM (
  SELECT u.fg_id AS fg_id,
         u.fg_first || ' ' || u.fg_last AS name,
         u.g AS g,
         u.hr AS "hr/w",
         u.rbi AS "rbi/sv",
         u.sb AS "sb/so",
         u.r AS "r/era",
         (u.b1 + u.b2 + u.b3 + u.hr)/u.ab AS "ba/whip",
         t.hrv_g AS "hr/w val",
         t.rbiv_g AS "rbi/sv val",
         t.sbv_g AS "sb/so val",
         t.rv_g AS "r/era val",
         t.bav_g AS "ba/whip val",
         t.hrv_g + t.rbiv_g + t.sbv_g + t.rv_g + t.bav_g AS val,
         'BAT' AS role
    FROM v_bat_value t,
         v_bat_composite u
   WHERE t.fg_id = u.fg_id
   UNION
     ALL
  SELECT u.fg_id AS fg_id,
         u.fg_first || ' ' || u.fg_last AS name,
         u.g AS g,
         u.w AS "hr/w",
         u.sv AS "rbi/sv",
         u.so AS "sb/so",
         9*u.er/u.ip AS "r/era",
         (u.bb + u.h)/u.ip AS "ba/whip",
         t.wv_g AS "hr/w val",
         t.svv_g AS "rbi/sv val",
         t.sov_g AS "sb/so val",
         t.erav_g AS "r/era val",
         t.whipv_g AS "ba/whip val",
         t.wv_g + t.svv_g + t.sov_g + t.erav_g + t.whipv_g AS val,
         'PIT' AS role
    FROM v_pit_value t,
         v_pit_composite u
   WHERE t.fg_id = u.fg_id
         ) t,
         id_map u
   WHERE t.fg_id = u.fg_id
ORDER BY t.val DESC
;
"""
