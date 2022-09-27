import scrapy
from scrapy.http import JsonRequest
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
        yield JsonRequest(url=self.start_urls[0], data=self.get_payload(self.video_id))

    def parse(self, response):
        data = response.json()
        suggestions = data['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results']
        parent_video_id = data['currentVideoEndpoint']['watchEndpoint']['videoId']
        videos=[]
        for suggest in suggestions:
            if compact_video := suggest.get("compactVideoRenderer",None):
                if (videoId:=compact_video.get('videoId')) is not None:
                    videos.append(videoId)
                    yield Subtitle(
                        video_id=videoId,
                        parent_video_id=parent_video_id
                    )
        
        yield from self.parse_videos(videos)
            # elif not (suggest.get("continuationItemRenderer") is None):
            #     command_token = suggest['continuationItemRenderer']['continuationEndpoint']['continuationCommand']
            #     payload = self.get_payload(parent_video_id)
            #     payload['continuation'] = command_token['token']
                # yield JsonRequest(url=self.start_urls[0],callback=self._get_next_suggest_videos, data=payload,dont_filter=True)

    def parse_videos(self, videos):
        for video_id in videos:
            yield JsonRequest(url=self.start_urls[0],callback=self.parse, data=self.get_payload(video_id))

    # def _get_next_suggest_videos(self, response):
    #     request = json.loads(response.request.body.decode("utf-8"))
    #     parent_video_id = request['videoId']
    #     data = response.json()
    #     videos = data['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems']
        
    #     for video in videos:
    #         if compact_video := video.get("compactVideoRenderer",None):
    #             if (videoId:=compact_video.get('videoId')) is not None:
    #                 yield from self._get_subtitles(videoId,parent_video_id)
            
    #         elif not (video.get("continuationItemRenderer") is None):
    #             command_token = video['continuationItemRenderer']['continuationEndpoint']['continuationCommand']
    #             payload = self.get_payload(parent_video_id)
    #             payload['continuation'] = command_token['token']
    #             # yield JsonRequest(url=self.start_urls[0],callback=self._get_next_suggest_videos, data=payload,dont_filter=True) 


