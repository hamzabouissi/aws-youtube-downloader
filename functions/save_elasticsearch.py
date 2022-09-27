import uuid
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os
import boto3

ELASTIC_URI = os.environ['ELASTIC_URI']
ELASTIC_BASIC_AUTH = ('elastic', 'eoxQaciW-ulf2iTDTex')

client = boto3.client("s3")
with open('http_cert', 'wb') as f:
    client.download_fileobj('youtubecrawlerfunction', 'http_ca.crt', f)

elastic_client = Elasticsearch(
    [{"host":ELASTIC_URI,'port':9200,'scheme':"https"}],
    # make sure we verify SSL certificates
    verify_certs=True,
    # provide a path to CA certs on disk
    ca_certs='http_cert',
    basic_auth=ELASTIC_BASIC_AUTH,
)


def handler(event, context):
    for item in event['Records']:
        index_id = f"video_{item['language']}".lower()
        data = item['text']
        index = elastic_client.indices.exists(index=index_id)
        if not index:
            elastic_client.indices.create(index=index_id)    
        bulk(elastic_client, gendata(index_id, item['video_id'], data))
    return item
    

def gendata(index_id, videoId, data):
    for doc in data:
        doc['videoId'] = videoId
        yield {
            "_index":index_id,
            "_id":uuid.uuid4(),
            "doc":doc,
            "refresh":True
        }