'''
Created on May 31, 2016

@author: pedrom
'''
import urllib
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver


def khanacademy_search(query):
    urls = []
    print("Khanacademy query: " + query)
    browser = webdriver.Firefox()
    query = urllib.request.quote(query)
    url = "https://www.khanacademy.org/search?search_again=1&page_search_query=" + query
    browser.get(url)
    html = browser.page_source
    browser.close()
    soup = BeautifulSoup(html, "lxml")
    for vid in soup.findAll(attrs={'class':'gs-title', 'class':'gs-title'}):
        if vid.has_attr('href'):
            urls.append(vid['href'])
    return urls
