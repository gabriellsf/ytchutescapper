import requests
from app import file_manager
import re
from datetime import date
import time

while True:
    initial_response = requests.get('https://www.bitchute.com/')

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

    pattern = re.compile('/channel/(.+?)/')

    offset = 0
    request_headers_list['referer'] = 'https://www.bitchute.com/channels/'
    while True:
        print(offset)
        request_extend_list_payload["offset"] = offset
        request_extend_channel = requests.post('https://www.bitchute.com/channels/extend/', request_extend_list_payload, headers=request_headers_list, cookies=request_cookies)
        file_manager.write_data(request_extend_channel.text,"video/none/list/" + date.today().strftime("%Y%m%d") + "/list_channel", "extend_"+ str(offset) + ".txt")
            
        all_matches = re.findall(pattern, request_extend_channel.text) 
        
        if offset > 20000 or len(all_matches) == 0:
            break
        else:
            offset += 40

    time.sleep(24*60*60)

