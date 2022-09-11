import json
from time import sleep
import scrapy
from scrapy.http import JsonRequest,Request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api._errors import NoTranscriptFound
from crawler.items import Subtitle

class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    allowed_domains = ['www.youtube.com']
    start_urls = ['https://www.youtube.com/youtubei/v1/next']
    desirable_languages = ['en','ar', 'fr','de','es','it','rs','pt-PT','ko','ja']
    


    def get_payload(self, videoId):
        return  {
            "context": {
                "client": {
                    "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36,gzip(gfe)",
                    "clientName": "WEB",
                    "clientVersion": "2.20220829.00.00",
                    "platform": "DESKTOP"
                }
            },
            "videoId": videoId,
            "captionsRequested": True
        }


    def start_requests(self):
        video_id = "rE_SxmltgmA"
        for url in self.start_urls:
            yield JsonRequest(url=url, data=self.get_payload(video_id))

    def parse(self, response):
        data = response.json()
        suggestions = data['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results']
        current_video_id = data['currentVideoEndpoint']['watchEndpoint']['videoId']
        for suggest in suggestions:
            if compact_video := suggest.get("compactVideoRenderer",None):
                if (videoId:=compact_video.get('videoId')) is not None:
                    print(videoId)
                    # yield from self._get_subtitles(videoId,current_video_id)
                    # yield  JsonRequest(url=self.start_urls[0],callback=self.parse, data=self.get_payload(videoId))

            elif not (suggest.get("continuationItemRenderer") is None):
                command_token = suggest['continuationItemRenderer']['continuationEndpoint']['continuationCommand']
                payload = self.get_payload(current_video_id)
                payload['continuation'] = command_token['token']
                yield  JsonRequest(url=self.start_urls[0],callback=self._get_next_suggest_videos, data=payload,dont_filter=True) 

    def _get_next_suggest_videos(self, response):
        print("started")
        request = json.loads(response.request.body.decode("utf-8"))
        current_video_id = request['videoId']
        data = response.json()
        videos = data['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems']
        
        for video in videos:
            if compact_video := video.get("compactVideoRenderer",None):
                if not (compact_video.get('videoId') is None):
                    pass
                    # yield from self._get_subtitles(compact_video.get('videoId'),current_video_id)
            
            elif not (video.get("continuationItemRenderer") is None):
                command_token = video['continuationItemRenderer']['continuationEndpoint']['continuationCommand']
                payload = self.get_payload(current_video_id)
                payload['continuation'] = command_token['token']
                print(command_token['token'])
                yield JsonRequest(url=self.start_urls[0],callback=self._get_next_suggest_videos, data=payload,dont_filter=True) 



    def _get_subtitles(self,videoId,parent_video_id):
        try:
            subtitles = YouTubeTranscriptApi.list_transcripts(videoId)
            for lang in self.desirable_languages:
                try:
                    transcript = subtitles.find_manually_created_transcript([lang])
                    item = Subtitle(
                        language=lang,
                        text=transcript.fetch(),
                        video_id=videoId,
                        parent_video_id=parent_video_id
                    )
                    yield item
                except NoTranscriptFound:
                    continue
                
        except Exception as e:
            print(e)