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
        'vlogging','travel','sport','none']


id_pattern = re.compile('<p class="name"><a href="/channel/(.+?)/"')
name_pattern = re.compile('<h1 id="channel-title" class="page-title hidden">(.+?)</h1>')
owner_pattern = re.compile('<p class="owner"><a href="/profile/(.+?)/"')
code_pattern = re.compile('<link id="canonical" rel="canonical" href="https://www.bitchute.com/channel/(.+?)/" />')
age_pattern = re.compile('<p>Created (.+?) ago.</p>')
videos_pattern = re.compile('<p><span><i class="fas fa-video fa-fw"></i> <span>(.+?) video')

main_youtube_channel_pattern = re.compile('<a href="https://www\.youtube\.com/user/(.+?)" target="_blank" rel="noopener noreferrer" data-toggle="tooltip" data-placement="bottom" title="YouTube">') 
main_youtube_channel_pattern_2 = re.compile('<a href="https://www\.youtube\.com/channel/(.+?)" target="_blank" rel="noopener noreferrer" data-toggle="tooltip" data-placement="bottom" title="YouTube">') 
youtube_channel_id_pattern = re.compile('https://www\.youtube\.com/channel/(.+?)[\"|/|<|?:\s+|$]')
youtube_channel_user_pattern = re.compile('https://www\.youtube\.com/user/(.+?)[\"|/|<|?:\s+|$]')
youtube_channel_user_pattern_2 = re.compile('https://www\.youtube\.com/c/(.+?)[\"|/|<|?:\s+|$]')
youtube_video_id_pattern = re.compile('https://www\.youtube\.com/watch\?v=(.+?)[\"|/|<|?:\s+|$]')

channel_collection = db['channel']

for c in category:
    dir = "./data/video/" + c + "/channel/"
    print(dir)
    files =  os.listdir(dir)
    for file in files:
        print(file)
        with open(dir + file, "r") as data:
            text = data.read()

            id_match = re.findall(id_pattern,text)
            name_match = re.findall(name_pattern,text)
            owner_match = re.findall(owner_pattern,text)
            code_match = re.findall(code_pattern,text)
            age_match = re.findall(age_pattern,text) 
            videos_match = re.findall(videos_pattern,text) 

            if id_match[0] != os.path.splitext(file)[0]:
                channel_collection.delete_one( {"_id": os.path.splitext(file)[0]});  
                os.remove(dir + file)
                try:
                    channel_collection.insert_one({
                        "_id": id_match[0],
                        "scrapped": False
                    })         
                except mongo_exception.DuplicateKeyError:
                    # skip document because it already exists in new collection
                    pass
                continue

            main_youtube_channel_matches = re.findall(main_youtube_channel_pattern,text)
            main_youtube_channel_matches.extend(re.findall(main_youtube_channel_pattern_2,text))
            youtube_channel_id_matches = re.findall(youtube_channel_id_pattern,text) 
            youtube_channel_user_matches = re.findall(youtube_channel_user_pattern,text) 
            youtube_channel_user_matches.extend(re.findall(youtube_channel_user_pattern_2,text))
            youtube_video_id_matches = re.findall(youtube_video_id_pattern,text) 

            channel_collection.update_one({"_id": os.path.splitext(file)[0]},{ '$set': {
                "name" : name_match[0],
                "owner" : owner_match[0],
                "code" : code_match[0],
                "age" :  age_match[0],
                "videos_total_about" : videos_match[0],
                "youtube_main_channel" : main_youtube_channel_matches[0] if len(main_youtube_channel_matches) > 0 else '',
                "youtube_channel_id": list(set(youtube_channel_id_matches)),
                "youtube_channel_name": list(set(youtube_channel_user_matches)),
                "youtube_video_id": list(set(youtube_video_id_matches)),
                "lastModified_static_data": datetime.now()
            }})
                