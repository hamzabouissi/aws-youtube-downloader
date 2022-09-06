from codecs import ignore_errors
import json
from uuid import uuid4
from elasticsearch import Elasticsearch

es = Elasticsearch(
    [{"host":'35.171.163.235','port':9200,'scheme':"https"}],
    # make sure we verify SSL certificates
    verify_certs=True,
    # provide a path to CA certs on disk
    ca_certs='~/Projects/youtube-captions-downloader/http_cert.crt',
    basic_auth=('elastic', 'wReKOgoKIc_hC6D=JElT'),
)
video_id = '9XGm_uHit5g'.lower()
with open("en.json", "r") as f:
    data = json.loads(f.read()) 

index = es.indices.exists(index=video_id)
if not index:
    es.indices.create(index=video_id)    
es.create(index=video_id,id=uuid4(),document=data['text'][0],refresh=True)
es.create(index=video_id,id=uuid4(),document=data['text'][1],refresh=True)