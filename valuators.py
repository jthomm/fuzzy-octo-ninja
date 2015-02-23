from __future__ import division


class BatBbm(object):

    def __init__(self, data):
        self.data = data

    @property
    def ab(self):
        return self.data['at_bats']

    @property
    def h(self):
        return self.data['singles'] + \
               self.data['doubles'] + \
               self.data['triples'] + \
               self.data['home_runs']

    @property
    def g(self):
        return self.data['games']

    @property
    def hr(self):
        return self.data['home_runs']

    @property
    def rbi(self):
        return self.data['rbi']

    @property
    def sb(self):
        return self.data['stolen_bases']

    @property
    def r(self):
        return self.data['runs_scored']

    @property
    def ba(self):
        return self.h/(1.0*self.ab)


class BatTotal(object):

    #HR_M = 0.1132
    #HR_B = -2.0622
    HR_M = 0.1089
    HR_B = -1.7513

    #RBI_M = 0.0461
    #RBI_B = -3.258
    RBI_M = 0.0463
    RBI_B = -3.1111

    #SB_M = 0.0825
    #SB_B = -0.9473
    SB_M = 0.0827
    SB_B = -0.9996

    #R_M = 0.065
    #R_B = -4.7858
    R_M = 0.0613
    R_B = -4.3763

    #BA_P = 1/13.0
    #BA_Q = 0.278
    BA_P = 14/183.0
    BA_Q = 0.2778

    @property
    def hr_v(self):
        return self.HR_M*self.hr + self.HR_B

    @property
    def rbi_v(self):
        return self.RBI_M*self.rbi + self.RBI_B

    @property
    def sb_v(self):
        return self.SB_M*self.sb + self.SB_B

    @property
    def r_v(self):
        return self.R_M*self.r + self.R_B

    @property
    def ba_v(self):
        return self.BA_P*self.ab*(self.ba - self.BA_Q)


class BatPerGame(object):

    HR_M = 15.05
    HR_B = -2.2128

    RBI_M = 7.2198
    RBI_B = -3.7077

    SB_M = 6.8097
    SB_B = -0.643

    R_M = 9.495
    R_B = -5.1474

    #BA_P = 1/0.093
    #BA_Q = 0.283
    BA_P = 10.65
    BA_Q = 0.2818

    @property
    def hr_v(self):
        return self.HR_M*(self.hr/self.g) + self.HR_B

    @property
    def rbi_v(self):
        return self.RBI_M*(self.rbi/self.g) + self.RBI_B

    @property
    def sb_v(self):
        return self.SB_M*(self.sb/self.g) + self.SB_B

    @property
    def r_v(self):
        return self.R_M*(self.r/self.g) + self.R_B

    @property
    def ba_v(self):
        return self.BA_P*(self.ab/self.g)*(self.ba - self.BA_Q)


class BatBbmTotal(BatBbm, BatTotal):
    pass


class BatBbmPerGame(BatBbm, BatPerGame):
    pass


class PitBbm(object):

    def __init__(self, data):
        self.data = data

    @property
    def g(self):
        return self.data['games']

    @property
    def er(self):
        return self.data['runs_earned']

    @property
    def bb(self):
        return self.data['bases_on_balls']

    @property
    def h(self):
        return self.data['hits_allowed']

    @property
    def ip(self):
        return self.data['innings']

    @property
    def w(self):
        return self.data['wins']

    @property
    def sv(self):
        return self.data['saves']

    @property
    def era(self):
        return 9*self.er/self.ip

    @property
    def whip(self):
        return (self.bb + self.h)/self.ip

    @property
    def so(self):
        return self.data['strikeouts_pitched']


class PitTotal(object):

    W_M = 0.2056
    W_B = -2.0082

    SV_M = 0.0623
    SV_B = -0.6037

    ERA_P = 1/87.0
    ERA_Q = 3.2

    WHIP_P = 1/18.0
    WHIP_Q = 1.1447

    SO_M = 0.0178
    SO_B = -2.4163

    @property
    def w_v(self):
        return self.W_M*self.w + self.W_B

    @property
    def sv_v(self):
        return self.SV_M*self.sv + self.SV_B

    @property
    def era_v(self):
        return self.ERA_P*self.ip*(self.ERA_Q - self.era)

    @property
    def whip_v(self):
        return self.WHIP_P*self.ip*(self.WHIP_Q - self.whip)

    @property
    def so_v(self):
        return self.SO_M*self.so + self.SO_B


class PitPerGame(object):

    W_M = 5.6022
    W_B = -1.9762

    SV_M = 4.214
    SV_B = -0.4692

    ERA_P = 1/3.73
    ERA_Q = 3.07

    WHIP_P = 1.656
    WHIP_Q = 1.14

    SO_M = 0.5047
    SO_B = -2.336

    @property
    def w_v(self):
        return self.W_M*self.w/self.g + self.W_B

    @property
    def sv_v(self):
        return self.SV_M*self.sv/self.g + self.SV_B

    @property
    def era_v(self):
        return self.ERA_P*(self.ip/self.g)*(self.ERA_Q - self.era)

    @property
    def whip_v(self):
        return self.WHIP_P*(self.ip/self.g)*(self.WHIP_Q - self.whip)

    @property
    def so_v(self):
        return self.SO_M*self.so/self.g + self.SO_B


class PitBbmTotal(PitBbm, PitTotal):
    pass


class PitBbmPerGame(PitBbm, PitPerGame):
    pass


"""
import sqlite3
from collections import OrderedDict

def unique_key(dct, key):
    if key in dct:
        return unique_key(dct, '_{0}'.format(key))
    else:
        return key

def ordered_dict_factory(cursor, row):
    dct = OrderedDict()
    for i, column_name in enumerate(cursor.description):
        key = unique_key(dct, column_name[0])
        dct[key] = row[i]
    return dct

n = sqlite3.connect('fbb')
n.row_factory = ordered_dict_factory

c = n.cursor()







c.execute('''
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
''')

data = c.fetchall()

from valuators import BatBbmTotal, BatBbmPerGame

for d in data:
    tv = BatBbmTotal(d)
    d['hr_tv'] = tv.hr_v
    d['rbi_tv'] = tv.rbi_v
    d['sb_tv'] = tv.sb_v
    d['r_tv'] = tv.r_v
    d['ba_tv'] = tv.ba_v
    pgv = BatBbmPerGame(d)
    d['hr_pgv'] = pgv.hr_v
    d['rbi_pgv'] = pgv.rbi_v
    d['sb_pgv'] = pgv.sb_v
    d['r_pgv'] = pgv.r_v
    d['ba_pgv'] = pgv.ba_v

import csv

file_name = 'bat_value.csv'

with open(file_name, 'wb') as tgt_file:
    w = csv.writer(tgt_file, quoting=csv.QUOTE_MINIMAL, delimiter=',')
    headers = data[0].keys()
    for row in data:
        w.writerow(row.values())







c.execute('''
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
         NULL quality_starts
    FROM pit_stmr t LEFT OUTER JOIN id_map v ON t.fg_id = v.fg_id
   WHERE t.h > 1
''')

data = c.fetchall()

from valuators import PitBbmTotal, PitBbmPerGame

for d in data:
    tv = PitBbmTotal(d)
    d['w_tv'] = tv.w_v
    d['sv_tv'] = tv.sv_v
    d['era_tv'] = tv.era_v
    d['whip_tv'] = tv.whip_v
    d['so_tv'] = tv.so_v
    pgv = PitBbmPerGame(d)
    d['w_pgv'] = pgv.w_v
    d['sv_pgv'] = pgv.sv_v
    d['era_pgv'] = pgv.era_v
    d['whip_pgv'] = pgv.whip_v
    d['so_pgv'] = pgv.so_v

import csv

file_name = 'pit_value.csv'

with open(file_name, 'wb') as tgt_file:
    w = csv.writer(tgt_file, quoting=csv.QUOTE_MINIMAL, delimiter=',')
    headers = data[0].keys()
    w.writerow(headers)
    for row in data:
        w.writerow(row.values())
"""
