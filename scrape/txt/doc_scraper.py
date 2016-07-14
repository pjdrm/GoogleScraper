'''
Created on Jun 2, 2016

@author: pedrom
'''
from _socket import timeout
import functools
import multiprocessing.pool
from os import listdir, makedirs, linesep
from os import remove
from os.path import isfile, join, exists
import subprocess
import sys

from newspaper.article import Article
import requests

from query.stats import is_video, get_url_type
from scrape.txt.downloader import download_url_file
from scrape.txt.slide_share import get_slide_share_pp
from scrape.txt.youtube_cap import get_captions
from utils.my_utils import is_good_lin


no_txt_urls = []
cache = None

def url_crawler(urlsDir, docTopTxtDir):
    global cache
    cache = build_cache(docTopTxtDir)
    for doc in listdir(urlsDir):
        docDir = join(docTopTxtDir, doc.split(".")[0])
        if not exists(docDir):
            makedirs(docDir)
        with open(join(urlsDir, doc)) as urlsDocFile:
            urls = urlsDocFile.readlines()
        urlDispatcher(urls, doc, docDir)
    
    with open("no_txt_url.txt", "w+") as outF:
        for no_txt_url in no_txt_urls:
            outF.write(no_txt_url)

def urlDispatcher(urls, doc, docTxtDir):
    for url in urls:
        global cache
        url = url[:-1]
        docName = docTxtDir.split("\\")[1]
        if docName in cache and url in cache[docName]["urls"]:
            continue
        urlType = get_url_type(url)
        '''
        if urlType == "video":
            print("New Video")
            youtube_handler(url, doc, docTxtDir)
        
        if urlType == "html":
            try:
                html_handler(url, doc, docTxtDir)
            except Exception as e:
                print(str(e))
                print("Time out while parsing HTML")
                print("writing dummy cache")
                buildFile(join(docTxtDir, str(nextFileIndex(docTxtDir))+".txt"), "", url, "html")
        if urlType == "pdf":
            tmp_pdf = "tmp.pdf"
            try:
                download_url_file(url, tmp_pdf)
            except Exception as e:
                print(str(e))
                try:
                    download_url_file(url, tmp_pdf)
                except Exception as e:
                    print(str(e))
                    print("Time out while downloading PDF")
                    print("writing dummy cache")
                    buildFile(join(docTxtDir, str(nextFileIndex(docTxtDir))+".txt"), "", url, "html")
                    continue
            try:
                get_txt_tika(url, tmp_pdf, doc, docTxtDir)
            except Exception as e:
                print(str(e))
                print("Time out while parsing PDF")
                print("writing dummy cache")
                buildFile(join(docTxtDir, str(nextFileIndex(docTxtDir))+".txt"), "", url, "html")
        if urlType == "ppt":
            print("New PPT")
            pp_handler(url, docTxtDir)
        '''
        if urlType == "word":
            print("New Word")
            word_handler(url, docTxtDir)
            
            
            
def youtube_handler(youtube_url, doc, docTxtDir):
    if youtube_url.startswith("https://www.youtube.com/") and not youtube_url.startswith("https://www.youtube.com/watch"):
        return
    dirIndex = str(nextDirIndex(docTxtDir))
    cap_txt_dic = get_captions(youtube_url)
    if len(cap_txt_dic.keys()) == 0:
        no_txt_urls.append(youtube_url)
        return
    makedirs(join(docTxtDir, dirIndex))
    for cap_type in cap_txt_dic:
        cap_txt = cap_txt_dic[cap_type]
        if not cap_txt == None:
            buildFile(join(docTxtDir, dirIndex, cap_type+".txt"), cap_txt, youtube_url, cap_type)
            
def pp_handler(ppt_url, docTxtDir):
    print("Power Point %s" % ppt_url)
    if ppt_url.startswith("http://www.slideshare"):
        print("writing dummy cache")
        buildFile(join(docTxtDir, str(nextFileIndex(docTxtDir))+".txt"), "", ppt_url, "slideshare")
        return
        #ppt_file_path = get_slide_share_pp(ppt_url)
    else:
        if ppt_url.endswith("pptx"):
            ppt_file_path = "tmp.pptx"
        elif ppt_url.endswith("ppt"):
            ppt_file_path = "tmp.ppt"
        try:
            download_url_file(ppt_url, ppt_file_path)
        except Exception as e:
            print("Power Point download time out")
            return
    if ppt_file_path == None:
        return
    
    if ppt_file_path.endswith("pptx") or ppt_file_path.endswith("ppt"):
        ppt_txt = get_txt_tika(ppt_file_path)
    else:
        return
    buildFile(join(docTxtDir, str(nextFileIndex(docTxtDir))+".txt"), ppt_txt, ppt_url, "ppt")
    remove(ppt_file_path)
    
def word_handler(word_url, docTxtDir):
    print("Word %s" % word_url)
    word_file_path = "tmp.doc"
    try:
        download_url_file(word_url, word_file_path)
    except Exception as e:
        print("Word download time out")
        return
    word_txt = get_txt_tika(word_file_path)
    buildFile(join(docTxtDir, str(nextFileIndex(docTxtDir))+".txt"), word_txt, word_url, "word")
    remove(word_file_path)
                
def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            res = async_result.get(max_timeout)
            async_result.wait()
            return res
        return func_wrapper
    return timeout_decorator 

def html_handler(html_url, doc, docTxtDir):
    print(html_url)
    article = Article(html_url, fetch_images=False, MAX_FILE_MEMO=1000)
    try:
        article.download()
    except Exception as e:
        print("article.download timeout")
        try:
            article.download()
        except Exception as e:
            print("writing dummy cache")
            buildFile(join(docTxtDir, str(nextFileIndex(docTxtDir))+".txt"), "", html_url, "html")
            return
    txt = ""
    if not article.html == "":
        try:
            article.parse()
            txt = article.text
        except Exception as e:
            print("article.parse timeout")
            print("writing dummy cache")
            buildFile(join(docTxtDir, str(nextFileIndex(docTxtDir))+".txt"), "", html_url, "html")
            return
    txt = "".join([s for s in txt.splitlines(True) if s.strip("\r\n")])
    buildFile(join(docTxtDir, str(nextFileIndex(docTxtDir))+".txt"), txt, html_url, "html")
    
def get_txt_tika(file_path):
    command = "java -jar C:\\Users\\pedrom\\workspace\\GoogleScraper\\tika-app-1.13.jar --encoding=utf8 -t " + file_path + " > temp_doc.txt"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = ""
    for line in p.stdout.readlines():
        result += str(line)
    retval = p.wait()
    final_txt = ""
    with open("temp_doc.txt", encoding="utf8") as ppFile:
        txt = ppFile.read()
        lins = [s for s in txt.splitlines(True) if s.strip("\r\n")]
        for lin in lins:
            lin = lin.strip()
            if is_good_lin(lin):
                final_txt += lin + "\n"
    return final_txt
                
def nextDirIndex(docTxtDir):
    onlyDirs = [int(f) for f in listdir(docTxtDir) if not isfile(join(docTxtDir, f))]
    if len(onlyDirs) == 0:
        return 0
    onlyDirs = sorted(onlyDirs)
    return onlyDirs[-1] + 1

def nextFileIndex(docTxtDir):
    print(docTxtDir)
    onlyFiles = [int(f[:-4]) for f in listdir(docTxtDir) if isfile(join(docTxtDir, f))]
    if len(onlyFiles) == 0:
        return 0
    onlyFiles = sorted(onlyFiles)
    return onlyFiles[-1] + 1

def buildFile(filePath, txt, url, desc):
    with open(filePath, "w+", encoding="utf8") as f:
        f.write(url + "\n")
        f.write("#" + desc + "\n")
        f.write(txt)
        
def build_cache(docTopTxtDir):
    cache = {}
    for docDir in listdir(docTopTxtDir):
        urls_to_cache = []
        for doc in listdir(join(docTopTxtDir, docDir)):
            if isfile(join(docTopTxtDir, docDir, doc)):
                with open(join(docTopTxtDir, docDir, doc), errors='ignore') as f:
                    urls_to_cache.append(f.readline()[:-1])
            else:
                for video_f in listdir(join(docTopTxtDir, docDir, doc)):
                    with open(join(docTopTxtDir, docDir, doc, video_f), errors='ignore') as f:
                        urls_to_cache.append(f.readline()[:-1])
        cache[docDir] = {"urls" : urls_to_cache}
    return cache         