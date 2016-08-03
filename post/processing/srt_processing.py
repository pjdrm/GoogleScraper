'''
Created on Jul 14, 2016

@author: pedrom
'''
import os

def srt2txt(in_file_path, out_file_path):
    with open(in_file_path, encoding="utf8", errors='ignore') as in_file:
        lins = in_file.readlines()[6:]
        sent = ""
        txt = ""
        for lin in lins:
            if "\n" == lin or "-->" in lin:
                continue
            lin = lin.strip()
            sent += lin + " "
            
            if lin.endswith(".") or lin.endswith("?") or lin.endswith("!"):
                txt += sent[:-1] + "\n"
                sent = ""
    
    with open(out_file_path, "w+", encoding="utf8") as out_file:
        out_file.write(txt[:-1])
        
def isSRT(video_file):
    with open(video_file, encoding="utf8", errors='ignore') as f:
        lins = f.readlines()
    if len(lins) <  6:
        return False
    
    if "-->" in lins[6]:
        return True
    else:
        return False
    
def process_srt(in_dir):
        doc_dirs = os.listdir(in_dir)
        for doc_dir in doc_dirs:
            related_docs_files = os.listdir(os.path.join(in_dir, doc_dir))
            for related_doc in related_docs_files:
                related_doc_path = os.path.join(in_dir, doc_dir, related_doc)
                if os.path.isdir(related_doc_path):
                    for video_file in os.listdir(related_doc_path):
                        video_path = os.path.join(related_doc_path, video_file)
                        if video_path.endswith("_processed.txt"):
                            continue
                        if isSRT(video_path):
                            srt2txt(video_path, video_path.split(".")[0]+"_processed.txt")

