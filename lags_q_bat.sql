  SELECT fg_id,
         name,
         season,
         reqd_lag,
         grnd_balls,
         line_drvs,
         fly_balls,
         infld_fly,
         gb_lag
         ld_lag,
         fb_lag,
         iffb_lag,
         1.0*(fly_balls - infld_fly)/(grnd_balls + line_drvs + fly_balls) offb_pct,
         1.0*(fb_lag - iffb_lag)/(gb_lag + ld_lag + fb_lag) offb_pct_lag
    FROM (

  SELECT u.fg_id,
         u.name,
         u.season,
         u.grnd_balls,
         u.line_drvs,
         u.fly_balls,
         u.infld_fly,
         v.reqd_lag,

         CASE v.reqd_lag WHEN 1 THEN u.gb_lag1
                         WHEN 2 THEN u.gb_lag2
                         WHEN 3 THEN u.gb_lag3
                         WHEN 4 THEN u.gb_lag4 ELSE NULL
         END gb_lag,

         CASE v.reqd_lag WHEN 1 THEN u.ld_lag1
                         WHEN 2 THEN u.ld_lag2
                         WHEN 3 THEN u.ld_lag3
                         WHEN 4 THEN u.ld_lag4 ELSE NULL
         END ld_lag,

         CASE v.reqd_lag WHEN 1 THEN u.fb_lag1
                         WHEN 2 THEN u.fb_lag2
                         WHEN 3 THEN u.fb_lag3
                         WHEN 4 THEN u.fb_lag4 ELSE NULL
         END fb_lag,

         CASE v.reqd_lag WHEN 1 THEN u.iffb_lag1
                         WHEN 2 THEN u.iffb_lag2
                         WHEN 3 THEN u.iffb_lag3
                         WHEN 4 THEN u.iffb_lag4 ELSE NULL
         END iffb_lag

    FROM lags u,

         (SELECT t.fg_id,
                 t.season,
                 CASE WHEN t.gb_lag1 + t.ld_lag1 + t.fb_lag1 >= 300
                      THEN 1
                      ELSE CASE WHEN t.gb_lag2 + t.ld_lag2 + t.fb_lag2 >= 300
                                THEN 2
                                ELSE CASE WHEN t.gb_lag3 + t.ld_lag3 + t.fb_lag3 >= 300
                                          THEN 3
                                          ELSE CASE WHEN t.gb_lag4 + t.ld_lag4 + t.fb_lag4 >= 300
                                                    THEN 4
                                                    ELSE NULL
                                               END
                                     END
                           END
                 END reqd_lag
            FROM lags t) v

   WHERE     1 = 1
         AND u.fg_id = v.fg_id
         AND u.season = v.season
         AND v.reqd_lag IS NOT NULL
         AND u.grnd_balls + u.line_drvs + u.fly_balls >= 200

         )
   WHERE     1 = 1
         AND fly_balls - infld_fly > 0
         AND fb_lag - iffb_lag > 0
;
