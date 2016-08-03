'''
Created on May 25, 2016

@author: pedrom
'''
import re

import requests

from post.processing.html_processing import process_html
from post.processing.ppt_processing import process_ppt
from post.processing.srt_processing import process_srt
from post.processing.process_pdf import process_pdf
from query.generation import query_gen
from query.stats import collect_stats, caption_stats, is_video
from query.url_scraper import scrape_urls
from scrape.txt.doc_scraper import url_crawler




#query_gen("in_docs/physics", "generated_queries", 10)
#scrape_urls("test_queries", "docs_urls", ['yahoo', 'baidu', 'youtube', 'khanacademy', 'google', 'bing', 'duckduckgo'])
#scrape_urls("test_queries", "docs_urls", ['yahoo'])
#collect_stats("docs_urls")
#url_crawler("docs_urls", "docs_txt")
#process_srt("docs_txt/")
#process_ppt("docs_txt/")
#process_html("docs_txt/")
process_pdf("docs_txt/")
#caption_stats("docs_txt")