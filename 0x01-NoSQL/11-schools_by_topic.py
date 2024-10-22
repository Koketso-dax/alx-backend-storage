#!/usr/bin/python3
"""
Return items with specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns list of schools with specified topic
    """
    topic_filter = {
        'topics': {
            'topics': {
                '$elemMatch': {
                    '$eq': topic
                }
            }
        }
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
