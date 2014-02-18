  SELECT u.fg_id,
         u.name,
         u.season,
         w.tbf,
         w.fp_str,
         w.sw_str,
         w.balls,
         w.strikes,
         w.pitches,
         w.z_sw_cont,
         w.z_sw_miss,
         w.z_look,
         w.o_sw_cont,
         w.o_sw_miss,
         w.o_look,
         v.reqd_lag,

         CASE v.reqd_lag WHEN 1 THEN u.tbf1
                         WHEN 2 THEN u.tbf2
                         WHEN 3 THEN u.tbf3
                         WHEN 4 THEN u.tbf4 ELSE NULL
         END tbf_lag,

         CASE v.reqd_lag WHEN 1 THEN u.fp_str1
                         WHEN 2 THEN u.fp_str2
                         WHEN 3 THEN u.fp_str3
                         WHEN 4 THEN u.fp_str4 ELSE NULL
         END fp_str_lag,

         CASE v.reqd_lag WHEN 1 THEN u.sw_str1
                         WHEN 2 THEN u.sw_str2
                         WHEN 3 THEN u.sw_str3
                         WHEN 4 THEN u.sw_str4 ELSE NULL
         END sw_str_lag,

         CASE v.reqd_lag WHEN 1 THEN u.balls1
                         WHEN 2 THEN u.balls2
                         WHEN 3 THEN u.balls3
                         WHEN 4 THEN u.balls4 ELSE NULL
         END balls_lag,

         CASE v.reqd_lag WHEN 1 THEN u.strikes1
                         WHEN 2 THEN u.strikes2
                         WHEN 3 THEN u.strikes3
                         WHEN 4 THEN u.strikes4 ELSE NULL
         END strikes_lag,

         CASE v.reqd_lag WHEN 1 THEN u.pitches1
                         WHEN 2 THEN u.pitches2
                         WHEN 3 THEN u.pitches3
                         WHEN 4 THEN u.pitches4 ELSE NULL
         END pitches_lag,

         CASE v.reqd_lag WHEN 1 THEN u.z_sw_cont1
                         WHEN 2 THEN u.z_sw_cont2
                         WHEN 3 THEN u.z_sw_cont3
                         WHEN 4 THEN u.z_sw_cont4 ELSE NULL
         END z_sw_cont_lag,

         CASE v.reqd_lag WHEN 1 THEN u.z_sw_miss1
                         WHEN 2 THEN u.z_sw_miss2
                         WHEN 3 THEN u.z_sw_miss3
                         WHEN 4 THEN u.z_sw_miss4 ELSE NULL
         END z_sw_miss_lag,

         CASE v.reqd_lag WHEN 1 THEN u.z_look1
                         WHEN 2 THEN u.z_look2
                         WHEN 3 THEN u.z_look3
                         WHEN 4 THEN u.z_look4 ELSE NULL
         END z_look_lag,

         CASE v.reqd_lag WHEN 1 THEN u.o_sw_cont1
                         WHEN 2 THEN u.o_sw_cont2
                         WHEN 3 THEN u.o_sw_cont3
                         WHEN 4 THEN u.o_sw_cont4 ELSE NULL
         END o_sw_cont_lag,

         CASE v.reqd_lag WHEN 1 THEN u.o_sw_miss1
                         WHEN 2 THEN u.o_sw_miss2
                         WHEN 3 THEN u.o_sw_miss3
                         WHEN 4 THEN u.o_sw_miss4 ELSE NULL
         END o_sw_miss_lag,

         CASE v.reqd_lag WHEN 1 THEN u.o_look1
                         WHEN 2 THEN u.o_look2
                         WHEN 3 THEN u.o_look3
                         WHEN 4 THEN u.o_look4 ELSE NULL
         END o_look_lag

    FROM lags_pfx u,

         (SELECT t.fg_id,
                 t.season,
                 CASE WHEN t.z_sw_cont1 + t.z_sw_miss1 >= 400
                      THEN 1
                      ELSE CASE WHEN t.z_sw_cont2 + t.z_sw_miss2 >= 400
                                THEN 2
                                ELSE CASE WHEN t.z_sw_cont3 + t.z_sw_miss3 >= 400
                                          THEN 3
                                          ELSE CASE WHEN t.z_sw_cont4 + t.z_sw_miss4 >= 400
                                                    THEN 4
                                                    ELSE NULL
                                               END
                                     END
                           END
                 END reqd_lag
            FROM lags_pfx t) v,

         pfx_tot w

   WHERE     1 = 1
         AND u.fg_id = v.fg_id
         AND u.fg_id = w.fg_id
         AND u.season = v.season
         AND u.season = w.season
         AND v.reqd_lag IS NOT NULL
         AND w.z_sw_cont + w.z_sw_miss >= 400
