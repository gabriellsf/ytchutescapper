import os
import re
from pymongo import MongoClient
from pymongo import errors as mongo_exception

client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin')
db=client[os.environ['MONGODB_DATABASE']]

pattern = re.compile('/channel/(.+?)/')

channel_collection = db['channel']

dir = "./data/video/none/list_channel/"
files =  os.listdir(dir)
for file in files:
    with open(dir + file, "r") as data:
        text = data.read()
        all_matches = re.findall(pattern, text)

        for i, match in enumerate(all_matches):
            try:
                channel_collection.insert_one({
                    "_id": match,
                    "scrapped": False
                })         
            except mongo_exception.DuplicateKeyError:
                # skip document because it already exists in new collection
                continue        
    print(channel_collection.count_documents({"scrapped": False}))

