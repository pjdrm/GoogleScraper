'''
Created on May 25, 2016

@author: pedrom
'''
import operator
from os import listdir
from os.path import join
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
from audioop import reverse
import subprocess

def collect_stats(urlDir):
    docTypes = ["pdf", "ppt", "doc", "pptx"]
    for fPath in listdir(urlDir):
        with open(join(urlDir, fPath)) as f:
            urls = f.readlines()
        statsDic = {}
        video_urls = ""
        for i, url in enumerate(urls):
            print ("Processing " + str(i) + " url")
            if is_video(url):
                pageType = "video"
                video_urls += url + "\n"
                
            else:
                pageType = url.split(".")[-1].strip()
                if not pageType in docTypes:
                    pageType = "html"
                    
                if pageType == "doc":
                    pageType == "word"
                    
                if pageType == "pptx":
                    pageType == "ppt"
                
            statsDic[pageType] = statsDic.get(pageType, 0) + 1
            
        
        with open("video_url.txt", "w+") as videoF:
            videoF.write(video_urls)
        statsDic = sorted(statsDic.items(), key=operator.itemgetter(1), reverse = True)
        objects = [label for label, val in statsDic]
        y_pos = np.arange(len(objects))
        performance = [val for label, val in statsDic]
         
        plt.bar(y_pos, performance, 0.5, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('#')
        plt.xlabel('Document Type')
         
        plt.show()
        
def is_video(url):
    command = "C:\Python34\Scripts\you-get -i " + url
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = ""
    for line in p.stdout.readlines():
        result += str(line)
    retval = p.wait()
    if "video" in result or "streams" in result:
        return True
    return False
            
    
