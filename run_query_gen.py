'''
Created on May 25, 2016

@author: pedrom
'''
import requests

from query.generation import query_gen
from query.stats import collect_stats
from query.url_scraper import scrape_urls


#query_gen("in_docs/physics", "generated_queries", 10)
scrape_urls("test_queries", "docs_urls", ['google', 'bing', 'yahoo', 'baidu', 'duckduckgo'])
#collect_stats("docs_urls")

