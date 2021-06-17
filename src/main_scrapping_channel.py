import requests
import re
import time
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
request_cookies["__cf_bm"] = "1e1e664beed0c4b9da63e4c9954218ba951e6a44-1621566780-1800-AXp0m8SRTnOnIInBLWNyLZXFMwwsgt2tM7p7jAUeqt25qostdPWI57pxaM9L10kKHl1xNzQwVgoKZbodOD0+vaAjZ2+wfk8v7audNgIE5BZcYz+EhG//Sdd625pHdo9U0w=="

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

pattern_category = re.compile('<p>Category <span class=""><a href="/category/(.+?)/"')

channel_collection = db['channel']

while True:
    channel = channel_collection.find_one({"scrapped": False})
    if channel is None:
        time.sleep(5*60)
        continue
    
    request_headers_id['referer'] = 'https://www.bitchute.com/channel/' + channel["_id"] + '/'
    request_headers_id['path'] = '/channel/' + channel["_id"] + '/'

    channel_request = requests.get('https://www.bitchute.com/channel/' + channel["_id"] + '/', headers=request_headers_id, cookies=request_cookies)

    if channel_request.status_code != 200:
        channel_collection.update_one({"_id": channel["_id"]},{ '$set': {
            "scrapped": True,
            "failed": True,
            "request_status_code": channel_request.status_code
        }})
        continue

    text = channel_request.text
    category = re.search(pattern_category,text)
    if category is None:
        category = [None,"none"]
    file_manager.write_data(text,"video/" + category[1] + "/channel", channel["_id"] + ".txt")

    channel_collection.update_one({"_id": channel["_id"]},{ '$set': {
        "scrapped": True,
        "category": category[1]
    },
        '$currentDate': { 'lastModified': True }
    })

    print(channel_collection.count_documents({"scrapped": False}))



