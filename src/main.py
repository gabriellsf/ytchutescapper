import requests
from app import file_manager
import re
import time
import random

## INICIO DB Externalizar em outro arquivo
from pymongo import MongoClient
import os
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'])
#db=client.db(os.environ['MONGODB_DATABASE'])
#FIM DB

initial_response = requests.get('https://www.bitchute.com/category/science/')

request_cookies = initial_response.cookies.get_dict()
request_cookies["registration"] = "on"
request_cookies["preferences"] = "{%22theme%22:%22day%22%2C%22autoplay%22:true}"
# TODO Buscar semente
request_cookies["__cf_bm"] = "1e1e664beed0c4b9da63e4c9954218ba951e6a44-1621566780-1800-AXp0m8SRTnOnIInBLWNyLZXFMwwsgt2tM7p7jAUeqt25qostdPWI57pxaM9L10kKHl1xNzQwVgoKZbodOD0+vaAjZ2+wfk8v7audNgIE5BZcYz+EhG//Sdd625pHdo9U0w=="

request_headers_id = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'sec-ch-ua': 'Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90',
    'sec-ch-ua-mobile': "?0",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "none",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1"
}

request_headers_list = {
    'origin': 'https://www.bitchute.com',
    'referer': 'https://www.bitchute.com/category/science/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

request_extend_list_payload = { "csrfmiddlewaretoken": request_cookies["csrftoken"],
    "name": "popular"
}

pattern = re.compile('<span class=\\\\\"video-card-id hidden\\\\\">(.+?)<\/span>')
category = ['news','science']
category_index = 0
offset = 0
last = ""
while category_index < len(category):
    request_headers_list['referer'] = 'https://www.bitchute.com/category/' + category[category_index] + '/'
    while True:
        request_extend_list_payload["offset"] = offset
        request_extend_list_payload["last"] = last
        request_extend_video = requests.post('https://www.bitchute.com/category/' + category[category_index] + '/extend/', request_extend_list_payload, headers=request_headers_list, cookies=request_cookies)
        file_manager.write_data(request_extend_video.text,"video/" + category[category_index] + "/list", "extend_"+ str(offset) + ".txt")

        all_matches = re.findall(pattern, request_extend_video.text)
        for match in all_matches:
            video_request = requests.get('https://www.bitchute.com/video/' + match + '/', headers=request_headers_id, cookies=request_cookies)
            file_manager.write_data(video_request.text,"video/" + category[category_index] + "/page", match + ".txt")
            last = match
            time.sleep(random.random())

        offset += 20

        if offset > 300:
            category_index += 1
            last = ''
            offset = 0
            break


