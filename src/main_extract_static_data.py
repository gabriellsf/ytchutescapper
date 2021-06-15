import os
import re
from datetime import datetime

## INICIO DB Externalizar em outro arquivo
from pymongo import MongoClient
from pymongo import errors as mongo_exception
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin')
db=client[os.environ['MONGODB_DATABASE']]

#FIM DB

category = ['news','science','animation','arts','vehicles','beauty','finance','cuisine','diy',
        'education','entertainment','gaming','health','music','family','animals','spirituality',
        'vlogging','travel','sport']


channel_pattern = re.compile('/channel/(.+?)/')
title_pattern = re.compile('<title>(.+)</title>', re.MULTILINE | re.DOTALL)
youtube_channel_id_pattern = re.compile('https://www\.youtube\.com/channel/(.+?)/videos')
youtube_channel_user_pattern = re.compile('https://www\.youtube\.com/user/(.+?)[\"|/|<|?:\s+|$]')
youtube_channel_user_pattern_2 = re.compile('https://www\.youtube\.com/c/(.+?)[\"|/|<|?:\s+|$]')
youtube_video_id_pattern = re.compile('https://www\.youtube\.com/watch\?v=(.+?)[\"|/|<|?:\s+|$]')
date_pattern = re.compile('First published at(.+)')
sensitivity_pattern = re.compile('<tr><td>Sensitivity</td><td><a href="https://support.bitchute.com/policy/guidelines/#content-sensitivity" target="_blank" rel="noopener noreferrer">(.+?)</a></td></tr>')

video_collection = db['video']
channel_collection = db['channel']

for c in category:
    dir = "./data/video/" + c + "/page/"
    print(dir)
    files =  os.listdir(dir)
    for file in files:
        print(file)
        with open(dir + file, "r") as data:
            text = data.read()
            channel_matches = re.findall(channel_pattern,text) 
            title_matches = re.findall(title_pattern,text) 
            youtube_channel_id_matches = re.findall(youtube_channel_id_pattern,text) 

            youtube_channel_user_matches = re.findall(youtube_channel_user_pattern,text) 
            youtube_channel_user_matches.extend(re.findall(youtube_channel_user_pattern_2,text))

            youtube_video_id_matches = re.findall(youtube_video_id_pattern,text) 
            date_matches = re.findall(date_pattern,text) 
            sensitivity_matches = re.findall(sensitivity_pattern,text) 

                
            video_collection.update_one({"_id": os.path.splitext(file)[0]},{ '$set': {
                "static_data": True,
                "channel": channel_matches[0],
                "title": title_matches[0],
                "youtube_channel_id": list(set(youtube_channel_id_matches)),
                "youtube_channel_name": list(set(youtube_channel_user_matches)),
                "youtube_video_id": list(set(youtube_video_id_matches)),
                "video_publish_date": date_matches[0],
                "sensitivity": sensitivity_matches[0],
                "lastModified_static_data": datetime.now()
            }})

            try:
                channel_collection.insert_one({
                    "_id": channel_matches[0],
                    "scrapped": False
                })         
            except mongo_exception.DuplicateKeyError:
                # skip document because it already exists in new collection
                continue 
                