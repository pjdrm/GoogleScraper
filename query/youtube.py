'''
Created on May 31, 2016

@author: pedrom
'''
import urllib
import urllib.request

from bs4 import BeautifulSoup
from oauth2client.tools import argparser  # pip install oauth2client

from apiclient.discovery import build  # pip install google-api-python-client
from apiclient.errors import HttpError  # pip install google-api-python-client


DEVELOPER_KEY = "AIzaSyBWxX3bvedI7M3JT5R-RePSWgPidkwNfpk" 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query):
    urls = []
    print("Youtube query: " + query)
    query = urllib.request.quote(query)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        urls.append('https://www.youtube.com' + vid['href'])
    return urls
        
def youtubeapi_search(query):

    print("Youtube query: " + query)
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    search_response = youtube.search().list(
     q=query,
     type="video",
     part="id,snippet",
     maxResults=25
    ).execute()
    
    # Add each result to the appropriate list, and then display the lists of
    # matching videos.
    # Filter out channels, and playlists.
    urslList = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            #videos.append("%s" % (search_result["id"]["videoId"]))
            urslList.append("https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
    return urslList
    
def download_caption(caption_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    subtitle = youtube.captions().download(
                                           id=caption_id
                                           ).execute()

    print("First line of caption track: %s" % (subtitle))
  
#youtube_search("time negative second first t1 velocity average acceleration zero")
#youtube_search("Game of Thrones")
#download_caption("rkDWSSzM8ox9kdHZoyfzHxobn_dcjtlYpeNE6JuaFJI=")
