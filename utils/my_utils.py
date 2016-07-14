'''
Created on Jun 29, 2016

@author: pedrom
'''
import re

def is_good_lin(lin):
    if len(lin) < 5:
        return False
    if no_letters(lin):
        return False
    return True

def no_letters(line):
    match = re.search('[a-zA-Z]', line)
    if match == None:
        return True
    return False