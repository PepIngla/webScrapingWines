# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 08:03:54 2022

"""

from selenium import webdriver
from urllib.robotparser import RobotFileParser
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.parse
from fake_useragent import UserAgent
import pandas as pd
import time
import re


def crawler_buttons(seed_url, scraper, num_max = -1):
    '''
    
    Crawls through the page given by the seed_url by pressing at the button
    "Siguiente" over and over until reaching the page limit or num_max, the
    maximum number of pages we want to scrap
    Parameters
    ----------
    seed_url : TYPE, string
        DESCRIPTION: The URL of the page that will be scraped.
    num_max : TYPE, optional
        DESCRIPTION. The default is -1.
    scraper : TYPE, optional
        DESCRIPTION. Name of the function to be used to scrap the website. 
        It should only take one input: the html file.

    Returns
    -------
    df : TYPE, Pandas data frame
        DESCRIPTION. Contains all the data extracted from scraping the page
        and its content is defined by the scraper function.

    '''
    global throttle
    df=pd.DataFrame()
    rp = RobotFileParser()#urllib.robotparser.
    base_url = re.findall(r'(.*)/es/vinos/(a*)',seed_url)
    rp.set_url(urllib.parse.urljoin(base_url[0][0], 'robots.txt'))
    rp.read()
    # Here I call the webdriver using a user agent which changes randomly
    # https://stackoverflow.com/questions/49565042/way-to-change-google-chrome-user-agent-in-selenium
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(options=options)
    actUserAgent = driver.execute_script("return navigator.userAgent;")
    assert userAgent == actUserAgent
    print(actUserAgent)
    driver.get(seed_url)
    # First we need to click on the cookie accepting button
    buttons = driver.find_elements(by=By.TAG_NAME, value="button")
    for button in buttons:
        if button.text == "ACEPTAR":
            button.click()
    
    # In case the number of pages to scrap is not specified
    # the code sets it to its maximum value
    buttons = driver.find_elements(by=By.TAG_NAME, value="button")
    if num_max < 1:
        for i, b in enumerate(buttons):
            if b.text == 'Siguiente':
                i_max = i-1 
        num_max = int(buttons[i_max].text)
        print(num_max)
    # Now the scraping can start
    num_pages = 0
    # To obtain a varied dataset that is not too heavy, we have limited the amount
    # of pages to scrap of each type of wine
    if rp.can_fetch(seed_url, userAgent):
        while num_pages < num_max:
            throttle.wait(driver.current_url)
            html = driver.page_source

            print('Call to scraper')
            # Here we call the scraper to append its output to the dataframe. 
            df = pd.concat([df,scraper(html)],ignore_index=True)
            account_buttons = driver.find_elements(by=By.XPATH, value="//span[@role='button']")     
            for b in account_buttons:
                print('Finestra tancada')
                b.click()
            # The line below is repeated to avoid StaleElementReferenceException
            # https://stackoverflow.com/questions/18225997/stale-element-reference-element-is-not-attached-to-the-page-document
            buttons = driver.find_elements(by=By.XPATH, value="//button[@class='btn-as-link']")
            
            for button in buttons[::-1]:
                # Order inverted to speed up 
                if  button.text == "Siguiente":
                    button.click()
                    
            num_pages += 1
        driver.quit() 
    return df

class Throttle:
    """
    Add a delay between downloads to the same domain
    Ref. R. Lawson, Web Scraping with Python Packt Publishing, Limited (2015)
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}
    def wait(self, url):
        domain = urllib.parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (time.time() -
            last_accessed)
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
            # update the last accessed time
        self.domains[domain] = time.time()


def link_crawler(seed_urls, scraper, delay=1, num_max=-1):
    '''
    Function that initializes the throttle object which controls the waiting
    times between page loadings and iterates through the requested pages.
    If URLs are repeated they will be scanned again and repeated data will be
    introduced into the dataframe.
    
    This function also saves the final dataset on a file called: vins.csv

    Parameters
    ----------
    seed_urls : TYPE, list
        DESCRIPTION. URLs to be scraped.
    delay : TYPE, int or float
        DESCRIPTION. delay between consecutive loadings of the web page.
    num_max : TYPE, int or float
        DESCRIPTION. maximum number of pages to be crawled by crawler_buttons.
        if it is smaller than 1 then it will crawl through all the pages of that
        type of wine.
    scrapper : TYPE, function
        DESCRIPTION. Function used to scrap the website
    Returns
    -------
    df : TYPE, pandas dataframe
        DESCRIPTION. dataset extracted from the web page

    '''
    global throttle
    df = pd.DataFrame()
    throttle = Throttle(delay)
    for seed_url in seed_urls:
        df = pd.concat([df,crawler_buttons(seed_url, scraper, num_max)], ignore_index=True)
    fname = 'vins.csv' 
    df.to_csv(fname, index=False)
    return df
