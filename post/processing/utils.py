'''
Created on Jul 20, 2016

@author: pedrom
'''

import re

from utils.my_utils import is_good_lin


caps = "([A-Z])"
lows = "([a-z])"
prefixes = "(etc|vs|Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Eg|Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])" 

def sentence_spliter(text, keepOriginalNewLine = False):
    text = " " + text + "  "
    if keepOriginalNewLine:
        text = text.replace("\n","<nl> ")
    else:
        text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(lows + "[.]" + lows + "[.]" + lows + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(lows + "[.]" + lows + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    if keepOriginalNewLine:
        text = text.replace("<nl> ", "<stop>")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def doc2txt(in_file_path, out_file_path, keepOriginalNewLine):
    with open(in_file_path, encoding="utf8", errors='ignore') as f:
        txt = ''.join(f.readlines()[2:])
    
    doc_sent_split = sentence_spliter(txt, keepOriginalNewLine)
    doc_sent_filtered = ""
    for sent in doc_sent_split:
        if is_good_lin(sent):
            doc_sent_filtered += sent + "\n"
    with open(out_file_path, "w+", encoding="utf8") as f:
        f.write(doc_sent_filtered[:-1])