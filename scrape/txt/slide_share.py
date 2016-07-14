'''
fp = webdriver.FirefoxProfile()

fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","pdf")

browser = webdriver.Firefox(fp)
'''

import os
import time

from selenium import webdriver

download_dir = 'C:\\Users\\pedrom\\Downloads'
isLogIn = False
browser = webdriver.Chrome()

def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )
    
class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)
        
def get_slide_share_pp(pp_url):
    slide_share_login()
    prev_new_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key = os.path.getctime)
    
    browser.get(pp_url)
    
    try:
        browser.find_element_by_css_selector('li > .download').click()
    except Exception as e:
        print("%s power point not available to download" % pp_url)
        return None
    time.sleep(1)
    try:
        browser.find_element_by_css_selector('button.art-deco:nth-child(3)').click()
    except Exception as e:
        print()
    newest_pp = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key = os.path.getctime)
    while newest_pp == prev_new_file:
        newest_pp = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key = os.path.getctime)
        time.sleep(1)
    return newest_pp
    
def slide_share_login():
    global isLogIn, browser
    if isLogIn:
        return
    isLogIn = True
    browser.get('https://www.slideshare.net/login')
    
    username = browser.find_element_by_name('user_login')
    username.send_keys('pjdrm')
    
    password = browser.find_element_by_name('user_password')
    password.send_keys('249718513')
    
    form = browser.find_element_by_id('login_from_loginpage')
    with wait_for_page_load(browser):
        form.submit()