from __future__ import division

import sqlite3
from collections import OrderedDict

from scipy.stats.stats import pearsonr
from scipy.special import logit
from math import sqrt, exp

from itertools import combinations

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

con = sqlite3.connect('fbb')
con.row_factory = ordered_dict_factory

cur = con.cursor()

cur.execute('''
  SELECT t.*,
         u.*
    FROM bar t,
         bar u
   WHERE     t.fg_id = u.fg_id
         AND t.year = u.year + 1
         AND t.pa >= 400
         AND u.pa >= 400
''')

data = cur.fetchall()

stats = (
    'ubb',
    'ibb',
    'hbp',
    'so',
    'bu',
    'hrofb',
    'gb',
    'ld',
    'sofb',
    'ofb',
    'ifb',
)



class Memoize:
    #
    def __init__(self, f):
        self.f = f
        self.memo = {}
    #
    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


def take_sum(datum, stats):
    result = 0
    for stat in stats:
        result += datum[stat]
    return result

@Memoize
def take_all_sums(stats):
    return [take_sum(datum, stats) for datum in data]


def take_all_logits(numer, denom):
    numer_sums = take_all_sums(numer)
    denom_sums = take_all_sums(denom)
    results = list()
    for i, numer_sum in enumerate(numer_sums):
        denom_sum = denom_sums[i]
        result = None
        if denom_sum > 0 and numer_sum > 0 and numer_sum != denom_sum:
            result = logit(numer_sum/denom_sum)
        results.append(result)
    return results

def underscore(strings):
    return tuple('_{0}'.format(string) for string in strings)

def get_pearson_r(numer, denom):
    y0_logits = take_all_logits(numer, denom)
    y1_logits = take_all_logits(underscore(numer), underscore(denom))
    p = list()
    q = list()
    for i, y0_logit in enumerate(y0_logits):
        if y0_logit is not None:
            y1_logit = y1_logits[i]
            if y1_logit is not None:
                p.append(y0_logit)
                q.append(y1_logit)
    return pearsonr(p, q)



def generate_combos(num_numer, num_denom):
    for numer_comb in combinations(stats, num_numer):
        for denom_comb in combinations(stats, num_denom):
            has_all_numer = True
            for comb in numer_comb:
                if comb not in denom_comb:
                    has_all_numer = False
                    continue
            if has_all_numer:
                yield (numer_comb, denom_comb)



def generate_all_combos(i, j):
    for d in xrange(i, j):
        print 'working on denom size {0}'.format(d)
        for n in xrange(1, d):
            for ncomb, dcomb in generate_combos(n, d):
                result = get_pearson_r(ncomb, dcomb)
                row = [len(ncomb), len(dcomb), result[0], result[1],]
                for stat in stats:
                    row.append(1 if stat in ncomb else 0)
                for stat in stats:
                    row.append(1 if stat in dcomb else 0)
                ___ = cur.execute('INSERT INTO pa_cor (numer, denom, r, p, n_ubb, n_ibb, n_hbp, n_so, n_bu, n_hrofb, n_gb, n_ld, n_sofb, n_ofb, n_ifb, d_ubb, d_ibb, d_hbp, d_so, d_bu, d_hrofb, d_gb, d_ld, d_sofb, d_ofb, d_ifb) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
                #___ = cur.execute('INSERT INTO pa_cor2 (numer, denom, r, p, n_ubb, n_ibb, n_hbp, n_so, n_bu, n_hrofb, n_gb, n_ld, n_ofb, n_ifb, d_ubb, d_ibb, d_hbp, d_so, d_bu, d_hrofb, d_gb, d_ld, d_ofb, d_ifb) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
            print 'committing for numer size {0}'.format(n)
            con.commit()

generate_all_combos(2, 3)
