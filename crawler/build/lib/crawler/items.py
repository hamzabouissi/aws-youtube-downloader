# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy





class Subtitle(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    language = scrapy.Field()
    video_id = scrapy.Field()
    parent_video_id = scrapy.Field()
