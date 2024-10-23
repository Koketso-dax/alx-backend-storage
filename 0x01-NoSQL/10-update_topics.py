#!/usr/bin/env python3
"""
Change all topics
"""


def update_topics(mongo_collection, name, topics):
    """ Changes all topics of collection's docs """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
