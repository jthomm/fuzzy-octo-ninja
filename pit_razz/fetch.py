import requests
from bs4 import BeautifulSoup as Soup
from collections import OrderedDict
import csv

import sqlite3
n = sqlite3.connect('../fbb')
c = n.cursor()

fg_ids = {}
for row in c.execute('SELECT fg_id FROM id_map'):
    fg_ids[row[0]] = None;

from collections import defaultdict
fg_ids_by_name = defaultdict(list)
for row in c.execute('SELECT fg_id, fg_name FROM id_map'):
    fg_ids_by_name[row[1]].append(row[0])

class PitcherTable(object):
    #
    URL = 'http://razzball.com/steamer-pitcher-projections/'
    #
    def __init__(self):
        self.soup = self.get_soup()
    #
    def get_html(self):
        return requests.get(self.URL).text
    #
    def get_soup(self):
        return Soup(self.get_html())
    #
    def get_trs(self):
        return self.soup.find_all('tr')[3:-9]


class Pitcher(object):
    #
    attrs = ('fg_id', 'name', 'team', 'pos',
             'g', 'gs', 'w', 'sv', 'ip', 'so',
             'bb', 'h', 'hbp', 'er', 'r', 'hr',
             'gb_pct', 'fb_pct', 'ld_pct', 'babip',)
    #
    def __init__(self, tr):
        self.tds = tr.find_all('td')
    #
    @property
    def fg_id(self):
        href = self.tds[1].a.attrs[u'href']
        bis_id = href.split('/')[2]
        if (bis_id in fg_ids):
            return bis_id
        else:
            possible_ids = fg_ids_by_name[self.name];
            return bis_id if len(possible_ids) != 1 else possible_ids[0]
    #
    @property
    def name(self):
        return self.tds[1].a.text.replace(u'\u2019', u"'")
    #
    @property
    def team(self):
        return self.tds[2].a.text
    #
    @property
    def pos(self):
        return u'/'.join(self.tds[3].text.split(', '))
    #
    @property
    def g(self):
        return int(self.tds[5].text)
    #
    @property
    def gs(self):
        return int(self.tds[6].text)
    #
    @property
    def w(self):
        return float(self.tds[9].text)
    #
    @property
    def sv(self):
        return int(self.tds[11].text)
    #
    @property
    def ip(self):
        return float(self.tds[8].text)
    #
    @property
    def so(self):
        return float(self.tds[16].text)
    #
    @property
    def bb(self):
        return float(self.tds[17].text)
    #
    @property
    def h(self):
        return float(self.tds[18].text)
    #
    @property
    def hbp(self):
        return float(self.tds[19].text)
    #
    @property
    def er(self):
        return float(self.tds[20].text)
    #
    @property
    def r(self):
        return float(self.tds[21].text)
    #
    @property
    def hr(self):
        return float(self.tds[22].text)
    #
    @property
    def gb_pct(self):
        return float(self.tds[23].text)
    #
    @property
    def fb_pct(self):
        return float(self.tds[24].text)
    #
    @property
    def ld_pct(self):
        return float(self.tds[25].text)
    #
    @property
    def babip(self):
        return float(self.tds[26].text)
    #
    def as_dict(self):
        return OrderedDict((attr, getattr(self, attr)) for attr in self.attrs)


"""
df['w_val'] = 0.1876*df['w'] - 1.8776
df['sv_val'] = 0.0653*df['sv'] - 0.5800
df['so_val'] = 0.0181*df['so'] - 2.4819
df['whip_val'] = 0.0611*df['ip'] - 0.0550*(df['bb'] + df['h'])
df['era_val'] = 0.327*df['ip'] - 0.1002*df['er']

df['xval'] = +0.0376*df['w'] \
             +0.0130*df['sv'] \
             +0.0036*df['so'] \
             +0.0188*df['ip'] \
             -0.0110*(df['bb'] + df['h']) \
             -0.0200*df['er'] \
             -0.9874
"""

if __name__ == '__main__':
    pt = PitcherTable()
    pitchers = [Pitcher(tr).as_dict() for tr in pt.get_trs()]
    with open('pit_razz.csv', 'wb') as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter=',')
        w.writerow(pitchers[0].keys())
        for pitcher in pitchers:
            try:
                w.writerow(pitcher.values())
            except UnicodeEncodeError:
                pitcher
