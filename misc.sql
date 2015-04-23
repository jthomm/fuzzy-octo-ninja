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
;


  SELECT t.*,
         u.g + v.g + w.g g,
         u.ab + v.ab + w.ab ab,
         u.pa + v.pa + w.pa pa,
         u.h + v.h + w.h h,
         u.b1 + v.b1 + w.b1 b1,
         u.b2 + v.b2 + w.b2 b2,
         u.b3 + v.b3 + w.b3 b3,
         u.hr + v.hr + w.hr hr,
         u.r + v.r + w.r r,
         u.rbi + v.rbi + w.rbi rbi,
         u.bb + v.bb + w.bb bb,
         u.ibb + v.ibb + w.ibb ibb,
         u.so + v.so + w.so so,
         u.hbp + v.hbp + w.hbp hbp,
         u.sf + v.sf + w.sf sf,
         u.sh + v.sh + w.sh sh,
         u.gdp + v.gdp + w.gdp gdp,
         u.sb + v.sb + w.sb sb,
         u.cs + v.cs + w.cs cs,
         u.gb + v.gb + w.gb gb,
         u.ld + v.ld + w.ld ld,
         u.fb + v.fb + w.fb fb,
         u.iffb + v.iffb + w.iffb iffb,
         u.ifh + v.ifh + w.ifh ifh,
         u.bu + v.bu + w.bu bu,
         u.buh + v.buh + w.buh buh,
         u.balls + v.balls + w.balls balls,
         u.strikes + v.strikes + w.strikes strikes,
         u.pitches + v.pitches + w.pitches pitches
    FROM bat_basic t,
         bat_basic u,
         bat_basic v,
         bat_basic w
   WHERE     1 = 1
         AND t.fg_id = u.fg_id
         AND u.fg_id = v.fg_id
         AND v.fg_id = w.fg_id
         AND t.year - 1 = u.year
         AND u.year - 1 = v.year
         AND v.year - 1 = w.year
         AND t.pa >= 500
         AND u.pa >= 250
         AND v.pa >= 250
         AND w.pa >= 250
;



  SELECT t.year,
         t.fg_id,
         t.name,

         (SELECT COUNT (1)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) num_yrs,

         (SELECT SUM (w.g)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) g,

         (SELECT SUM (w.ab)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) ab,

         (SELECT SUM (w.pa)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) pa,

         (SELECT SUM (w.h)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) h,

         (SELECT SUM (w.b1)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) b1,

         (SELECT SUM (w.b2)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) b2,

         (SELECT SUM (w.b3)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) b3,

         (SELECT SUM (w.hr)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) hr,

         (SELECT SUM (w.r)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) r,

         (SELECT SUM (w.rbi)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) rbi,

         (SELECT SUM (w.bb)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) bb,

         (SELECT SUM (w.ibb)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) ibb,

         (SELECT SUM (w.so)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) so,

         (SELECT SUM (w.hbp)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) hbp,

         (SELECT SUM (w.sf)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) sf,

         (SELECT SUM (w.sh)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) sh,

         (SELECT SUM (w.gdp)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) gdp,

         (SELECT SUM (w.sb)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) sb,

         (SELECT SUM (w.cs)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) cs,

         (SELECT SUM (w.gb)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) gb,

         (SELECT SUM (w.ld)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) ld,

         (SELECT SUM (w.fb)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) fb,

         (SELECT SUM (w.iffb)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) iffb,

         (SELECT SUM (w.ifh)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) ifh,

         (SELECT SUM (w.bu)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) bu,

         (SELECT SUM (w.buh)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) buh,

         (SELECT SUM (w.balls)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) balls,

         (SELECT SUM (w.strikes)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) strikes,

         (SELECT SUM (w.pitches)
            FROM bat_basic w
           WHERE     1 = 1
                 AND w.fg_id = t.fg_id
                 AND w.year >= t.year - 2) pitches

    FROM bat_basic t
   WHERE     1 = 1
         AND t.year = 2013
;


  SELECT t.*,
         1.0*u.o_swing/100,
         1.0*u.z_swing/100,
         1.0*u.swing/100,
         1.0*u.o_contact/100,
         1.0*u.z_contact/100,
         1.0*u.contact/100,
         1.0*u.zone/100
    FROM bat_basic t,
         bat_pfx u
   WHERE     1 = 1
         AND t.fg_id = u.fg_id
         AND t.year = u.year
         AND t.year > 2007
         AND u.pitches > 300
;




CREATE TABLE bat_pfx_ext
AS
  SELECT t.*,
         (1 - v.zone_pct)*v.o_swing_pct*(1 - v.o_contact_pct) o_sw_miss,
         (1 - v.zone_pct)*v.o_swing_pct*v.o_contact_pct o_sw_cont,
         (1 - v.zone_pct)*(1 - v.o_swing_pct) o_look,
         v.zone_pct*v.z_swing_pct*(1 - v.z_contact_pct) z_sw_miss,
         v.zone_pct*v.z_swing_pct*v.z_contact_pct z_sw_cont,
         v.zone_pct*(1 - v.z_swing_pct) z_look
    FROM bat_pfx t,
         (SELECT u.fg_id,
                 u.year,
                 1.0*u.o_swing/100 o_swing_pct,
                 1.0*u.z_swing/100 z_swing_pct,
                 1.0*u.swing/100 swing_pct,
                 1.0*u.o_contact/100 o_contact_pct,
                 1.0*u.z_contact/100 z_contact_pct,
                 1.0*u.contact/100 contact_pct,
                 1.0*u.zone/100 zone_pct
            FROM bat_pfx u) v
   WHERE     1 = 1
         AND t.fg_id = v.fg_id
         AND t.year = v.year
         AND t.year > 2007
         AND t.pitches > 200
;


CREATE TABLE bat_basic_ext
AS
  SELECT t.*,
         u.o_sw_miss*u.pitches o_sw_miss,
         u.o_sw_cont*u.pitches o_sw_cont,
         u.o_look*u.pitches o_look,
         u.z_sw_miss*u.pitches z_sw_miss,
         u.z_sw_cont*u.pitches z_sw_cont,
         u.z_look*u.pitches z_look
    FROM bat_basic t,
         bat_pfx_ext u
   WHERE     1 = 1
         AND t.fg_id = u.fg_id
         AND t.year = u.year
;


  SELECT t.*,
         u.*
    FROM bat_basic_ext t,
         bat_basic_ext u
   WHERE     1 = 1
         AND t.fg_id = u.fg_id
         AND t.year = u.year + 1
         AND t.pa >= 250
         AND u.pa >= 250
;

  SELECT t.*
    FROM bat_basic_ext t
   WHERE     1 = 1
         AND t.year = 2013
         AND t.pa >= 1250
         AND (   (    1.0*t.hr/(t.gb+t.ld+t.fb-t.sf) >= 0.04
                  AND spd >= 4.5)
              OR EXISTS (SELECT NULL
                           FROM bat_basic_ext u
                          WHERE     1 = 1
                                AND u.year = t.year - 1
                                AND u.pa >= 125
                                AND 1.0*u.hr/(u.gb+u.ld+u.fb-u.sf) >= 0.04
                                AND u.spd >= 4.5))
;



CREATE TABLE pit_pfx_ext
AS
  SELECT t.*,
         (1 - v.zone_pct)*v.o_swing_pct*(1 - v.o_contact_pct) o_sw_miss,
         (1 - v.zone_pct)*v.o_swing_pct*v.o_contact_pct o_sw_cont,
         (1 - v.zone_pct)*(1 - v.o_swing_pct) o_look,
         v.zone_pct*v.z_swing_pct*(1 - v.z_contact_pct) z_sw_miss,
         v.zone_pct*v.z_swing_pct*v.z_contact_pct z_sw_cont,
         v.zone_pct*(1 - v.z_swing_pct) z_look
    FROM pit_pfx t,
         (SELECT u.fg_id,
                 u.year,
                 1.0*u.o_swing/100 o_swing_pct,
                 1.0*u.z_swing/100 z_swing_pct,
                 1.0*u.swing/100 swing_pct,
                 1.0*u.o_contact/100 o_contact_pct,
                 1.0*u.z_contact/100 z_contact_pct,
                 1.0*u.contact/100 contact_pct,
                 1.0*u.zone/100 zone_pct
            FROM pit_pfx u) v
   WHERE     1 = 1
         AND t.fg_id = v.fg_id
         AND t.year = v.year
         AND t.year > 2007
         AND t.pitches > 200
;


  SELECT v.mlb_id,
         t.fg_id,
         t.name,
         1.0*u.pa/u.g cair_pag,
         t.pa stmr_pa,
         u.pa cair_pa,
         t.avg stmr_avg,
         u.avg cair_avg,
         1.0*t.r/t.pa stmr_rpa,
         1.0*u.r/u.pa cair_rpa,
         1.0*t.hr/t.pa stmr_hrpa,
         1.0*u.hr/u.pa cair_hrpa,
         1.0*t.rbi/t.pa stmr_rbipa,
         1.0*u.rbi/u.pa cair_rbipa,
         1.0*t.sb/t.pa stmr_sbpa,
         1.0*u.sb/u.pa cair_sbpa
    FROM bat_stmr t,
         bat_cairo u,
         id_map v
   WHERE     1 = 1
         AND t.fg_id = v.fg_id
         AND u.mlb_id = v.mlb_id
         AND t.pa + t.ab > 2
;

  SELECT v.bbm_id player_id,
         v.fg_last last_name,
         v.fg_first first_name,
         (1.0*(s.pa + t.pa)/2)/s.pa_g games,
         (1.0*(s.pa + t.pa)/2)*(t.ab + u.ab)/2 at_bats,
         (1.0*(s.pa + t.pa)/2)*(t.b1 + u.b1)/2 singles,
         (1.0*(s.pa + t.pa)/2)*(t.b2 + u.b2)/2 doubles,
         (1.0*(s.pa + t.pa)/2)*(t.b3 + u.b3)/2 triples,
         (1.0*(s.pa + t.pa)/2)*(t.hr + u.hr)/2 home_runs,
         (1.0*(s.pa + t.pa)/2)*(t.r + u.r)/2 runs_scored,
         (1.0*(s.pa + t.pa)/2)*(t.rbi + u.rbi)/2 rbi,
         (1.0*(s.pa + t.pa)/2)*(t.bb + u.bb)/2 bases_on_balls,
         (1.0*(s.pa + t.pa)/2)*(t.so + u.so)/2 strikeouts,
         (1.0*(s.pa + t.pa)/2)*(t.sb + u.sb)/2 stolen_bases,
         (1.0*(s.pa + t.pa)/2)*(t.cs + u.cs)/2 stolen_bases_caught
    FROM (SELECT fg_id,
                 g,
                 pa,
                 1.0*pa/g pa_g
            FROM bat_fans) s,
         (SELECT fg_id,
                 pa,
                 1.0*ab/pa ab,
                 1.0*(h - b2 - b3 - hr)/pa b1,
                 1.0*b2/pa b2,
                 1.0*b3/pa b3,
                 1.0*hr/pa hr,
                 1.0*r/pa r,
                 1.0*rbi/pa rbi,
                 1.0*bb/pa bb,
                 1.0*so/pa so,
                 1.0*sb/pa sb,
                 1.0*cs/pa cs
            FROM bat_stmr
           WHERE     1 = 1
                 AND pa + ab > 2) t,
         (SELECT mlb_id,
                 g,
                 pa,
                 1.0*pa/g pa_g,
                 1.0*ab/pa ab,
                 1.0*(h - b2 - b3 - hr)/pa b1,
                 1.0*b2/pa b2,
                 1.0*b3/pa b3,
                 1.0*hr/pa hr,
                 1.0*r/pa r,
                 1.0*rbi/pa rbi,
                 1.0*bb/pa bb,
                 1.0*so/pa so,
                 1.0*sb/pa sb,
                 1.0*cs/pa cs
            FROM bat_cairo) u,
         id_map v
   WHERE     1 = 1
         AND s.fg_id = v.fg_id
         AND t.fg_id = v.fg_id
         AND u.mlb_id = v.mlb_id
;


  SELECT v.bbm_id player_id,
         v.fg_last last_name,
         v.fg_first first_name,
         1.0*(t.g + u.g)/2 games,
         1.0*(t.gs + u.gs)/2 starts,
         (1.0*(t.g + u.g)/2)*(t.ip + u.ip)/2 innings,
         (1.0*(t.g + u.g)/2)*((t.ip + u.ip)/2)*((t.h + u.h)/2) hits_allowed,
         (1.0*(t.g + u.g)/2)*((t.ip + u.ip)/2)*((t.er + u.er)/2) runs_earned,
         (1.0*(t.g + u.g)/2)*((t.ip + u.ip)/2)*((t.bb + u.bb)/2) bases_on_balls,
         (1.0*(t.g + u.g)/2)*((t.ip + u.ip)/2)*((t.so + u.so)/2) so_pitched,
         (1.0*(t.g + u.g)/2)*((t.ip + u.ip)/2)*((t.hr + u.hr)/2) hr_allowed,
         (1.0*(t.g + u.g)/2)*(t.w + u.w)/2 wins,
         (1.0*(t.g + u.g)/2)*(t.l + u.l)/2 losses,
         (1.0*(t.g + u.g)/2)*(t.sv + u.sv)/2 saves,
         NULL saves_blown,
         NULL holds,
         NULL quality_starts
    FROM (SELECT fg_id,
                 g,
                 gs,
                 1.0*ip/g ip,
                 1.0*h/ip h,
                 1.0*er/ip er,
                 1.0*bb/ip bb,
                 1.0*so/ip so,
                 1.0*hr/ip hr,
                 1.0*w/g w,
                 1.0*l/g l,
                 1.0*sv/g sv
            FROM pit_stmr) t,
         (SELECT mlb_id,
                 g,
                 gs,
                 1.0*ip/g ip,
                 1.0*h/ip h,
                 1.0*er/ip er,
                 1.0*bb/ip bb,
                 1.0*so/ip so,
                 1.0*hr/ip hr,
                 1.0*w/g w,
                 1.0*l/g l,
                 1.0*sv/g sv
            FROM pit_cairo) u,
         id_map v
   WHERE     1 = 1
         AND t.fg_id = v.fg_id
         AND u.mlb_id = v.mlb_id
;


  SELECT v.bbm_id player_id,
         v.fg_last last_name,
         v.fg_first first_name,
         t.g games,
         t.gs starts,
         t.ip innings,
         t.h hits_allowed,
         t.er runs_earned,
         t.bb bases_on_balls,
         t.so strikeouts_pitched,
         t.hr home_runs_allowed,
         t.w wins,
         t.l losses,
         t.sv saves,
         NULL saves_blown,
         NULL holds,
         NULL quality_starts,
         NULL comment
    FROM pit_stmr t LEFT OUTER JOIN id_map v ON t.fg_id = v.fg_id
   WHERE t.h > 1
;

--CREATE UNIQUE INDEX id_map_bbm_id_uidx ON id_map (bbm_id)
--CREATE UNIQUE INDEX id_map_fg_id_uidx ON id_map (fg_id)
--CREATE UNIQUE INDEX id_map_mlb_id_uidx ON id_map (mlb_id)
--CREATE UNIQUE INDEX id_map_yh_id_uidx ON id_map (yh_id)
--CREATE UNIQUE INDEX bat_stmr_fg_id_uidx ON bat_stmr (fg_id)
--CREATE UNIQUE INDEX bat_cairo_mlb_id_uidx ON bat_cairo (mlb_id)
--CREATE UNIQUE INDEX pit_stmr_fg_id_uidx ON pit_stmr (fg_id)
--CREATE UNIQUE INDEX pit_cairo_mlb_id_uidx ON pit_cairo (mlb_id)



CREATE VIEW v_bat_pa AS
   SELECT t.fg_id,
          CASE WHEN u.fg_id IS NULL
               THEN t.pa
               ELSE 1.0*(t.pa + u.pa)/2
          END pa
     FROM bat_stmr t
LEFT JOIN bat_fans u ON t.fg_id = u.fg_id
    WHERE t.pa > 1
;

CREATE VIEW v_bat_stmr_pa AS
  SELECT fg_id,
         1.0*ab/pa ab,
         1.0*(h - b2 - b3 - hr)/pa b1,
         1.0*b2/pa b2,
         1.0*b3/pa b3,
         1.0*hr/pa hr,
         1.0*r/pa r,
         1.0*rbi/pa rbi,
         1.0*bb/pa bb,
         1.0*so/pa so,
         1.0*sb/pa sb,
         1.0*cs/pa cs
    FROM bat_stmr
;

CREATE VIEW v_bat_cairo_pa AS
  SELECT mlb_id,
         1.0*g/pa g,
         1.0*ab/pa ab,
         1.0*(h - b2 - b3 - hr)/pa b1,
         1.0*b2/pa b2,
         1.0*b3/pa b3,
         1.0*hr/pa hr,
         1.0*r/pa r,
         1.0*rbi/pa rbi,
         1.0*bb/pa bb,
         1.0*so/pa so,
         1.0*sb/pa sb,
         1.0*cs/pa cs
    FROM bat_cairo
;

CREATE VIEW v_bat_fans_pa AS
  SELECT fg_id,
         1.0*g/pa g
    FROM bat_fans
;

CREATE VIEW v_bat_composite_pa AS
   SELECT t.fg_id,
          CASE WHEN w.g IS NULL
               THEN u.g
               ELSE 1.0*(w.g + u.g)/2
          END g,
          1.0*(t.ab + u.ab)/2 ab,
          1.0*(t.b1 + u.b1)/2 b1,
          1.0*(t.b2 + u.b2)/2 b2,
          1.0*(t.b3 + u.b3)/2 b3,
          1.0*(t.hr + u.hr)/2 hr,
          1.0*(t.r + u.r)/2 r,
          1.0*(t.rbi + u.rbi)/2 rbi,
          1.0*(t.bb + u.bb)/2 bb,
          1.0*(t.so + u.so)/2 so,
          1.0*(t.sb + u.sb)/2 sb,
          1.0*(t.cs + u.cs)/2 cs
     FROM v_bat_stmr_pa t,
          v_bat_cairo_pa u,
          id_map v
LEFT JOIN v_bat_fans_pa w ON v.fg_id = w.fg_id
    WHERE     1 = 1
          AND t.fg_id = v.fg_id
          AND u.mlb_id = v.mlb_id
;

CREATE VIEW v_bat_composite AS
  SELECT t.fg_id,
         v.fg_last,
         v.fg_first,
         u.pa*t.g g,
         u.pa*t.ab ab,
         u.pa*t.b1 b1,
         u.pa*t.b2 b2,
         u.pa*t.b3 b3,
         u.pa*t.hr hr,
         u.pa*t.r r,
         u.pa*t.rbi rbi,
         u.pa*t.bb bb,
         u.pa*t.so so,
         u.pa*t.sb sb,
         u.pa*t.cs cs
    FROM v_bat_composite_pa t,
         v_bat_pa u,
         id_map v
    WHERE     1 = 1
          AND t.fg_id = u.fg_id
          AND t.fg_id = v.fg_id
;

  SELECT u.bbm_id player_id,
         u.fg_last last_name,
         u.fg_first first_name,
         t.g games,
         t.ab at_bats,
         t.b1 singles,
         t.b2 doubles,
         t.b3 triples,
         t.hr home_runs,
         t.r runs_scored,
         t.rbi rbi,
         t.bb bases_on_balls,
         t.so strikeouts,
         t.sb stolen_bases,
         t.cs stolen_bases_caught
    FROM v_bat_composite t,
         id_map u
    WHERE     1 = 1
          AND t.fg_id = u.fg_id
;


CREATE VIEW v2_bat_fans_stmr_f411 AS
  SELECT t.fg_id,
         v.fg_last,
         v.fg_first,

         1.0*w.g/w.pa fans_g,
         1.0*w.pa fans_pa,
         1.0*w.ab/w.pa fans_ab,
         1.0*(w.h - w.b2 - w.b3 - w.hr)/w.pa fans_b1,
         1.0*w.b2/w.pa fans_b2,
         1.0*w.b3/w.pa fans_b3,
         1.0*w.hr/w.pa fans_hr,
         1.0*w.r/w.pa fans_r,
         1.0*w.rbi/w.pa fans_rbi,
         1.0*w.bb/w.pa fans_bb,
         1.0*w.so/w.pa fans_so,
         1.0*w.sb/w.pa fans_sb,
         1.0*w.cs/w.pa fans_cs,

         --1.0*u.g/pa stmr_g,
         1.0*t.pa stmr_pa,
         1.0*t.ab/t.pa stmr_ab,
         1.0*(t.h - t.b2 - t.b3 - t.hr)/t.pa stmr_b1,
         1.0*t.b2/t.pa stmr_b2,
         1.0*t.b3/t.pa stmr_b3,
         1.0*t.hr/t.pa stmr_hr,
         1.0*t.r/t.pa stmr_r,
         1.0*t.rbi/t.pa stmr_rbi,
         1.0*t.bb/t.pa stmr_bb,
         1.0*t.so/t.pa stmr_so,
         1.0*t.sb/t.pa stmr_sb,
         1.0*t.cs/t.pa stmr_cs,

         1.0*u.g/u.pa f411_g,
         1.0*u.pa f411_pa,
         1.0*u.ab/u.pa f411_ab,
         1.0*(u.h - u.b2 - u.b3 - u.hr)/u.pa f411_b1,
         1.0*u.b2/u.pa f411_b2,
         1.0*u.b3/u.pa f411_b3,
         1.0*u.hr/u.pa f411_hr,
         1.0*u.r/u.pa f411_r,
         1.0*u.rbi/u.pa f411_rbi,
         1.0*u.bb/u.pa f411_bb,
         1.0*u.so/u.pa f411_so,
         1.0*u.sb/u.pa f411_sb,
         1.0*u.cs/u.pa f411_cs

    FROM bat_stmr t,
         bat_f411o u,
         id_map v
  LEFT OUTER JOIN bat_fans w ON v.fg_id = w.fg_id

   WHERE     1 = 1
         AND t.fg_id = v.fg_id
         AND u.mlb_id = v.mlb_id
         AND t.pa > 1
;



CREATE VIEW v2_bat_composite AS
  SELECT fg_id,
         fg_last,
         fg_first,

         CASE WHEN fans_g IS NULL
              THEN f411_g
              ELSE 0.1*fans_g + 0.9*f411_g
         END g,

         1.0*(stmr_pa + f411_pa)/2 pa,

         CASE WHEN fans_ab IS NULL
              THEN 1.0*(stmr_ab + f411_ab)/2
              ELSE 1.0*(fans_ab + stmr_ab + f411_ab)/3
         END ab,

         CASE WHEN fans_b1 IS NULL
              THEN 1.0*(stmr_b1 + f411_b1)/2
              ELSE 1.0*(fans_b1 + stmr_b1 + f411_b1)/3
         END b1,

         CASE WHEN fans_b2 IS NULL
              THEN 1.0*(stmr_b2 + f411_b2)/2
              ELSE 1.0*(fans_b2 + stmr_b2 + f411_b2)/3
         END b2,

         CASE WHEN fans_b3 IS NULL
              THEN 1.0*(stmr_b3 + f411_b3)/2
              ELSE 1.0*(fans_b3 + stmr_b3 + f411_b3)/3
         END b3,

         CASE WHEN fans_hr IS NULL
              THEN 1.0*(stmr_hr + f411_hr)/2
              ELSE 1.0*(fans_hr + stmr_hr + f411_hr)/3
         END hr,

         CASE WHEN fans_r IS NULL
              THEN 1.0*(stmr_r + f411_r)/2
              ELSE 1.0*(fans_r + stmr_r + f411_r)/3
         END r,

         CASE WHEN fans_rbi IS NULL
              THEN 1.0*(stmr_rbi + f411_rbi)/2
              ELSE 1.0*(fans_rbi + stmr_rbi + f411_rbi)/3
         END rbi,
        
         CASE WHEN fans_bb IS NULL
              THEN 1.0*(stmr_bb + f411_bb)/2
              ELSE 1.0*(fans_bb + stmr_bb + f411_bb)/3
         END bb,

         CASE WHEN fans_so IS NULL
              THEN 1.0*(stmr_so + f411_so)/2
              ELSE 1.0*(fans_so + stmr_so + f411_so)/3
         END so,

         CASE WHEN fans_sb IS NULL
              THEN 1.0*(stmr_sb + f411_sb)/2
              ELSE 1.0*(fans_sb + stmr_sb + f411_sb)/3
         END sb,

         CASE WHEN fans_cs IS NULL
              THEN 1.0*(stmr_cs + f411_cs)/2
              ELSE 1.0*(fans_cs + stmr_cs + f411_cs)/3
         END cs
    FROM v2_bat_fans_stmr_f411
;


  SELECT u.bbm_id player_id,
         t.fg_last last_name,
         t.fg_first first_name,
         t.g*t.pa games,
         t.ab*t.pa at_bats,
         t.b1*t.pa singles,
         t.b2*t.pa doubles,
         t.b3*t.pa triples,
         t.hr*t.pa home_runs,
         t.r*t.pa runs_scored,
         t.rbi*t.pa rbi,
         t.bb*t.pa bases_on_balls,
         t.so*t.pa strikeouts,
         t.sb*t.pa stolen_bases,
         t.cs*t.pa stolen_bases_caught,
         NULL comment
    FROM v2_bat_composite t,
         id_map u
   WHERE     1 = 1
         AND t.fg_id = u.fg_id
;

/*** Fangraphs FANs + Steamer for games/innings, Steamer for rate stats ***/

CREATE VIEW v_pit_stmr_per_g AS
  SELECT fg_id,
         g g,
         1.0*gs/g gs_g,
         1.0*w/g w_g,
         1.0*l/g l_g,
         1.0*sv/g sv_g,
         1.0*ip/g ip_g
    FROM pit_stmr t
   WHERE ip > 1
;

CREATE VIEW v_pit_fans_per_g AS
  SELECT fg_id,
         g g,
         1.0*gs/g gs_g,
         1.0*w/g w_g,
         1.0*l/g l_g,
         1.0*sv/g sv_g,
         1.0*ip/g ip_g
    FROM pit_fans t
;

CREATE VIEW v_pit_stmr_fans_per_g AS
  SELECT t.fg_id,
         CASE WHEN u.fg_id IS NULL
              THEN t.g
              ELSE 1.0*(t.g + u.g)/2
         END g,
         CASE WHEN u.fg_id IS NULL
              THEN t.gs_g
              ELSE 1.0*(t.gs_g + u.gs_g)/2
         END gs_g,
         CASE WHEN u.fg_id IS NULL
              THEN t.w_g
              ELSE 1.0*(t.w_g + u.w_g)/2
         END w_g,
         CASE WHEN u.fg_id IS NULL
              THEN t.l_g
              ELSE 1.0*(t.l_g + u.l_g)/2
         END l_g,
         CASE WHEN u.fg_id IS NULL
              THEN t.sv_g
              ELSE 1.0*(t.sv_g + u.sv_g)/2
         END sv_g,
         CASE WHEN u.fg_id IS NULL
              THEN t.ip_g
              ELSE 1.0*(t.ip_g + u.ip_g)/2
         END ip_g
    FROM v_pit_stmr_per_g t
         LEFT OUTER JOIN v_pit_fans_per_g u
            ON t.fg_id = u.fg_id
  UNION
  SELECT u.fg_id,
         CASE WHEN t.fg_id IS NULL
              THEN u.g
              ELSE 1.0*(u.g + t.g)/2
         END g,
         CASE WHEN t.fg_id IS NULL
              THEN u.gs_g
              ELSE 1.0*(u.gs_g + t.gs_g)/2
         END gs_g,
         CASE WHEN t.fg_id IS NULL
              THEN u.w_g
              ELSE 1.0*(u.w_g + t.w_g)/2
         END w_g,
         CASE WHEN t.fg_id IS NULL
              THEN u.l_g
              ELSE 1.0*(u.l_g + t.l_g)/2
         END l_g,
         CASE WHEN t.fg_id IS NULL
              THEN u.sv_g
              ELSE 1.0*(u.sv_g + t.sv_g)/2
         END sv_g,
         CASE WHEN t.fg_id IS NULL
              THEN u.ip_g
              ELSE 1.0*(u.ip_g + t.ip_g)/2
         END ip_g
    FROM v_pit_fans_per_g u
         LEFT OUTER JOIN v_pit_stmr_per_g t
            ON u.fg_id = t.fg_id
;

CREATE VIEW v_pit_stmr_per_ip AS
  SELECT fg_id,
         name,
         1.0*k9/9 so_ip,
         1.0*bb9/9 bb_ip,
         1.0*(whip - 1.0*bb9/9) h_ip,
         1.0*era/9 er_ip,
         1.0*hr/ip hr_ip,
         1.0*(fip - 3.048 - 13*hr/ip - 3*bb9/9 + 2*k9/9)/3 hbp_ip
    FROM pit_stmr
;

CREATE VIEW v_pit_stmr_fans AS
  SELECT t.fg_id,
         t.name,
         u.g,
         u.g*u.gs_g gs,
         u.g*u.w_g w,
         u.g*u.l_g l,
         u.g*u.sv_g sv,
         u.g*u.ip_g ip,
         u.g*u.ip_g*t.so_ip so,
         u.g*u.ip_g*t.bb_ip bb,
         u.g*u.ip_g*t.h_ip h,
         u.g*u.ip_g*t.er_ip er,
         u.g*u.ip_g*t.hr_ip hr,
         u.g*u.ip_g*t.hbp_ip hbp
    FROM v_pit_stmr_per_ip t,
         v_pit_stmr_fans_per_g u
   WHERE t.fg_id = u.fg_id
;





  CREATE VIEW v_pit_report AS
  SELECT y.*,

         1.0809*e_fip + 3.2272 AS fip,
         1.1760*e_xfip + 3.0624 AS xfip,
         2.1782*e_sbera - 1.4579 AS sbera,
         1.1552*9*xer/xip - 0.4023 AS xera,

         1.0*so/tbf AS so_pct,
         1.0*xso/xtbf AS xso_pct,
         1.0*bb/tbf AS bb_pct,
         1.0*xbb/xtbf AS xbb_pct,
         1.0*hr/tbf AS hr_pct,
         1.0*xhr/xtbf AS xhr_pct

    FROM (
  SELECT x.*,
         9.0*er/ip AS era,
         1.0*(13*hr + 3*bb - 2*so)/ip AS e_fip,
         1.0*(13*0.111*(iffb + offb) + 3*bb - 2*so)/ip AS e_xfip,
           (8.8*hr + 5.4*bb - 6.2*so)/tbf
         + (1.7*ld + 5.1*offb - 0.6*gb)/(iffb + offb + ld + gb)
         - 7*(1.0*(offb)/(iffb + offb + ld + gb))*(1.0*(offb)/(iffb + offb + ld + gb))
         + 2.4*z_sw_cont/(z_sw_cont + z_sw_miss) AS e_sbera,

          0.11877*lk_ball + 0.19096*lk_strk + 0.34294*sw_strk + 0.10135*sw_foul + 0.77570*sw_grn + 0.66701*sw_air AS xtbf,
         -0.00908*lk_ball + 0.08354*lk_strk + 0.12849*sw_strk + 0.03976*sw_foul + 0.19833*sw_grn + 0.14193*sw_air AS xip,
          0.06814*lk_ball - 0.05976*lk_strk - 0.05335*sw_strk - 0.03622*sw_foul + 0.05977*sw_grn + 0.18348*sw_air AS xer,
          0.00568*lk_ball - 0.00643*lk_strk + 0.00000*sw_strk - 0.01469*sw_foul - 0.00678*sw_grn + 0.08661*sw_air AS xhr,
         -0.02665*lk_ball + 0.23239*lk_strk + 0.38502*sw_strk + 0.10671*sw_foul - 0.12912*sw_grn - 0.23115*sw_air AS xso,
          0.13797*lk_ball - 0.03999*lk_strk - 0.03678*sw_strk - 0.00947*sw_foul - 0.09902*sw_grn - 0.09263*sw_air AS xbb,
          0.01318*lk_ball - 0.02108*lk_strk - 0.01813*sw_strk - 0.01069*sw_foul + 0.31763*sw_grn + 0.34157*sw_air AS xh

    FROM (
  SELECT v.year || '-' || v.fg_id "year-fg_id",
         v.year,
         v.fg_id,
         u.bbm_id,
         v.name,
         CAST (v.ip AS INT) + (10.0/3)*(v.ip - CAST (v.ip AS INT)) ip,
         v.er,
         v.r,
         v.hr,
         v.tbf,
         v.so,
         v.bb,
         v.bu,
         v.gb,
         v.ld,
         v.fb - v.iffb offb,
         v.iffb,
         w.o_sw_miss,
         w.o_sw_cont,
         w.o_look,
         w.z_sw_miss,
         w.z_sw_cont,
         w.z_look,
         w.pitches,
         w.balls,
         w.strikes,
         w.balls lk_ball,
         w.pitches*(w.z_look + w.o_look) - w.balls lk_strk,
         w.pitches*(w.z_sw_miss + w.o_sw_miss) sw_strk,
         w.pitches*(w.z_sw_cont + w.o_sw_cont) - (v.bu + v.gb + v.ld + v.fb) sw_foul,
         v.bu + v.gb sw_grn,
         v.ld + v.fb sw_air
    FROM pit_basic v,
         v_pit_pfx_ext w
    LEFT
   OUTER
    JOIN id_map u ON u.fg_id = v.fg_id
   WHERE 1 = 1
     AND v.fg_id = w.fg_id
     AND v.year = w.year
         ) x
         ) y
ORDER BY year DESC,
         CASE WHEN year = 2015 THEN 1.0*xer/xip ELSE e_sbera END
;


  SELECT w.fg_id,
         w.total_pa,
         w.name,
         w.age,
         w.spd,
         w.hr_pct,
         w.ld_pct,
         w.so_pct,
         w.avg,
         w.xavg,
         w.xval
    FROM (
  SELECT v.*,
         1.0*v.h/v.ab avg,
         1.0*v.xh/v.ab xavg,
         0.1*v.spd + 7*hr_pct + 13*(1.0*v.xh/v.ab) - 5 xval
    FROM (
  SELECT t.*,
         u.bbm_id,
         1.0*t.hr/(t.hr+t.gb) hr_pct,
         1.0*t.ld/(t.ld+t.so) ld_pct,
         1.0*t.so/t.pa so_pct,
         0.202*(t.gb - t.ifh) + 0.623*(t.ld - 0.1*t.hr) + 0.251*(t.fb - t.iffb - 0.9*t.hr - t.sf) - 0.339*t.iffb + t.ifh + t.hr + t.buh xh
    FROM (
  SELECT r.fg_id,
         r.name,
         r.team,
         r.age,
         r.pa + IFNULL (s.pa, 0) + IFNULL (t.pa, 0) total_pa,
         5*r.pa + 4*IFNULL (s.pa, 0) + 3*IFNULL (t.pa, 0) pa,
         5*r.ab + 4*IFNULL (s.ab, 0) + 3*IFNULL (t.ab, 0) ab,
         5*r.h + 4*IFNULL (s.h, 0) + 3*IFNULL (t.h, 0) h,
         5*r.hr + 4*IFNULL (s.hr, 0) + 3*IFNULL (t.hr, 0) hr,
         5*r.so + 4*IFNULL (s.so, 0) + 3*IFNULL (t.so, 0) so,
         5*r.bb + 4*IFNULL (s.bb, 0) + 3*IFNULL (t.bb, 0) bb,
         5*r.buh + 4*IFNULL (s.buh, 0) + 3*IFNULL (t.buh, 0) buh,
         5*r.gb + 4*IFNULL (s.gb, 0) + 3*IFNULL (t.gb, 0) gb,
         5*r.ld + 4*IFNULL (s.ld, 0) + 3*IFNULL (t.ld, 0) ld,
         5*r.fb + 4*IFNULL (s.fb, 0) + 3*IFNULL (t.fb, 0) fb,
         5*r.iffb + 4*IFNULL (s.iffb, 0) + 3*IFNULL (t.iffb, 0) iffb,
         5*r.sf + 4*IFNULL (s.sf, 0) + 3*IFNULL (t.sf, 0) sf,
         5*r.ifh + 4*IFNULL (s.ifh, 0) + 3*IFNULL (t.ifh, 0) ifh,
         1.0*(5*r.g*r.spd + 4*IFNULL (s.g, 0)*IFNULL (s.spd, 0) + 3*IFNULL (t.g, 0)*IFNULL (t.spd, 0))/(5*r.g + 4*IFNULL (s.g, 0) + 3*IFNULL (t.g, 0)) spd
    FROM bat_basic r
    LEFT
   OUTER
    JOIN bat_basic s ON r.fg_id = s.fg_id AND r.year = s.year + 1
    LEFT
   OUTER
    JOIN bat_basic t ON r.fg_id = t.fg_id AND r.year = t.year + 2
   WHERE r.year = 2015
     AND r.pa >= 30
         ) t
    LEFT
   OUTER
    JOIN id_map u ON u.fg_id = t.fg_id
         ) v
         ) w
ORDER BY w.xval DESC
;
