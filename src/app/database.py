from pymongo import MongoClient
import os

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'])
db=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")


print(serverStatusResult)