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


class BatterTable(object):
    #
    URL = 'http://razzball.com/steamer-hitter-projections/'
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
        return self.soup.find_all('tr')[3:-10]


class Batter(object):
    #
    attrs = ('fg_id', 'name', 'team', 'pos',
             'g', 'pa', 'ab', 'r', 'hr', 'rbi',
             'sb', 'h', 'b1', 'b2', 'b3', 'tb',
             'so', 'bb', 'hbp', 'sf', 'cs',)
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
        return u'/'.join(self.tds[5].text.split(', '))
    #
    @property
    def g(self):
        return int(self.tds[6].text)
    #
    @property
    def pa(self):
        return int(self.tds[7].text)
    #
    @property
    def ab(self):
        return int(self.tds[8].text)
    #
    @property
    def r(self):
        return float(self.tds[9].text)
    #
    @property
    def hr(self):
        return float(self.tds[10].text)
    #
    @property
    def rbi(self):
        return float(self.tds[11].text)
    #
    @property
    def sb(self):
        return float(self.tds[12].text)
    #
    @property
    def h(self):
        return float(self.tds[13].text)
    #
    @property
    def b1(self):
        return float(self.tds[14].text)
    #
    @property
    def b2(self):
        return float(self.tds[15].text)
    #
    @property
    def b3(self):
        return float(self.tds[16].text)
    #
    @property
    def tb(self):
        return float(self.tds[17].text)
    #
    @property
    def so(self):
        return float(self.tds[18].text)
    #
    @property
    def bb(self):
        return float(self.tds[19].text)
    #
    @property
    def hbp(self):
        return float(self.tds[20].text)
    #
    @property
    def sf(self):
        return float(self.tds[21].text)
    #
    @property
    def cs(self):
        return float(self.tds[22].text)
    #
    def as_dict(self):
        return OrderedDict((attr, getattr(self, attr)) for attr in self.attrs)


"""
df['hr_val'] = 0.1089*df['hr'] - 1.7513
df['rbi_val'] = 0.0463*df['rbi'] - 3.1111
df['sb_val'] = 0.0827*df['sb'] - 0.9996
df['r_val'] = 0.0613*df['r'] - 4.3763
df['ba_val'] = 0.0787*df['h'] - 0.0219*df['ab']

df['xval'] = -0.0044*df['ab'] \
             +0.0157*df['h'] \
             +0.0123*df['r'] \
             +0.0218*df['hr'] \
             +0.0093*df['rbi'] \
             +0.0165*df['sb'] \
             -2.0477
"""

if __name__ == '__main__':
    bt = BatterTable()
    batters = [Batter(tr).as_dict() for tr in bt.get_trs()]
    with open('bat_razz.csv', 'wb') as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter=',')
        w.writerow(batters[0].keys())
        for batter in batters:
            try:
                w.writerow(batter.values())
            except UnicodeEncodeError:
                batter
