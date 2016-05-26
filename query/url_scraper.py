'''
Created on May 25, 2016

@author: pedrom
'''
from os import listdir
from os.path import join
from GoogleScraper import scrape_with_config, GoogleSearchError
from urllib.request import urlopen

def scrape_urls(queryDir, outDir, search_engines):
    for fPath in listdir(queryDir):
        with open(join(queryDir, fPath)) as f:
            queries = f.readlines()
            queries_merged =  ' '.join(set(' '.join(queries).replace("\n", "").split(" ")))
            
        urls_file_name = fPath.split(".")[0] + ".urls.txt"
        urls_scraped = []
        with open(join(outDir, urls_file_name), "w+") as outF:
            for search_engine in search_engines:
                if search_engine == "google":
                    num_pages_for_keyword = 2
                else:
                    num_pages_for_keyword = 10
                config = {
                    'use_own_ip': 'True',
                    'keywords': [queries_merged],
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
                
                for serp in search.serps:
                    for link in serp.links:
                        print(link)
                        if not link.link in urls_scraped:
                            outF.write(link.link+"\n")
                        urls_scraped.append(link.link)