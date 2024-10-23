#!/usr/bin/env python3
""" Insert doc using python """


def insert_school(mongo_collection, **kwargs):
    """ Inserts new doc in collection """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
