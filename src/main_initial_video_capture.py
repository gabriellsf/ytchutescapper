import requests
from app import file_manager
import re

initial_response = requests.get('https://www.bitchute.com/category/science/')

request_cookies = initial_response.cookies.get_dict()
request_cookies["registration"] = "on"
request_cookies["preferences"] = "{%22theme%22:%22day%22%2C%22autoplay%22:true}"
# TODO Buscar semente
request_cookies["__cf_bm"] = "1e1e664beed0c4b9da63e4c9954218ba951e6a44-1621566780-1800-AXp0m8SRTnOnIInBLWNyLZXFMwwsgt2tM7p7jAUeqt25qostdPWI57pxaM9L10kKHl1xNzQwVgoKZbodOD0+vaAjZ2+wfk8v7audNgIE5BZcYz+EhG//Sdd625pHdo9U0w=="

request_headers_list = {
    'origin': 'https://www.bitchute.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

request_extend_list_payload = { "csrfmiddlewaretoken": request_cookies["csrftoken"]}

pattern = re.compile('<span class=\\\\\"video-card-id hidden\\\\\">(.+?)<\/span>')

type = ["all","popular"]        
category = ['science','animation','arts','vehicles','beauty','finance','cuisine','diy',
        'education','entertainment','gaming','health','music','family','animals','spirituality',
        'vlogging','travel','sport','news']

category_index = 0
type_index = 0
offset = 0
last = ""
while type_index < len(type):
    while category_index < len(category):
        request_headers_list['referer'] = 'https://www.bitchute.com/category/' + category[category_index] + '/'
        print(category[category_index] + '_' + type[type_index])
        while True:
            print(offset)
            request_extend_list_payload["offset"] = offset
            request_extend_list_payload["last"] = last
            request_extend_list_payload["name"] = type[type_index]
            request_extend_video = requests.post('https://www.bitchute.com/category/' + category[category_index] + '/extend/', request_extend_list_payload, headers=request_headers_list, cookies=request_cookies)
            file_manager.write_data(request_extend_video.text,"video/" + category[category_index] + "/list_" + type[type_index], "extend_"+ str(offset) + ".txt")
                
            all_matches = re.findall(pattern, request_extend_video.text) 
            
            if offset > 20000 or len(all_matches) == 0:
                category_index += 1
                last = ''
                offset = 0
                break
            else:
                last = all_matches[len(all_matches)-1]
                offset += 40
    type_index += 1

