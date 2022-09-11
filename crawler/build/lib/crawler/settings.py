# Scrapy settings for crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }
CLOSESPIDER_PAGECOUNT = 2
CLOSESPIDER_ERRORCOUNT = 1
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'crawler.pipelines.SubtitlePipeline': 300,
   # 'crawler.pipelines.S3Pipeline': 1,
   # 'crawler.pipelines.MongoPipeline': 2,
   # 'crawler.pipelines.ElasticSearchPipeline': 3,
   
   # 'scrapy.pipelines.files.FilesPipeline': 1

}

AWS_ACCESS_KEY_ID = 'AKIAQJ57FYCB5UT6G74A'
AWS_SECRET_ACCESS_KEY = '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'
SUBTITLES_BUCKET_NAME = 'youtubecrawledsubtitles'
# MONGO_URI = 'mongodb://admin:never_mind@ec2-54-82-177-165.compute-1.amazonaws.com:27017/?authSource=admin'
MONGO_URI = "mongodb://root:example@localhost:27017/?authSource=admin"
MONGO_DATABASE = "YoutubeVideos"

ELASTIC_URL = "35.171.163.235"
ELASTIC_HTTP_CERT = "/home/forswearbeetle/Projects/youtube-captions-downloader/http_cert.crt"
ELASTIC_BASIC_AUTH = ('elastic', 'wReKOgoKIc_hC6D=JElT')

# FEEDS = {
#     's3://youtubecrawledsubtitles/%(name)s/data.json': {
#         'format': 'json',
#         'encoding': 'utf8',
#         'store_empty': False,
#         'indent': 4,
#         "item_classes": ['crawler.items.Subtitle']
#     }
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'