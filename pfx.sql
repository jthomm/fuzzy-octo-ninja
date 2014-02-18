CREATE TABLE pfx_pct AS
  SELECT fg_id,
         name,
         season,
         tb_faced tbf,
         1.0*f_strike/100 fp_str,
         1.0*sw_strike/100 sw_str,
         balls,
         strikes,
         pitches,
         1.0*(zone/100)*(z_swing/100)*(z_contact/100) z_sw_cont,
         1.0*(zone/100)*(z_swing/100)*(1 - z_contact/100) z_sw_miss,
         1.0*(zone/100)*(1 - z_swing/100) z_look,
         1.0*(1 - zone/100)*(o_swing/100)*(o_contact/100) o_sw_cont,
         1.0*(1 - zone/100)*(o_swing/100)*(1 - o_contact/100) o_sw_miss,
         1.0*(1 - zone/100)*(1 - o_swing/100) o_look
    FROM fg_pit
   WHERE     1 = 1
         AND o_swing IS NOT NULL
         AND z_swing IS NOT NULL
         AND swing IS NOT NULL
         AND o_contact IS NOT NULL
         AND z_contact IS NOT NULL
         AND contact IS NOT NULL
         AND zone IS NOT NULL
ORDER BY season DESC,
         tb_faced DESC
;


CREATE TABLE pfx_tot AS
  SELECT fg_id,
         name,
         season,
         tbf,
         ROUND (fp_str*tbf, 0) fp_str,
         ROUND (sw_str*pitches, 0) sw_str,
         balls,
         strikes,
         pitches,
         ROUND (z_sw_cont*pitches, 0) z_sw_cont,
         ROUND (z_sw_miss*pitches, 0) z_sw_miss,
         ROUND (z_look*pitches, 0) z_look,
         ROUND (o_sw_cont*pitches, 0) o_sw_cont,
         ROUND (o_sw_miss*pitches, 0) o_sw_miss,
         ROUND (o_look*pitches, 0) o_look
    FROM pfx_pct
;
