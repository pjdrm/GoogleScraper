'''
Created on May 25, 2016

@author: pedrom
'''
from audioop import reverse
import operator, time
from os import listdir, kill
from os.path import join, isfile
import signal
from subprocess import TimeoutExpired
import subprocess, threading
import tempfile

import matplotlib.pyplot as plt
import numpy as np
import sys


import matplotlib.pyplot as plt; plt.rcdefaults()

isVideoCache = None
isVideoCacheDir = "isVideoCacheDir"

def caption_stats(doc_top_dir):
    caption_stats_dic = {}
    for doc_dir in listdir(doc_top_dir):
        for videoDir in listdir(join(doc_top_dir, doc_dir)):
            if not isfile(videoDir):
                for capFile in listdir(join(doc_top_dir, doc_dir, videoDir)):
                    caption_stats_dic[capFile.split(".")[0]] = caption_stats_dic.get(capFile.split(".")[0], 0) + 1
    print("ASR captions: %d\nManual captions: %d" % (caption_stats_dic["cap_asr"], caption_stats_dic["cap_man"]))
    
def collect_stats(urlDir):
    statsDic = {}
    video_urls = ""
    for fPath in listdir(urlDir):
        with open(join(urlDir, fPath)) as f:
            urls = f.readlines()
        for i, url in enumerate(urls):
            pageType = get_url_type(url)
            if pageType == "video":
                video_urls += url                
            statsDic[pageType] = statsDic.get(pageType, 0) + 1
            
        
    with open("video_url.txt", "w+") as videoF:
        videoF.write(video_urls)
    statsDic = sorted(statsDic.items(), key=operator.itemgetter(1), reverse = True)
    objects = [label for label, val in statsDic]
    y_pos = np.arange(len(objects))
    performance = [val for label, val in statsDic] 
     
    plt.bar(y_pos, performance, 0.5, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of Documents')
    plt.xlabel('Document Type')
     
    plt.show()
        
def is_video(url):
    global isVideoCache
    if isVideoCache == None:
        isVideoCache = loadIsVideoCache()
        
    if url in isVideoCache:
        return isVideoCache[url]
    
    print("Checking if %s is a video" % url)
    cmd = "C:\Python34\Scripts\you-get -i " + url
    returnVal = False
    f = tempfile.TemporaryFile() 
    process = subprocess.Popen(cmd, shell=True, stdout=f)
    time.sleep(10)
    process.terminate() 
    process.wait()
    f.seek(0)
    result = f.read().decode("utf-8", errors='ignore')   

    if "video" in result or "streams" in result:
        returnVal = True
    '''
    command = Command("C:\Python34\Scripts\you-get -i " + url)
    command.run(timeout=10)
    returnVal = command.returnVal
    '''
    cacheIsVideo(url, str(returnVal))
    return returnVal

def cacheIsVideo(url, returnVal):
    global isVideoCacheDir
    files = [int(f.split(".")[0]) for f in listdir(isVideoCacheDir)]
    if len(files) == 0:
        fName = "0.txt"
    else:
        files = sorted(files)    
        fName = str(files[-1] + 1) + ".txt"
    with open(join(isVideoCacheDir, fName), "w+") as f:
        f.write(url + returnVal)
        
def loadIsVideoCache():
    global isVideoCacheDir
    cache = {}
    for filePath in listdir(isVideoCacheDir):
        with open(join(isVideoCacheDir, filePath)) as f:
            lins = f.readlines()
            val = True
            #print(join(isVideoCacheDir, filePath))
            if lins[1] == "False":
                val = False
            cache[lins[0][:-1]] = val
    return cache

def get_url_type(url):
    docTypes = ["pdf", "ppt", "doc", "pptx", "video", "DOCX", "DOC", "PDF"]
    if url.startswith("http://www.slideshare.net"):
        pageType = "ppt"
    elif is_video(url):
        pageType = "video"
    else:
        pageType = url.split(".")[-1].strip()
        if not pageType in docTypes:
            pageType = "html"
            
        if pageType == "doc" or pageType == "DOC" or pageType == "docx" or pageType == "DOCX":
            pageType = "word"
            
        if pageType == "pptx":
            pageType = "ppt"
        if pageType == "PDF":
            pageType = "pdf"
    return pageType

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.returnVal = False

    def run(self, timeout):
        def target():
            print('you-get Thread started')
            f = tempfile.TemporaryFile() 
            self.process = subprocess.Popen(self.cmd, shell=True, stdout=f)
            time.sleep(timeout)
            self.process.terminate() 
            self.process.wait()
            f.seek(0)
            result = f.read().decode("utf-8")   

            if "video" in result or "streams" in result:
                self.returnVal = True
            print('you-get Thread finished')

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print('Terminating you-get process')
            kill(self.process.pid, signal.SIGTERM)
            thread.join()
            print('Killed you-get process')
            
    
