import requests
import re
from datetime  import datetime
from app import file_manager

## INICIO DB Externalizar em outro arquivo
from pymongo import MongoClient
from pymongo import errors as mongo_exception
import os
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin')
db=client[os.environ['MONGODB_DATABASE']]

#FIM DB

initial_response = requests.get('https://www.bitchute.com/channels/')

request_cookies = initial_response.cookies.get_dict()
request_cookies["registration"] = "on"
request_cookies["preferences"] = "{%22theme%22:%22day%22%2C%22autoplay%22:true}"
request_cookies["__cf_bm"] = "4dc3db51f6f7241eeece9ef48763056de9c3b26f-1623714637-1800-AfEmTDVhDhomG/N51oD6UIiVmQSNSOtswFP+W8fGi9IKLAtusj/2V1OS2vil0eiCeapWwEjM3QkdehZIXPoMqyKTs+YmslGja0QoYuIxPuuuTutcYzx+GNKWqEzHMZauxA=="

request_headers_id = {
    'origin': 'https://www.bitchute.com',
    'authority': 'www.bitchute.com',
    'method': 'GET',
    'scheme': 'https',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'sec-ch-ua': 'Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90',
    'sec-ch-ua-mobile': "?0",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "none",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1"
}

pattern = re.compile('')
pattern_category = re.compile('')
pattern_views = re.compile('<span class="video-views"><i class="far fa-eye"><\/i>(.+?)<\/span>')
pattern_duration = re.compile('<span class="video-duration">(.+?)<\/span>')

channel_collection = db['channel']
video_collection = db['video']
count = 0

while True:
    channel = channel_collection.find_one({"scrapped": False})
    request_headers_id['referer'] = 'https://www.bitchute.com/channel/' + channel["_id"] + '/'
    request_headers_id['path'] = '/channel/' + channel["_id"] + '/'

    channel_request = requests.get('https://www.bitchute.com/channel/' + channel["_id"] + '/', headers=request_headers_id, cookies=request_cookies)

    if channel_request.status_code != 200:
        channel.update_one({"_id": channel["_id"]},{ '$set': {
            "scrapped": True,
            "failed": True
        }})
        continue

    text = channel_request.text
    category = re.search(pattern_category,text)
    file_manager.write_data(text,"channel/" + category[1] + "/page", channel["_id"] + ".txt")

    video_matches = re.findall(pattern, text)
    views_matches = re.findall(pattern_views, text)
    duration_matches = re.findall(pattern_duration, text)

    for i, match in enumerate(video_matches):
        try:
            video_collection.insert_one({"_id": match}, {
                "_id": match,
                "scrapped": False,
                "views": views_matches[i],
                "duration": duration_matches[i]
            })         
        except mongo_exception.DuplicateKeyError:
            # skip document because it already exists in new collection
            continue 

    channel_collection.update_one({"_id": channel["_id"]},{ '$set': {
        "scrapped": True,
        "category": category[1],
        "lastModified_scrapped": datetime.now()
    },
        '$currentDate': { 'lastModified': True }
    })

    print(count)
    count += 1


