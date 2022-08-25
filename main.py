# importing the module
import json
from time import sleep
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import pprint

pp = pprint.PrettyPrinter(indent=2)
channels = [
    "https://www.youtube.com/c/Vox/videos",
    "https://www.youtube.com/c/TED/videos",
    "https://www.youtube.com/c/bigthink/videos",
    "https://www.youtube.com/c/inanutshell/videos",
    "https://www.youtube.com/teded/videos"
]


def get_channel_id(channel_url:str)->list[str]:
    res = requests.get(channel_url)
    html = res.text
    extract_videos_code(html)
    # soup = BeautifulSoup(html, 'lxml')
    # element = soup.find("link",{"rel":"canonical"})
    # return element.attrs['href']

 

def download_captions(code):
    try:
        srt = YouTubeTranscriptApi.get_transcript(code)
        with open(f"subtitles/{code}.txt", "w") as f:
            for i in srt:
                f.write("{}\n".format(i))
    except Exception:
        return
    


def extract_videos_code(html):
    f = html.index('{"responseContext')
    e = html[f:].index(";</script>")
    data = html[f:f+e]
    json_data = json.loads(data)
    for item in json_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']\
        ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']:
        gridVideo = item.get("gridVideoRenderer",None)
        if not(gridVideo is None):
            print(gridVideo['videoId'])
            download_captions(gridVideo['videoId'])
    command = item.get('continuationItemRenderer', None)
    token = command['continuationEndpoint']['continuationCommand']['token']
    if token is None:
        return
    scrape(token)
            


def scrape(token):
    print("scraping tokens began")
    sleep(3)
    payload = {
        "context": {
            "client": {
                "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36,gzip(gfe)",
                "clientName": "WEB",
                "clientVersion": "2.20220823.05.00"
            }
        },
        "continuation": token
    }
    headers={

    }
    res = requests.post("https://www.youtube.com/youtubei/v1/browse",json=payload)
    videos = res.json()
    for item in videos['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems']:
        gridVideo = item.get("gridVideoRenderer",None)
        if not(gridVideo is None):
            print(gridVideo['videoId'])
            download_captions(gridVideo['videoId'])
    command = item.get('continuationItemRenderer', None)
    token = command['continuationEndpoint']['continuationCommand']['token']
    if token is None:
        return
    scrape(token)

for channel in channels:
    channel_id = get_channel_id(channel)
