from scrapy.crawler import CrawlerProcess
from crawler.spiders.youtube import YoutubeSpider

def main(event, context):
    process = CrawlerProcess({
      'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
      'FEED_FORMAT': 'json',
    })
    process.crawl(YoutubeSpider,video_id='ZHhmi2bS0hU')
    process.start() 


if __name__ == "__main__":
   main('', '')