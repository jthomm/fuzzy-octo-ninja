CREATE TABLE lags_pfx AS

  SELECT fg_id,
         name,
         season,

         /* Lag of 1 year (i.e. previous year) */

         (  SELECT COUNT (*)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) seas_lag1,

         (  SELECT SUM (u.tbf)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) tbf1,

         (  SELECT SUM (u.fp_str)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) fp_str1,

         (  SELECT SUM (u.balls)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) balls1,

         (  SELECT SUM (u.strikes)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) strikes1,

         (  SELECT SUM (u.pitches)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) pitches1,

         (  SELECT SUM (u.sw_str)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) sw_str1,

         (  SELECT SUM (u.z_sw_cont)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) z_sw_cont1,

         (  SELECT SUM (u.z_sw_miss)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) z_sw_miss1,

         (  SELECT SUM (u.z_look)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) z_look1,

         (  SELECT SUM (u.o_sw_cont)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) o_sw_cont1,

         (  SELECT SUM (u.o_sw_miss)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) o_sw_miss1,

         (  SELECT SUM (u.o_look)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 2) o_look1,

         /* Lag of 2 years (i.e. previous 2 years) */

         (  SELECT COUNT (*)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) seas_lag2,

         (  SELECT SUM (u.tbf)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) tbf2,

         (  SELECT SUM (u.fp_str)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) fp_str2,

         (  SELECT SUM (u.balls)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) balls2,

         (  SELECT SUM (u.strikes)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) strikes2,

         (  SELECT SUM (u.pitches)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) pitches2,

         (  SELECT SUM (u.sw_str)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) sw_str2,

         (  SELECT SUM (u.z_sw_cont)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) z_sw_cont2,

         (  SELECT SUM (u.z_sw_miss)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) z_sw_miss2,

         (  SELECT SUM (u.z_look)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) z_look2,

         (  SELECT SUM (u.o_sw_cont)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) o_sw_cont2,

         (  SELECT SUM (u.o_sw_miss)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) o_sw_miss2,

         (  SELECT SUM (u.o_look)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 3) o_look2,

         /* Lag of 3 years (i.e. previous 3 years) */

         (  SELECT COUNT (*)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) seas_lag3,

         (  SELECT SUM (u.tbf)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) tbf3,

         (  SELECT SUM (u.fp_str)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) fp_str3,

         (  SELECT SUM (u.balls)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) balls3,

         (  SELECT SUM (u.strikes)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) strikes3,

         (  SELECT SUM (u.pitches)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) pitches3,

         (  SELECT SUM (u.sw_str)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) sw_str3,

         (  SELECT SUM (u.z_sw_cont)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) z_sw_cont3,

         (  SELECT SUM (u.z_sw_miss)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) z_sw_miss3,

         (  SELECT SUM (u.z_look)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) z_look3,

         (  SELECT SUM (u.o_sw_cont)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) o_sw_cont3,

         (  SELECT SUM (u.o_sw_miss)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) o_sw_miss3,

         (  SELECT SUM (u.o_look)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 4) o_look3,

         /* Lag of 4 years (i.e. previous 4 years) */


         (  SELECT COUNT (*)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) seas_lag4,

         (  SELECT SUM (u.tbf)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) tbf4,

         (  SELECT SUM (u.fp_str)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) fp_str4,

         (  SELECT SUM (u.balls)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) balls4,

         (  SELECT SUM (u.strikes)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) strikes4,

         (  SELECT SUM (u.pitches)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) pitches4,

         (  SELECT SUM (u.sw_str)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) sw_str4,

         (  SELECT SUM (u.z_sw_cont)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) z_sw_cont4,

         (  SELECT SUM (u.z_sw_miss)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) z_sw_miss4,

         (  SELECT SUM (u.z_look)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) z_look4,

         (  SELECT SUM (u.o_sw_cont)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) o_sw_cont4,

         (  SELECT SUM (u.o_sw_miss)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) o_sw_miss4,

         (  SELECT SUM (u.o_look)
              FROM pfx_tot u
             WHERE     1 = 1
                   AND t.fg_id = u.fg_id
                   AND u.season < t.season
                   AND u.season > t.season - 5) o_look4

    FROM pfx_tot t
;
