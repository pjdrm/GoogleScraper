'''
Created on May 25, 2016

@author: pedrom
'''
from os import listdir
from os.path import join
import re
from urllib.request import urlopen

import requests

from GoogleScraper import scrape_with_config, GoogleSearchError
from query.khanacademy import khanacademy_search
from query.youtube import youtube_search


def scrape_urls(queryDir, outDir, search_engines):
    for fPath in listdir(queryDir):
        with open(join(queryDir, fPath)) as f:
            queries = f.readlines()
            queries_merged =  ' '.join(set(' '.join(queries).replace("\n", "").split(" ")))
            
        urls_file_name = fPath.split(".")[0] + ".urls.txt"
        urls_scraped = []
        with open(join(outDir, urls_file_name), "w+") as outF:
            for search_engine in search_engines:
                if search_engine == "youtube":
                    urls = youtube_search(queries_merged)
                    for url in urls:
                        if not url in urls_scraped:
                            outF.write(url+"\n")
                            print("Youtube URL: " + url)
                        urls_scraped.append(url)
                        
                elif search_engine == "khanacademy":
                    urls = khanacademy_search(queries_merged)
                    for url in urls:
                        if not url in urls_scraped:
                            outF.write(url+"\n")
                            print("Khanacademy URL: " + url)
                        urls_scraped.append(url)
                        
                else:
                    search = google_scrapper(search_engine, queries_merged)
                
                    for serp in search.serps:
                        for link in serp.links:
                            print(link)
                            str_link = str(link.link)
                            '''
                            if search_engine == "baidu":
                                str_link = getRedirectURL(str_link)
                            if search_engine == "yahoo" and str_link.startswith("http://r.search.yahoo.com"):
                                str_link = getRedirectURL(str_link)
                            '''    
                            if str_link == None:
                                continue
                            
                            if not str_link in urls_scraped:
                                outF.write(str_link+"\n")
                            urls_scraped.append(str_link)
        
        urls_final = ""
        with open(join(outDir, urls_file_name), "r") as urlsFile:
            lines = urlsFile.readlines()
            for lin in lines:
                if lin.startswith("http://r.search.yahoo.com") or lin.startswith("http://www.baidu.com"):
                    lin = getRedirectURL(lin[:-1])
                    if lin == None:
                        continue
                urls_final += lin
        
        with open(join(outDir, urls_file_name), "w") as urlsFinalFile:
            urlsFinalFile.write(urls_final)

def google_scrapper(search_engine, query):
    if search_engine == "google":
        num_pages_for_keyword = 2
    else:
        num_pages_for_keyword = 10
    config = {
        'use_own_ip': 'True',
        'keywords': [query],
        'search_engines': search_engine,
        'num_results_per_page': 100,
        'num_pages_for_keyword': num_pages_for_keyword,
        'search_offset': 1,
        'scrape_method': 'http',
        'do_caching': 'False'
    }
    
    try:
        search = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)
    return search
                                            
def getRedirectURL(url):
    try:
        response = requests.get(url)
        match = re.search("URL=\\\\\\'[^\\\\]+\\\\\\'", str(response._content))
        url = match.group(0).replace("URL=\\'", "")[:-2]
        if not url[-1] == "\n":
            url += "\n"
        return url
    except Exception:
        return None
    