'''
Created on Jun 8, 2016

@author: pedrom
'''
from tqdm import tqdm
import requests

def download_url_file(url, outFilePath):
    print("downloader %s" % url)
    response = requests.get(url, stream=True, timeout=5)
    
    with open(outFilePath, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    print("finish downloading")