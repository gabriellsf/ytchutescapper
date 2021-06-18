from datetime import datetime
from datetime import timedelta
import time
import requests
import json
import os
from pymongo import MongoClient

client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin')
db=client[os.environ['MONGODB_DATABASE']]

channel_collection = db['channel']

initial_response = requests.get('https://www.bitchute.com/')

request_cookies = initial_response.cookies.get_dict()
request_cookies["registration"] = "on"
request_cookies["preferences"] = "{%22theme%22:%22day%22%2C%22autoplay%22:true}"
# TODO Buscar semente
request_cookies["__cf_bm"] = "1e1e664beed0c4b9da63e4c9954218ba951e6a44-1621566780-1800-AXp0m8SRTnOnIInBLWNyLZXFMwwsgt2tM7p7jAUeqt25qostdPWI57pxaM9L10kKHl1xNzQwVgoKZbodOD0+vaAjZ2+wfk8v7audNgIE5BZcYz+EhG//Sdd625pHdo9U0w=="

request_headers = {
    'origin': 'https://www.bitchute.com',
    'authority': 'www.bitchute.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

request_payload = { "csrfmiddlewaretoken": request_cookies["csrftoken"]}
request_comment_payload = {"cf_auth": "eyJwcm9maWxlX2lkIjogImFub255bW91cyIsICJvd25lcl9pZCI6ICI0ajJDdU5tbzFrU3kiLCAiZGlzcGxheV9uYW1lIjogImFub255bW91cyIsICJ0aHJlYWRfaWQiOiAiYmNfd3hkNVVPb05BTHFPIiwgImljb25fdXJsIjogIi9zdGF0aWMvdjEzMS9pbWFnZXMvYmxhbmstcHJvZmlsZS5wbmciLCAiY2ZfaXNfYWRtaW4iOiAiZmFsc2UifQ== 6883274cc76bc48380f010d5a0be71a9b5541329d4c0a4f9368025d7ec58c5db 1623934581"}

query = {"scrapped": True, 
         "lastModified_static_data":  { "$exists" : True },
         "failed":  { "$exists" : False }}

while True:
    count_view = 0
    count_comment = 0
    for channel in channel_collection.find(query):
        print(channel['_id'])
        if channel.get('lastModified_live_data', datetime.now() + timedelta(days=-10)) < datetime.now() + timedelta(days=-3) :
            request_headers['referer'] = 'https://www.bitchute.com/channel/' + channel['_id'] + '/'

            request_count_channel = requests.post('https://www.bitchute.com/channel/' + channel['code'] + '/counts/', request_payload, headers=request_headers, cookies=request_cookies)
                
            if request_count_channel.status_code == 200:
                count_response = json.loads(request_count_channel.text.strip())
                if count_response["success"]:
                    channel_collection.update_one({"_id": channel["_id"]},{ '$set': {
                        "subscriber_count": count_response["subscriber_count"], 
                        "about_view_count": count_response["about_view_count"].replace(' views',''), 
                        "lastModified_live_data": datetime.now()
                    }})
                    count_view += 1    
      
            print(count_view)
    time.sleep(5*60)



