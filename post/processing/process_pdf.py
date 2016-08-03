'''
Created on Aug 1, 2016

@author: pedrom
'''
from post.processing.utils import doc2txt
import os

def isPDF(doc_path):
    with open(doc_path, encoding="utf8", errors='ignore') as f:
        lins = f.readlines()
    if len(lins) <  3:
        return False
    
    if "#pdf\n" == lins[1]:
        return True
    else:
        return False
    
def process_pdf(in_dir):
        doc_dirs = os.listdir(in_dir)
        for doc_dir in doc_dirs:
            related_docs_files = os.listdir(os.path.join(in_dir, doc_dir))
            for related_doc in related_docs_files:
                related_doc_path = os.path.join(in_dir, doc_dir, related_doc)
                if not os.path.isdir(related_doc_path):
                    if isPDF(related_doc_path):
                        doc2txt(related_doc_path, related_doc_path.split(".")[0]+"_processed.txt", False)