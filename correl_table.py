from connect import connect
connection, cursor = connect('fbb')

data = cursor.execute("""
  SELECT t.*,
         u.*
    FROM foo t,
         foo u
   WHERE     t.fg_id = u.fg_id
         AND t.year = u.year + 1
         AND t.pa >= 200
         AND u.pa >= 200
""").fetchall()


data = cursor.execute('''
  SELECT t.*, u.*
    FROM baz t, baz u
   WHERE t.fg_id = u.fg_id
     AND t.year = u.year - 1
     AND t.pa >= 200
     AND u.pa >= 200
''').fetchall()

import pandas as pd
df = pd.DataFrame(data=data, columns=data[0].keys())

import numpy as np
from scipy.special import logit
from scipy.stats import pearsonr

def sum_of(df, columns):
    return sum(df[column] for column in columns)

def underscore(columns):
    return [u'_{column}'.format(column=column) for column in columns]

def logit_of(df, numer, denom):
    return logit(sum_of(df, numer)/sum_of(df, denom))

def pearsonr_of(df, numer, denom):
    x = logit_of(df, numer, denom)
    y = logit_of(df, underscore(numer), underscore(denom))
    i = np.isfinite(x) & np.isfinite(y)
    n = len(i)
    r, p = pearsonr(x[i], y[i])
    return (n, r, p,)

def binary_subset(subset, superset):
    return tuple(1 if item in subset else 0 for item in superset)

import datetime

def log(message):
    print u'[{timestamp}] {message}'.format(
        timestamp=datetime.datetime.now().isoformat(),
        message=message)

from itertools import combinations

def run(number_of_denoms):
    log('Working on {0} denoms'.format(number_of_denoms))
    for denom in combinations(stats, number_of_denoms):
        for number_of_numers in xrange(1, len(denom)):
            for numer in combinations(denom, number_of_numers):
                n, r, p = pearsonr_of(df, numer, denom)
                yield (n, r, p, numer, denom,)

stats = (
    u'ubb',
    u'ibb',
    u'hbp',
    u'so',
    u'bu',
    u'gb',
    u'ld',
    u'hrofb',
    u'sofb',
    u'ofb',
    u'ifb',
)

stats = (
    'ubb',
    'ibb',
    'hbp',
    'so',
    'bu_hard',
    'bu_soft',
    'gb_hard',
    'gb_soft',
    'ld_hr',
    'ld_hard',
    'ld_soft',
    'offb_hr',
    'offb_hard',
    'offb_soft',
    'iffb',
)

numer_cols = ['n_{0}'.format(stat) for stat in stats]
denom_cols = ['d_{0}'.format(stat) for stat in stats]

new_results = [r[:3] + binary_subset(r[3], stats) + binary_subset(r[4], stats) for r in results]
fd = pd.DataFrame(data=new_results, columns=['n', 'r', 'p',] + numer_cols + denom_cols)
fd['numer'] = sum(fd[col] for col in numer_cols)
fd['denom'] = sum(fd[col] for col in denom_cols)


"""
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
    FROM foo t,
         foo u
   WHERE     t.fg_id = u.fg_id
         AND t.year = u.year + 1
         AND t.pa >= 400
         AND u.pa >= 400
''')

cur.execute('''
  SELECT t.*, u.*
    FROM baz t, baz u
   WHERE t.fg_id = u.fg_id
     AND t.year = u.year - 1
     AND t.pa >= 200
     AND u.pa >= 200
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

stats = (
    'ubb',
    'ibb',
    'hbp',
    'so',
    'bu_hard',
    'bu_med',
    'bu_soft',
    'gb_hard',
    'gb_med',
    'gb_soft',
    'ld_hr',
    'ld_hard',
    'ld_med',
    'ld_soft',
    'offb_hr',
    'offb_hard',
    'offb_med',
    'offb_soft',
    'iffb',
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
"""
