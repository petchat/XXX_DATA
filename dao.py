__author__ = 'jiusi'

from pymongo import MongoClient





def get_prescription(bId):
    return db.Prescription.find({'bId': bId})


def all_bId():
    return db.Prescription.distinct('bId')


def get_valid_prescriptions():
    return db.Prescription.find({
        'itemPrice': {'$exists': True},
        'itemCount': {'$exists': True},
        'bId': {'$exists': True}
    })