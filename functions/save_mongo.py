import pymongo
import os
import boto3
import json

mongo_host = os.environ['MONGO_HOST']
mongo_db = 'youtubeVideos'
mongo_uri = f'mongodb://{mongo_host}:27017/?authSource=admin'
SUBTITLES_BUCKET_NAME='youtubecrawledsubtitles'
CAPTION_QUEUE = "https://sqs.us-east-1.amazonaws.com/021338898563/youtube_subtitle_data"


def handler(event, context):
    mongo_client = pymongo.MongoClient(mongo_uri) 
    sqs_client = boto3.client("sqs")
    db = mongo_client[mongo_db]
    
    for item in event['Records']:
        item = json.loads(item['body'])
        print(item)
        video_id = item['video_id']
        parent_video_id = item['parent_video_id']
        db_result = db[video_id].insert_one({
            "video_id": video_id,
            "parent_video_id": parent_video_id,
            "subtitles":f"https://{SUBTITLES_BUCKET_NAME}.s3.amazonaws.com/{video_id}"
        })
        print(db_result)
        result = sqs_client.send_message(
            QueueUrl=CAPTION_QUEUE,
            MessageBody=item
        )
        print(result)
    return 'success'