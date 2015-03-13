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

  CREATE VIEW v_bat_composite_pa AS
  SELECT t.fg_id,
         CASE WHEN v.g IS NULL AND w.g IS NULL
              THEN 1.0*(t.g + u.g)/2
              WHEN v.g IS NULL
              THEN 1.0*(t.g + u.g + w.g)/3
              WHEN w.g IS NULL
              THEN 1.0*(t.g + u.g + v.g)/3
              ELSE 1.0*(t.g + u.g + v.g + w.g)/4
         END AS g,
         CASE WHEN v.pa IS NULL AND w.pa IS NULL
              THEN 0.9*t.pa + 0.1*u.pa
              WHEN v.pa IS NULL
              THEN 0.9*t.pa + 0.05*u.pa + 0.05*w.pa
              WHEN w.pa IS NULL
              THEN 0.6*t.pa + 0.1*u.pa + 0.3*v.pa
              ELSE 0.6*t.pa + 0.05*u.pa + 0.3*v.pa + 0.05*w.pa
         END AS pa,
         CASE WHEN v.ab IS NULL AND w.ab IS NULL
              THEN 1.0*(t.ab + u.ab)/2
              WHEN v.ab IS NULL
              THEN 1.0*(t.ab + u.ab + w.ab)/3
              WHEN w.ab IS NULL
              THEN 1.0*(t.ab + u.ab + v.ab)/3
              ELSE 1.0*(t.ab + u.ab + v.ab + w.ab)/4
         END AS ab,
         CASE WHEN v.b1 IS NULL AND w.b1 IS NULL
              THEN 1.0*(t.b1 + u.b1)/2
              WHEN v.b1 IS NULL
              THEN 1.0*(t.b1 + u.b1 + w.b1)/3
              WHEN w.b1 IS NULL
              THEN 1.0*(t.b1 + u.b1 + v.b1)/3
              ELSE 1.0*(t.b1 + u.b1 + v.b1 + w.b1)/4
         END AS b1,
         CASE WHEN v.b2 IS NULL AND w.b2 IS NULL
              THEN 1.0*(t.b2 + u.b2)/2
              WHEN v.b2 IS NULL
              THEN 1.0*(t.b2 + u.b2 + w.b2)/3
              WHEN w.b2 IS NULL
              THEN 1.0*(t.b2 + u.b2 + v.b2)/3
              ELSE 1.0*(t.b2 + u.b2 + v.b2 + w.b2)/4
         END AS b2,
         CASE WHEN v.b3 IS NULL AND w.b3 IS NULL
              THEN 1.0*(t.b3 + u.b3)/2
              WHEN v.b3 IS NULL
              THEN 1.0*(t.b3 + u.b3 + w.b3)/3
              WHEN w.b3 IS NULL
              THEN 1.0*(t.b3 + u.b3 + v.b3)/3
              ELSE 1.0*(t.b3 + u.b3 + v.b3 + w.b3)/4
         END AS b3,
         CASE WHEN v.hr IS NULL AND w.hr IS NULL
              THEN 1.0*(t.hr + u.hr)/2
              WHEN v.hr IS NULL
              THEN 1.0*(t.hr + u.hr + w.hr)/3
              WHEN w.hr IS NULL
              THEN 1.0*(t.hr + u.hr + v.hr)/3
              ELSE 1.0*(t.hr + u.hr + v.hr + w.hr)/4
         END AS hr,
         CASE WHEN v.r IS NULL AND w.r IS NULL
              THEN 1.0*(t.r + u.r)/2
              WHEN v.r IS NULL
              THEN 1.0*(t.r + u.r + w.r)/3
              WHEN w.r IS NULL
              THEN 1.0*(t.r + u.r + v.r)/3
              ELSE 1.0*(t.r + u.r + v.r + w.r)/4
         END AS r,
         CASE WHEN v.rbi IS NULL AND w.rbi IS NULL
              THEN 1.0*(t.rbi + u.rbi)/2
              WHEN v.rbi IS NULL
              THEN 1.0*(t.rbi + u.rbi + w.rbi)/3
              WHEN w.rbi IS NULL
              THEN 1.0*(t.rbi + u.rbi + v.rbi)/3
              ELSE 1.0*(t.rbi + u.rbi + v.rbi + w.rbi)/4
         END AS rbi,
         CASE WHEN v.bb IS NULL AND w.bb IS NULL
              THEN 1.0*(t.bb + u.bb)/2
              WHEN v.bb IS NULL
              THEN 1.0*(t.bb + u.bb + w.bb)/3
              WHEN w.bb IS NULL
              THEN 1.0*(t.bb + u.bb + v.bb)/3
              ELSE 1.0*(t.bb + u.bb + v.bb + w.bb)/4
         END AS bb,
         CASE WHEN v.so IS NULL AND w.so IS NULL
              THEN 1.0*(t.so + u.so)/2
              WHEN v.so IS NULL
              THEN 1.0*(t.so + u.so + w.so)/3
              WHEN w.so IS NULL
              THEN 1.0*(t.so + u.so + v.so)/3
              ELSE 1.0*(t.so + u.so + v.so + w.so)/4
         END AS so,
         CASE WHEN v.sb IS NULL AND w.sb IS NULL
              THEN 1.0*(t.sb + u.sb)/2
              WHEN v.sb IS NULL
              THEN 1.0*(t.sb + u.sb + w.sb)/3
              WHEN w.sb IS NULL
              THEN 1.0*(t.sb + u.sb + v.sb)/3
              ELSE 1.0*(t.sb + u.sb + v.sb + w.sb)/4
         END AS sb,
         CASE WHEN v.cs IS NULL AND w.cs IS NULL
              THEN 1.0*(t.cs + u.cs)/2
              WHEN v.cs IS NULL
              THEN 1.0*(t.cs + u.cs + w.cs)/3
              WHEN w.cs IS NULL
              THEN 1.0*(t.cs + u.cs + v.cs)/3
              ELSE 1.0*(t.cs + u.cs + v.cs + w.cs)/4
         END AS cs,
         CASE WHEN v.ab IS NULL AND w.ab IS NULL
              THEN 'STMR-ZIPS'
              WHEN v.ab IS NULL
              THEN 'STMR-ZIPS-CAIR'
              WHEN w.ab IS NULL
              THEN 'STMR-ZIPS-CLAY'
              ELSE 'STMR-ZIPS-CLAY-CAIR'
         END AS mix
    FROM v_bat_stmr_pa t
    LEFT
    JOIN v_bat_zips_pa u
      ON t.fg_id = u.fg_id
    LEFT
    JOIN v_bat_clay_pa v
      ON t.fg_id = v.fg_id
    LEFT
    JOIN v_bat_cairo_pa w
      ON t.fg_id = w.fg_id
   WHERE t.fg_id IS NOT NULL --steamer is present (always true)
     AND u.fg_id IS NOT NULL --zips is present (almost always true)
;

  CREATE VIEW v_bat_composite AS
  SELECT t.fg_id,
         u.fg_last,
         u.fg_first,
         t.pa*t.g g,
         t.pa*t.ab ab,
         t.pa*t.b1 b1,
         t.pa*t.b2 b2,
         t.pa*t.b3 b3,
         t.pa*t.hr hr,
         t.pa*t.r r,
         t.pa*t.rbi rbi,
         t.pa*t.bb bb,
         t.pa*t.so so,
         t.pa*t.sb sb,
         t.pa*t.cs cs
    FROM v_bat_composite_pa t,
         id_map u
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

  CREATE VIEW v_pit_composite_pa AS
  SELECT t.fg_id,
         CASE WHEN v.g IS NULL AND w.g IS NULL
              THEN 1.0*(t.g + u.g)/2
              WHEN v.g IS NULL
              THEN 1.0*(t.g + u.g + w.g)/3
              WHEN w.g IS NULL
              THEN 1.0*(t.g + u.g + v.g)/3
              ELSE 1.0*(t.g + u.g + v.g + w.g)/4
         END AS g,
         CASE WHEN v.gs IS NULL AND w.gs IS NULL
              THEN 1.0*(t.gs + u.gs)/2
              WHEN v.gs IS NULL
              THEN 1.0*(t.gs + u.gs + w.gs)/3
              WHEN w.gs IS NULL
              THEN 1.0*(t.gs + u.gs + v.gs)/3
              ELSE 1.0*(t.gs + u.gs + v.gs + w.gs)/4
         END AS gs,
         CASE WHEN v.ip IS NULL AND w.ip IS NULL
              THEN 0.9*t.ip + 0.1*u.ip
              WHEN v.ip IS NULL
              THEN 0.9*t.ip + 0.05*u.ip + 0.05*w.ip
              WHEN w.ip IS NULL
              THEN 0.6*t.ip + 0.1*u.ip + 0.3*v.ip
              ELSE 0.6*t.ip + 0.05*u.ip + 0.3*v.ip + 0.05*w.ip
         END AS ip,
         CASE WHEN v.h IS NULL AND w.h IS NULL
              THEN 1.0*(t.h + u.h)/2
              WHEN v.h IS NULL
              THEN 1.0*(t.h + u.h + w.h)/3
              WHEN w.h IS NULL
              THEN 1.0*(t.h + u.h + v.h)/3
              ELSE 1.0*(t.h + u.h + v.h + w.h)/4
         END AS h,
         CASE WHEN v.er IS NULL AND w.er IS NULL
              THEN 1.0*(t.er + u.er)/2
              WHEN v.er IS NULL
              THEN 1.0*(t.er + u.er + w.er)/3
              WHEN w.er IS NULL
              THEN 1.0*(t.er + u.er + v.er)/3
              ELSE 1.0*(t.er + u.er + v.er + w.er)/4
         END AS er,
         CASE WHEN v.bb IS NULL AND w.bb IS NULL
              THEN 1.0*(t.bb + u.bb)/2
              WHEN v.bb IS NULL
              THEN 1.0*(t.bb + u.bb + w.bb)/3
              WHEN w.bb IS NULL
              THEN 1.0*(t.bb + u.bb + v.bb)/3
              ELSE 1.0*(t.bb + u.bb + v.bb + w.bb)/4
         END AS bb,
         CASE WHEN v.so IS NULL AND w.so IS NULL
              THEN 1.0*(t.so + u.so)/2
              WHEN v.so IS NULL
              THEN 1.0*(t.so + u.so + w.so)/3
              WHEN w.so IS NULL
              THEN 1.0*(t.so + u.so + v.so)/3
              ELSE 1.0*(t.so + u.so + v.so + w.so)/4
         END AS so,
         CASE WHEN v.hr IS NULL AND w.hr IS NULL
              THEN 1.0*(t.hr + u.hr)/2
              WHEN v.hr IS NULL
              THEN 1.0*(t.hr + u.hr + w.hr)/3
              WHEN w.hr IS NULL
              THEN 1.0*(t.hr + u.hr + v.hr)/3
              ELSE 1.0*(t.hr + u.hr + v.hr + w.hr)/4
         END AS hr,
         CASE WHEN v.w IS NULL AND w.w IS NULL
              THEN 1.0*(t.w + u.w)/2
              WHEN v.w IS NULL
              THEN 1.0*(t.w + u.w + w.w)/3
              WHEN w.w IS NULL
              THEN 1.0*(t.w + u.w + v.w)/3
              ELSE 1.0*(t.w + u.w + v.w + w.w)/4
         END AS w,
         CASE WHEN v.l IS NULL AND w.l IS NULL
              THEN 1.0*(t.l + u.l)/2
              WHEN v.l IS NULL
              THEN 1.0*(t.l + u.l + w.l)/3
              WHEN w.l IS NULL
              THEN 1.0*(t.l + u.l + v.l)/3
              ELSE 1.0*(t.l + u.l + v.l + w.l)/4
         END AS l,
         CASE WHEN v.sv IS NULL AND w.sv IS NULL
              THEN t.sv
              WHEN v.sv IS NULL
              THEN 1.0*(t.sv + w.sv)/2
              WHEN w.sv IS NULL
              THEN 1.0*(t.sv + v.sv)/2
              ELSE 1.0*(t.sv + v.sv + w.sv)/3
         END AS sv,
         NULL bsv,
         NULL hld,
         NULL qs,
         CASE WHEN v.ip IS NULL AND w.ip IS NULL
              THEN 'STMR-ZIPS'
              WHEN v.ip IS NULL
              THEN 'STMR-ZIPS-CAIR'
              WHEN w.ip IS NULL
              THEN 'STMR-ZIPS-CLAY'
              ELSE 'STMR-ZIPS-CLAY-CAIR'
         END AS mix
    FROM v_pit_stmr_ip t
    LEFT
    JOIN v_pit_zips_ip u
      ON t.fg_id = u.fg_id
    LEFT
    JOIN v_pit_clay_ip v
      ON t.fg_id = v.fg_id
    LEFT
    JOIN v_pit_cairo_ip w
      ON t.fg_id = w.fg_id
   WHERE t.fg_id IS NOT NULL --steamer is present (always true)
     AND u.fg_id IS NOT NULL --zips is present (almost always true)
;

  CREATE VIEW v_pit_composite AS
  SELECT t.fg_id,
         u.fg_last,
         u.fg_first,
         t.ip*t.g g,
         t.ip*t.gs gs,
         t.ip ip,
         t.ip*t.h h,
         t.ip*t.er er,
         t.ip*t.bb bb,
         t.ip*t.so so,
         t.ip*t.hr hr,
         t.ip*t.w w,
         t.ip*t.l l,
         t.ip*t.sv sv,
         NULL bsv,
         NULL hld,
         NULL qs
    FROM v_pit_composite_pa t,
         id_map u
   WHERE t.fg_id = u.fg_id
; 

UPDATE pit_cairo SET sv = 34 WHERE first = 'Aroldis';
UPDATE pit_cairo SET sv = 24 WHERE first = 'Dellin';
"""
