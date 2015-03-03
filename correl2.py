from connect import connect
connection, cursor = connect('fbb')

data = cursor.execute("""
  SELECT t.*,
         u.*
    FROM bar t,
         bar u
   WHERE     t.fg_id = u.fg_id
         AND t.year = u.year + 1
         AND t.pa >= 250
         AND u.pa >= 250
""").fetchall()

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
    #u'sofb',
    u'ofb',
    u'ifb',
)


results = list()
for i in xrange(1, len(stats) + 1):
    for n, r, p, numer, denom in run(i):
        results.append((n, r, p, len(numer), len(denom),) + binary_subset(numer, stats) + binary_subset(denom, stats))
    log('done...')


numer_cols = ['n_{0}'.format(stat) for stat in stats]
denom_cols = ['d_{0}'.format(stat) for stat in stats]

fd = pd.DataFrame(data=results, columns=['n', 'r', 'p', 'numer', 'denom',] + numer_cols + denom_cols)
fd['numer'] = sum(fd[col] for col in numer_cols)
fd['denom'] = sum(fd[col] for col in denom_cols)

