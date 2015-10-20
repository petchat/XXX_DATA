# -*- coding: utf-8 -*-
from __future__ import division
__author__ = 'jiusi'

import json


def load_json(path):
    with open(path, 'r') as f:
        j = json.loads(f.read())

        return j


def calculate_slot(key, step, keys, steps, j):
    buckets = []

    j = sorted(j, key=lambda k:k[key]['data'])

    for start in xrange(0, int(j[-1][key]['data'] + 1), step):
        bucket = []
        for data in j:
            if start <= data[key]['data'] < start + step:
                bucket.append(data)

        buckets.append(bucket)
    counters = [len(b) for b in buckets]
    counters = [ele / sum(counters) for ele in counters]
    print 'key:', key, 'step:', step, 'distri:', counters


    for k, s in zip(keys, steps):
        dis4buckets=[]
        print 'k:', k, 's:', s
        for bucket in buckets:
            if (len(bucket) == 0):
                print 'bucket is empty'
                continue

            bucket = sorted(bucket, key=lambda kk: kk[k])

            bs = []

            for start in xrange(0, int(bucket[-1][k]['data'] + 1), s):
                b=[]
                for data in bucket:
                    if start <= data[k]['data'] < start + s:
                        b.append(data)
                bs.append(b)

            counters = [len(b) for b in bs]
            counters = [ele / sum(counters) for ele in counters]
            print counters
            dis4buckets.append(counters)

        print dis4buckets


# NLS age, ZJZYDS hospital time, ZYFYZJ cost,

keymap={
    'age':'NLS',
    'time':'ZJZYDS',
    'cost':'ZYFYZJ'
}

def correctType(arr):
    refined = []
    for ele in arr:

        try:

            if 'NLS' in ele:
                ele['NLS']['data'] = int(ele['NLS']['data'])
            if 'ZJZYDS' in ele:
                ele['ZJZYDS']['data'] = int(ele['ZJZYDS']['data'])
            if 'ZYFYZJ' in ele:
                try:
                    ele['ZYFYZJ']['data'] = float(ele['ZYFYZJ']['data'].split(' ')[0])
                except ValueError:
                    ele['ZYFYZJ']['data'] = 0

            refined.append(ele)
        except ValueError:
            continue

    return refined

if __name__ == '__main__':
    j = load_json('/Users/jiusi/Desktop/refined.json')
    j = correctType(j)
    j_1 = load_json('/Users/jiusi/Desktop/refined_1.json')
    j_1 = correctType(j_1)


    # key = keymap['age']
    # keys = [keymap['time'], keymap['cost']]
    # step = 10
    # steps = [3, 1000]
    #
    # calculate_slot(key, step, keys, steps, j)

    # key = keymap['time']
    # keys = [keymap['age'], keymap['cost']]
    # step = 3
    # steps = [10, 1000]
    #
    # calculate_slot(key, step, keys, steps, j)

    key = keymap['cost']
    keys = [keymap['age'], keymap['time']]
    step = 1000
    steps = [10, 3]

    calculate_slot(key, step, keys, steps, j)
