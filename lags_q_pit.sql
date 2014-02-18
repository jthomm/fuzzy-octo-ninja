  SELECT u.fg_id,
         u.name,
         u.season,
         w.tb_faced,
         w.strikeouts,
         w.walks,
         w.int_walks,
         w.hitby_ptch,
         w.bunts,
         w.home_runs,
         w.grnd_balls,
         w.line_drvs,
         w.fly_balls,
         w.infld_fly,
         v.reqd_lag,

         CASE v.reqd_lag WHEN 1 THEN u.tbf_lag1
                         WHEN 2 THEN u.tbf_lag2
                         WHEN 3 THEN u.tbf_lag3
                         WHEN 4 THEN u.tbf_lag4 ELSE NULL
         END tbf_lag,

         CASE v.reqd_lag WHEN 1 THEN u.so_lag1
                         WHEN 2 THEN u.so_lag2
                         WHEN 3 THEN u.so_lag3
                         WHEN 4 THEN u.so_lag4 ELSE NULL
         END so_lag,

         CASE v.reqd_lag WHEN 1 THEN u.bb_lag1
                         WHEN 2 THEN u.bb_lag2
                         WHEN 3 THEN u.bb_lag3
                         WHEN 4 THEN u.bb_lag4 ELSE NULL
         END bb_lag,

         CASE v.reqd_lag WHEN 1 THEN u.ibb_lag1
                         WHEN 2 THEN u.ibb_lag2
                         WHEN 3 THEN u.ibb_lag3
                         WHEN 4 THEN u.ibb_lag4 ELSE NULL
         END ibb_lag,

         CASE v.reqd_lag WHEN 1 THEN u.hbp_lag1
                         WHEN 2 THEN u.hbp_lag2
                         WHEN 3 THEN u.hbp_lag3
                         WHEN 4 THEN u.hbp_lag4 ELSE NULL
         END hbp_lag,

         CASE v.reqd_lag WHEN 1 THEN u.bu_lag1
                         WHEN 2 THEN u.bu_lag2
                         WHEN 3 THEN u.bu_lag3
                         WHEN 4 THEN u.bu_lag4 ELSE NULL
         END bu_lag,

         CASE v.reqd_lag WHEN 1 THEN u.hr_lag1
                         WHEN 2 THEN u.hr_lag2
                         WHEN 3 THEN u.hr_lag3
                         WHEN 4 THEN u.hr_lag4 ELSE NULL
         END hr_lag,

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

    FROM lags_pit u,

         (SELECT t.fg_id,
                 t.season,
                 CASE WHEN t.ld_lag1 + t.fb_lag1 - t.iffb_lag1 >= 300
                      THEN 1
                      ELSE CASE WHEN t.ld_lag2 + t.fb_lag2 - t.iffb_lag2 >= 300
                                THEN 2
                                ELSE CASE WHEN t.ld_lag3 + t.fb_lag3 - t.iffb_lag3 >= 300
                                          THEN 3
                                          ELSE CASE WHEN t.ld_lag4 + t.fb_lag4 - t.iffb_lag4 >= 300
                                                    THEN 4
                                                    ELSE NULL
                                               END
                                     END
                           END
                 END reqd_lag
            FROM lags_pit t) v,

         fg_pit w

   WHERE     1 = 1
         AND u.fg_id = v.fg_id
         AND u.fg_id = w.fg_id
         AND u.season = v.season
         AND u.season = w.season
         AND v.reqd_lag IS NOT NULL
         AND w.line_drvs + w.fly_balls - w.infld_flys >= 200
