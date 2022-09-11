# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import io
import json
import uuid
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
import pymongo
from crawler.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, SUBTITLES_BUCKET_NAME
from elasticsearch import Elasticsearch
from motor import motor_asyncio,motor_tornado
from scrapy.utils.defer import maybe_deferred_to_future




class SubtitlePipeline:

    def open_spider(self, spider):
        self.subtitles_to_export = {}


    def close_spider(self, spider):
        for exporter, json_file in self.subtitles_to_export.values():
            exporter.finish_exporting()
            json_file.close()

    def _export_item(self, item):
        adapter = ItemAdapter(item)
        file_name = f"{item['video_id']}-{item['language']}"
        json_file = open(f"test/{file_name}.json", "wb")
        exporter = JsonItemExporter(json_file)
        exporter.start_exporting()
        self.subtitles_to_export[file_name] = (exporter, json_file)
        return self.subtitles_to_export[file_name][0]

    def process_item(self, item, spider):
        print("processing item")
        exporter = self._export_item(item)
        exporter.export_item(item)
        return item

import boto3

class TempJsonFile:
    obj: bytes
    
    def __init__(self, obj) -> None:
        self.obj = obj
    
    def read(self,*args,**kwargs):
        return self.obj


class S3Pipeline:
    client: boto3


    def open_spider(self, spider):
        self.client = boto3.client("s3",aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY,)


    def close_spider(self, spider):
       self.client.close()

    def _export_item(self, item):
        data = json.dumps(dict(item))
        temp = TempJsonFile(str.encode(data))
        self.client.upload_fileobj(temp, SUBTITLES_BUCKET_NAME,f"{item['video_id']}/{item['language']}")

    def process_item(self, item, spider):
        self._export_item(item)
        return item


class MongoPipeline:

    # collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        # self.client = motor_tornado.MotorClient(self.mongo_uri)

        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        

        response = self.db[item['video_id']].insert_one({
            "video_id": item['video_id'],
            "parent_video_id": item['parent_video_id'],
            "subtitles":f"https://{SUBTITLES_BUCKET_NAME}.s3.amazonaws.com/{item['video_id']}"
        })
        return item


class ElasticSearchPipeline:
    
    def __init__(self, elastic_uri:str, elastic_http_cert:str, auth:list[str]):
        self.elastic_uri = elastic_uri
        self.elastic_http_cert = elastic_http_cert
        self.auth = auth

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            elastic_uri=crawler.settings.get('ELASTIC_URL'),
            elastic_http_cert=crawler.settings.get('ELASTIC_HTTP_CERT'),
            auth=crawler.settings.get("ELASTIC_BASIC_AUTH")
        )


    def open_spider(self, spider):
        self.client = es = Elasticsearch(
            [{"host":self.elastic_uri,'port':9200,'scheme':"https"}],
            # make sure we verify SSL certificates
            verify_certs=True,
            # provide a path to CA certs on disk
            ca_certs=self.elastic_http_cert,
            basic_auth=self.auth,
        )
        

    def close_spider(self, spider):
        self.client.close()

    
    def process_item(self, item, spider):
        video_id = f"{item['video_id']}_{item['language']}".lower()
        data = item['text']
        index = self.client.indices.exists(index=video_id)
        if not index:
            self.client.indices.create(index=video_id)    
        for doc in data:
            self.client.create(index=video_id,id=uuid.uuid4(),document=doc,refresh=True)
        return item