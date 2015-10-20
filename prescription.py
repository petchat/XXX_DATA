from __future__ import division
import dao


def test():
    print 'fuck'


def get_hospitalized_time(bId):
    cur = dao.get_prescription(bId)

    ps = cur[:]


    # ps = sorted(ps, key=ps['zxrq'])

    ps = sorted(ps, key=lambda k: k['zxrq'])

    start = ps[0]['zxrq']
    end = ps[-1]['zxrq']

    d = end - start
    return d.days * 24 + d.seconds / 3600


def gen_time_distribution():
    # get all id
    bIds = dao.all_bId()

    times = []
    # calculate time
    for bId in bIds:
        times.append(get_hospitalized_time(bId))

    # sort by time
    times = sorted(times)

    times = [ele for ele in times if ele < 8000]
    print 'avg hospi time:', sum(times) / len(times)

    # make distribution
    step = 72
    buckets = []

    for start in xrange(0, int(times[-1] + 1), step):
        crtBucket = []
        for time in times:
            if start <= time < start + step:
                crtBucket.append(time)

        buckets.append(crtBucket)

    counter = [len(bucket) for bucket in buckets]
    counter = [ele / sum(counter) for ele in counter]

    return counter


def getPatientCost():
    ps = dao.get_valid_prescriptions()

    # group by bid
    bidBucket = {}
    for p in ps:
        if p['bId'] not in bidBucket:
            bidBucket[p['bId']] = []
        bidBucket[p['bId']].append(p)

    # calculate total cost for patient
    costs = []
    for bid in bidBucket.keys():
        ps = bidBucket[bid]

        cost = sum([ele['itemPrice'] * ele['itemCount'] for ele in ps])
        costs.append({'bid': bid, 'cost': cost})

    costs = sorted(costs, key=lambda k: k['cost'])

    return costs


def getCostDistribution(patientCost):
    max = patientCost[-1]['cost']
    step = 500
    start = 0
    stop = start + step

    distribution = [0] * int((max + step) / step)

    # put into slots
    pci = 0
    for i in xrange(0, int(max + 1), step):
        start = i
        stop = i + step
        for j in range(pci, len(patientCost)):
            pc = patientCost[j]

            index = int(start / step)

            if start <= pc['cost'] < stop:
                distribution[index] += 1
            else:
                pci = j
                break

    return distribution


def genCostDistribution():
    costs = getPatientCost()

    print 'avg cost:', sum([c['cost'] for c in costs]) / len(costs)

    # get the bloody distribution
    step = 1000
    buckets = []
    for start in xrange(0, int(costs[-1]['cost'] + 1), step):
        bucket = []
        for c in costs:
            if start <= c['cost'] < start + step:
                bucket.append(c)
        buckets.append(bucket)

    counter = [len(bucket) for bucket in buckets]
    counter = [ele / sum(counter) for ele in counter]

    return counter


print gen_time_distribution()
# print getPatientCost()
# print genCostDistribution()