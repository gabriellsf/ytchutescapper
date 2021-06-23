from app import file_manager
import csv
import os
from pymongo import MongoClient

client = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin')
db=client[os.environ['MONGODB_DATABASE']]

channel_collection = db['channel']
video_collection = db['video']

channel_list = channel_collection.find() 
output_channel = csv.writer(open('./data/channel.csv', 'wt')) 

output_channel.writerow([ "_id",
    "scrapped",
    "category",
    "name" ,
    "owner" ,
    "code" ,
    "age" ,
    "videos_total_about" ,
    "subscriber_count",
    "view_count",
    "youtube_main_channel" ,
    "youtube_channel_id",
    "youtube_channel_name",
    "youtube_video_id",
    "scrapped_datetime",
    "lastModified_static_data",
    "lastModified_live_data",
    "lastModified",
    "failed",
    "request_status_code"
])

for item in channel_list:
    output_channel.writerow([
    item["_id"] if "_id" in item else '',
    item["scrapped"] if "scrapped" in item else '',
    item["category"] if "category" in item else '',
    item["name"] if "name" in item else '',
    item["owner"] if "owner" in item else '',
    item["code"] if "code" in item else '',
    item["age"] if "age" in item else '',
    item["videos_total_about"] if "videos_total_about" in item else '',
    item["subscriber_count"] if "subscriber_count" in item else '',
    item["about_view_count"] if "about_view_count" in item else '',
    item["youtube_main_channel"] if "youtube_main_channel" in item else '',
    item["youtube_channel_id"] if "youtube_channel_id" in item else '',
    item["youtube_channel_name"] if "youtube_channel_name" in item else '',
    item["youtube_video_id"] if "youtube_video_id" in item else '',
    item["scrapped_datetime"] if "scrapped_datetime" in item else '',
    item["lastModified_static_data"] if "lastModified_static_data" in item else '',
    item["lastModified_live_data"] if "lastModified_live_data" in item else '',
    item["lastModified"] if "lastModified" in item else '',
    item["failed"] if "failed" in item else '',
    item["request_status_code"] if "request_status_code" in item else '',
    ])
    

video_list = video_collection.find() 
output_video = csv.writer(open('./data/video.csv', 'wt'))

output_video.writerow(["_id",
    "scrapped",
    "title",
    "views",
    "duration",
    "category",
    "channel",
    "youtube_channel_id",
    "youtube_channel_name",
    "youtube_video_id",
    "video_publish_date",
    "sensitivity",
    "view_count",
    "like_count",
    "dislike_count",
    "comment_count",
    "related_videos",
    "scrapped_datetime",
    "lastModified_static_data",
    "lastModified_live_data",
    "lastModified_live_data_comment",
    'lastModified',
    "video_blocked",
    "failed",
    "request_status_code"
])


for item in video_list:
    output_video.writerow([
        item["_id"] if "_id" in item else '',
        item["scrapped"] if "scrapped" in item else '',
        item["title"] if "title" in item else '',
        item["views"] if "views" in item else '',
        item["duration"] if "duration" in item else '',
        item["category"] if "category" in item else '',
        item["channel"] if "channel" in item else '',
        item["youtube_channel_id"] if "youtube_channel_id" in item else '',
        item["youtube_channel_name"] if "youtube_channel_name" in item else '',
        item["youtube_video_id"] if "youtube_video_id" in item else '',
        item["video_publish_date"] if "video_publish_date" in item else '',
        item["sensitivity"] if "sensitivity" in item else '',
        item["view_count"] if "view_count" in item else '',
        item["like_count"] if "like_count" in item else '',
        item["dislike_count"] if "dislike_count" in item else '',
        item["comment_count"] if "comment_count" in item else '',
        item["related_videos"] if "related_videos" in item else '',
        item["scrapped_datetime"] if "scrapped_datetime" in item else '',
        item["lastModified_static_data"] if "lastModified_static_data" in item else '',
        item["lastModified_live_data"] if "lastModified_live_data" in item else '',
        item["lastModified_live_data_comment"] if "lastModified_live_data_comment" in item else '',
        item["lastModified"] if "lastModified" in item else '',
        item["video_blocked"] if "video_blocked" in item else '',
        item["failed"] if "failed" in item else '',
        item["request_status_code"] if "request_status_code" in item else ''
    ])
