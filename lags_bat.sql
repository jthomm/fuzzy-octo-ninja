CREATE TABLE lags AS

  SELECT fg_id,
         name,
         season,
         struckout,
         walks,
         int_walks,
         home_runs,
         grnd_balls,
         line_drvs,
         fly_balls,
         infld_fly,

         /* Lag of 1 year (i.e. previous year) */

         (  SELECT COUNT (*)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) seas_lag1,

         (  SELECT SUM (u.struckout)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) so_lag1,

         (  SELECT SUM (u.walks)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) bb_lag1,

         (  SELECT SUM (u.home_runs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) ibb_lag1,

         (  SELECT SUM (u.home_runs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) hr_lag1,

         (  SELECT SUM (u.grnd_balls)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) gb_lag1,

         (  SELECT SUM (u.line_drvs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) ld_lag1,

         (  SELECT SUM (u.fly_balls)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) fb_lag1,

         (  SELECT SUM (u.infld_fly)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) iffb_lag1,

         /* Lag of 2 years (i.e. previous 2 years) */

         (  SELECT COUNT (*)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) seas_lag2,

         (  SELECT SUM (u.struckout)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) so_lag2,

         (  SELECT SUM (u.walks)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) bb_lag2,

         (  SELECT SUM (u.home_runs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) ibb_lag2,

         (  SELECT SUM (u.home_runs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) hr_lag2,

         (  SELECT SUM (u.grnd_balls)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) gb_lag2,

         (  SELECT SUM (u.line_drvs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) ld_lag2,

         (  SELECT SUM (u.fly_balls)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) fb_lag2,

         (  SELECT SUM (u.infld_fly)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) iffb_lag2,

         /* Lag of 3 years (i.e. previous 3 years) */

         (  SELECT COUNT (*)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) seas_lag3,

         (  SELECT SUM (u.struckout)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) so_lag3,

         (  SELECT SUM (u.walks)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) bb_lag3,

         (  SELECT SUM (u.home_runs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) ibb_lag3,

         (  SELECT SUM (u.home_runs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) hr_lag3,

         (  SELECT SUM (u.grnd_balls)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) gb_lag3,

         (  SELECT SUM (u.line_drvs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) ld_lag3,

         (  SELECT SUM (u.fly_balls)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) fb_lag3,

         (  SELECT SUM (u.infld_fly)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) iffb_lag3,

         /* Lag of 4 years (i.e. previous 4 years) */

         (  SELECT COUNT (*)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) seas_lag4,

         (  SELECT SUM (u.struckout)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) so_lag4,

         (  SELECT SUM (u.walks)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) bb_lag4,

         (  SELECT SUM (u.home_runs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) ibb_lag4,

         (  SELECT SUM (u.home_runs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) hr_lag4,

         (  SELECT SUM (u.grnd_balls)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) gb_lag4,

         (  SELECT SUM (u.line_drvs)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) ld_lag4,

         (  SELECT SUM (u.fly_balls)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) fb_lag4,

         (  SELECT SUM (u.infld_fly)
              FROM fg_bat u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) iffb_lag4

    FROM fg_bat t
ORDER BY t.name,
         t.fg_id,
         t.season
;
