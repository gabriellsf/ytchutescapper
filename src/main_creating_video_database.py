import os
import re
from pymongo import MongoClient
from pymongo import errors as mongo_exception
import time
from datetime import date


client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin')
db=client[os.environ['MONGODB_DATABASE']]

category = ['news','science','animation','arts','vehicles','beauty','finance','cuisine','diy',
        'education','entertainment','gaming','health','music','family','animals','spirituality',
        'vlogging','travel','sport']
type = ["popular","all"] 

pattern = re.compile('<span class=\\\\\"video-card-id hidden\\\\\">(.+?)<\/span>')
pattern_views = re.compile('<span class=\\\\\"video-views\\\\\"><i class=\\\\\"far fa-eye\\\\\"><\/i>(.+?)<\/span>')
pattern_duration = re.compile('<span class=\\\\\"video-duration\\\\\">(.+?)<\/span>')

video_collection = db['video']
while True:
    for t in type:
        for c in category:
            dir = "./data/video/" + c + "/list/" + date.today().strftime("%Y%m%d") + "/list_" + t +"/"
            print(dir)
            files =  os.listdir(dir)
            for file in files:
                with open(dir + file, "r") as data:
                    text = data.read()
                    all_matches = re.findall(pattern, text)
                    views_matches = re.findall(pattern_views, text)
                    duration_matches = re.findall(pattern_duration, text)
                    for i, match in enumerate(all_matches):
                        try:
                            video_collection.insert_one({
                                "_id": match,
                                "scrapped": False,
                                "views": views_matches[i],
                                "duration": duration_matches[i]
                            })         
                        except mongo_exception.DuplicateKeyError:
                            # skip document because it already exists in new collection
                            continue        
                print(video_collection.count_documents({"scrapped": False}))
    time.sleep(20*60*60)

