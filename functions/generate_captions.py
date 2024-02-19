import boto3
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound,TranscriptsDisabled
from sys import getsizeof

SUBTITLES_BUCKET_NAME='youtubecrawledsubtitles'
CAPTION_QUEUE = "https://sqs.us-east-1.amazonaws.com/021338898563/youtube_subtitle_data"
desirable_languages = ['en','ar', 'fr','de','es','it','rs','pt-PT','ko','ja']

def handler(event, context):
    sqs_client = boto3.client("sqs")
    
    for item in event['Records']:
        item = json.loads(item['body'])
        
        video_id = item['video_id']
        parent_video_id = item['parent_video_id']
        print(video_id)
        try:
            subtitles = YouTubeTranscriptApi.list_transcripts(video_id)
        except TranscriptsDisabled:
            return {"statusCode": 200, "body": {"message": f"video {video_id} has no captions"}}

        for lang in desirable_languages:
            try:
                transcript = subtitles.find_manually_created_transcript([lang])
                data = {
                    "language":lang,
                    "text":transcript.fetch(),
                    "video_id":video_id,
                    "parent_video_id":parent_video_id,
                    "provider":"youtube"
                }

                data_size = getsizeof(data)
                if data_size >= 262144:
                    return {"statusCode": 200, "body": {"message": f"video {video_id} has large captions, we're escaping it"}}
                

                data = json.dumps(data)
                result = sqs_client.send_message(
                    QueueUrl=CAPTION_QUEUE,
                    MessageBody=data
                )
            except NoTranscriptFound:
                continue
    return {"statusCode": 200, "body": {"video_id":video_id}}