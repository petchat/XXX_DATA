# -*- coding: utf-8 -*-
from __future__ import division

__author__ = 'jiusi'

import json
import requests


def load_json(path):
    with open(path, 'r') as f:
        j = json.loads(f.read())

        return j


def savejson(data, path):
    with open(path, 'w') as f:
        j = json.dumps(data)

        f.write(j)


def calculate_slot(key, step, keys, steps, j):
    buckets = []

    j = sorted(j, key=lambda k: k[key]['data'])

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
        dis4buckets = []
        print 'k:', k, 's:', s
        for bucket in buckets:
            if (len(bucket) == 0):
                print 'bucket is empty'
                continue

            bucket = sorted(bucket, key=lambda kk: kk[k])

            bs = []

            for start in xrange(0, int(bucket[-1][k]['data'] + 1), s):
                b = []
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

keymap = {
    'age': 'NLS',
    'time': 'ZJZYDS',
    'cost': 'ZYFYZJ',
    'address': 'LXRDZ'  # AN
}


def correctType(arr):
    refined = []
    for ele in arr:

        for k in ele.keys():
            ele[k]['msg'] = ele[k]['msg'].encode('utf-8')

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

            ele['B_ID']['data'] = ele['B_ID']['data'].encode('utf-8').replace('\xc2\xa0', ' ').strip()

            if 'BAH' in ele:
                ele['BAH']['data'] = ele['BAH']['data'].strip().encode('utf-8')
            else:
                print 'no BAH:', ele

            if 'address' in ele:
                ele['address']['data'] = ele['address']['data'].encode('utf-8').replace('\xc2\xa0', ' ').strip()


            refined.append(ele)
        except ValueError:
            print 'bad data:', ele['B_ID']
            continue

    return refined


def print_distributions(j, j_1):
    key = keymap['age']
    keys = [keymap['time'], keymap['cost']]
    step = 10
    steps = [3, 1000]

    calculate_slot(key, step, keys, steps, j)

    key = keymap['time']
    keys = [keymap['age'], keymap['cost']]
    step = 3
    steps = [10, 1000]

    calculate_slot(key, step, keys, steps, j)

    key = keymap['cost']
    keys = [keymap['age'], keymap['time']]
    step = 1000
    steps = [10, 3]

    calculate_slot(key, step, keys, steps, j)


BID4MAP = {
    "冠心病": [
        "1500120",
        "0000037438",
        "0000043075",
        "0000039463",
        "0000041174",
        "0000757953"
    ],
    "脑梗塞": [
        "131530",
        "1404356",
        "99368",
        "41241",
        "110780",
        "2012018697",
        "2012009001",
        "0000037064",
        "0000034648"
    ],

    "高血压":
        [
            "1410351",
            "1309899",
            "1303888",
            "1303888",
            "1413193",
            "2012016266"
        ]
}


def getIllType(bid):
    for key in BID4MAP.keys():
        bids = BID4MAP[key]

        if bid in bids:
            return key


def getMapMeta(bid4map, j):
    metas = []

    bids = []
    for key in bid4map.keys():
        bs = bid4map[key]
        for b in bs:
            bids.append(b)

    for ele in j:
        for bid in bids:
            if ele['BAH']['data'] == bid:

                try:
                    geo = getLocation(ele['address']['data'])['result']['location']
                except Exception:
                    print 'bad addr:', ele['address']
                    geo = {}

                m = {
                    'age': ele['NLS']['data'],
                    'cost': ele['ZYFYZJ']['data'],
                    'sex': ele['XB']['data'],
                    'hospital': ele['duns']['data'],
                    'location': geo,
                    'address': ele['address']['data'],
                    'illness': ele['MZZDMC']['data'],
                    'illnessType': getIllType(bid)
                }
                metas.append(m)

    savejson(metas, '/Users/jiusi/Desktop/mapMeta.json')
    return metas


def testfind(j):
    for ele in j:
        # if ele['B_ID']['data'] == '2012018697':
        #     print ele
        print ele['B_ID']['data']


def getLocation(address):
    url = "http://api.map.baidu.com/geocoder?address=%s&output=json&key=8cb976834235d8cbcde2dce4835ae191&city=西安市"
    com = url % (address)

    r = requests.get(com)
    return r.json()


def getHospitalAddress(path, outpath):

    with open(path, 'r') as f:
        d = json.loads(f.read())


    for ele in d:
        hosStr = ele['hospital'].encode('utf-8')
        try:
            geo = getLocation(hosStr)['result']['location']
        except Exception:
            geo = {}
            print 'fucked hospital:', hosStr

        ele['hospitalLocation'] = geo

    savejson(d, outpath)


if __name__ == '__main__':
    # j = load_json('/Users/jiusi/Desktop/refined.json')
    # j = correctType(j)
    # j_1 = load_json('/Users/jiusi/Desktop/refined_1.json')
    # j_1 = correctType(j_1)


    # l = getMapMeta(BID4MAP, j)
    # print l
    #
    # add = '陕西省西安市长安区郭杜镇南街1号'
    # print getLocation(add)

    getHospitalAddress('/Users/jiusi/Desktop/mapMeta_refined.json', '/Users/jiusi/Desktop/mapMeta_withHos.json')
