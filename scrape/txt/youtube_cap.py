'''
Created on Jun 1, 2016

@author: pedrom
'''
import subprocess
from os import listdir, remove
from os.path import isfile, join


def get_captions(youtube_url):
    print("Getting captions for " + youtube_url)
    ret_dic = {}
    argsCapASR = "--write-auto-sub --sub-lang en --skip-download -o cap_asr.txt"
    cap_asr_str = run_youtube_dl(argsCapASR, "cap_asr", youtube_url)
    if not cap_asr_str == None:
        ret_dic["cap_asr"] = cap_asr_str
    
    argsManASR = "--write-sub --sub-lang en --skip-download -o cap_manual.txt"
    cap_manual_str = run_youtube_dl(argsManASR, "cap_manual", youtube_url)
    if not cap_manual_str == None:
        ret_dic["cap_man"] = cap_manual_str
    return ret_dic

def run_youtube_dl(args, outF, youtube_url):
    command = "C:\Python34\Scripts\youtube-dl " + args + " " + youtube_url
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = ""
    for line in p.stdout.readlines():
        result += str(line)
    retval = p.wait()
    all_files = [f for f in listdir(".") if isfile(join(".", f))]
    cap_str = None
    for file in all_files:
        if file.startswith(outF):
            with open(file, encoding="utf8") as cap_asr_file:
                cap_str = cap_asr_file.read()
            remove(file)
            return cap_str
    return None
