#channel_request = requests.get('https://www.bitchute.com/channel/warroomshow/', headers=request_headers, cookies=request_cookies)


#   request_extend_payload = { "csrfmiddlewaretoken": request_cookies["csrftoken"],
#        "offset": 40
#    }
#request_extend_channel = requests.post('https://www.bitchute.com/category/science/channels/extend/', request_extend_payload, headers=request_headers, cookies=request_cookies)
 
#print(str(video_request.status_code)) # Sucesso
#print(str(channel_request.status_code)) # Sucesso
#file_manager.write_data(channel_request.text,"channel","unique_channel.txt");
#file_manager.write_data(request_extend_channel.text,"channel","extend_channel.txt");