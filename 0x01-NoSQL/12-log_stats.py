#!/usr/bin/env python3
""" View nginx logs stats """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # Number of documents in this collection
    num_logs = nginx_collection.count_documents({})
    print(f"{num_logs} logs")

    # Number of documents with each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        num_method = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {num_method}")

    # Number of documents with method=GET and path=/status
    num_status_check = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{num_status_check} status check")
