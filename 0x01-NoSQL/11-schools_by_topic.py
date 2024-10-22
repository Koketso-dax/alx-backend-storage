#!/usr/bin/env python3
"""
Return items with specific topic
"""
from pymongo.collection import Collection
from typing import List, Dict


def schools_by_topic(mongo_collection: Collection, topic: str) -> List[Dict]:
    """
    Returns the list of schools having a specific topic.
    """
    return [doc for doc in mongo_collection.find({'topics': topic})]
