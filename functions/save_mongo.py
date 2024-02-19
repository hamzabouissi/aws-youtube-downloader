import pymongo
import os
import json

mongo_host = os.environ['MONGO_HOST']
mongo_db = 'videos'
mongo_uri = f'mongodb://{mongo_host}:27017/?authSource=admin'


def handler(event, context):
    mongo_client = pymongo.MongoClient(mongo_uri) 
    db = mongo_client[mongo_db]
    
    for item in event['Records']:
        item = json.loads(item['body'])
        collection_id = f"{item['language']}".lower()
        data = item['text']
        db_result = db[collection_id].insert_many(gendata(item['video_id'],item['provider'],data))
       
    return {"statusCode": 200}



def gendata(video_id, provider, data):
    for doc in data:
        doc['video_id'] = video_id
        doc['provider'] = provider
        doc['end'] = doc['start'] + doc['duration']
        yield doc