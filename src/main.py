import requests
import re
from app import file_manager

## INICIO DB Externalizar em outro arquivo
from pymongo import MongoClient
from pymongo import errors as mongo_exception
import os
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin')
db=client[os.environ['MONGODB_DATABASE']]

#FIM DB

initial_response = requests.get('https://www.bitchute.com/category/science/')

request_cookies = initial_response.cookies.get_dict()
request_cookies["registration"] = "on"
request_cookies["preferences"] = "{%22theme%22:%22day%22%2C%22autoplay%22:true}"
request_cookies["__cf_bm"] = "1e1e664beed0c4b9da63e4c9954218ba951e6a44-1621566780-1800-AXp0m8SRTnOnIInBLWNyLZXFMwwsgt2tM7p7jAUeqt25qostdPWI57pxaM9L10kKHl1xNzQwVgoKZbodOD0+vaAjZ2+wfk8v7audNgIE5BZcYz+EhG//Sdd625pHdo9U0w=="

request_headers_id = {
    'origin': 'https://www.bitchute.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'sec-ch-ua': 'Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90',
    'sec-ch-ua-mobile': "?0",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "none",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1"
}


pattern = re.compile('<p class="video-card-title"><a href="\/video\/(.+?)\/')
pattern_views = re.compile('<span class="video-views"><i class="far fa-eye"><\/i>(.+?)<\/span>')
pattern_duration = re.compile('<span class="video-duration">(.+?)<\/span>')
pattern_category = re.compile('<tr><td>Category<\/td><td><a href="\/category\/(.+?)\/')

video_collection = db['video']

while True:
    video = video_collection.find_one({"scrapped": False})
    request_headers_id['referer'] = 'https://www.bitchute.com/video/' + video["_id"] + '/'

    video_request = requests.get('https://www.bitchute.com/video/' + video["_id"] + '/', headers=request_headers_id, cookies=request_cookies)
    text = video_request.text
    category = re.search(pattern_category,text)
    file_manager.write_data(text,"video/" + category[1] + "/page", video["_id"] + ".txt")

    all_matches = re.findall(pattern, text)
    views_matches = re.findall(pattern_views, text)
    duration_matches = re.findall(pattern_duration, text)
    for i, match in enumerate(all_matches):
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

    video_collection.update_one({"_id": video["_id"]},{ '$set': {
        "scrapped": True,
        "category": category[1]
    },
        '$currentDate': { 'lastModified': True }
    })


