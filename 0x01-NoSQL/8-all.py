#!/usr/bin/env python3
"""
Uses python function to list all docs
"""


def list_all(mongo_collection):
    """
    Lists all docs in collection.
    """
    return [doc for doc in mongo_collection.find()]
