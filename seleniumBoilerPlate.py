from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from multiprocessing import Process, Lock

from bs4 import BeautifulSoup

from dateutil.parser import parse
import re

import os
import csv
import json
from time import sleep
from pprint import pprint


def getSoup(driver):
    "returns a Bs4-soup instance of the current window"
    return BeautifulSoup(driver.execute_script('return document.documentElement.outerHTML'), 'html.parser')


def login(driver, id_, password, button, delay):
    """
    @param
        1: driver = Main selenium driver Instance
        2: id_ = dictionary with a key of 1-> name which means login id and 2->xpath: xpath of login username input field
        3: password = dictionary with a key of 1-> name which means login password and 2->xpath: xpath of password input field
        4: button =  xpath of submit button
        5: delay = (int) sleep after login

    """
    driver.find_element_by_xpath(id_['xpath']).send_keys(id_['name'])
    driver.find_element_by_xpath(password['xpath']).send_keys(password['name'])
    driver.find_element_by_xpath(button).click()
    sleep(delay)


def append_to_json(fname, data):
    a = []
    if not os.path.isfile(fname):
        a.append(data)
        with open(fname, mode='w') as f:
            f.write(json.dumps(a, indent=4))
    else:
        with open(fname) as feedsjson:
            feeds = json.load(feedsjson)

            feeds.append(data)
            with open(fname, mode='w') as f:
                f.write(json.dumps(feeds, indent=4))
                

def closeTabs(driver, noOfTabs):
    """
    @param
        1: driver = Main selenium driver Instance
        2: noOfTabs: specify how many tabs to open
    """
    for i in reversed(range(noOfTabs-1)):
        driver.switch_to_window(driver.window_handles[i])
        driver.close()

    driver.switch_to_window(driver.window_handles[0])


def switchTab(driver, i):
    """
    function to switch tab.
    """
    driver.switch_to_window(driver.window_handles[i])


def openTabs(driver, noOfTabs, link, curent):
    """
    function to open n-number of tabs specified by 
    @param
        1: noOfTabs: specify how many tabs to open
        2: link: link which will be used to open those tabs
        3: current: link to be opened in current tab
    """
    
    driver.switch_to_window(driver.window_handles[0])
    driver.get(curent)
    
    for i in range(noOfTabs-1):
        JS = 'window.open("' + link + '","_blank");'

        driver.execute_script(JS)

def waitForElement(xpath, driver, t):
    myElem = WebDriverWait(driver, t).until(EC.presence_of_element_located((By.XPATH, xpath)))
    
def removeDuplicate(fileName):
    finalList = []
    
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
    
        for row in reader:
            if not row in finalList:
                finalList.append(row)
    
    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        
        writer.writerows(finalList)


def scroll_down(driver, iterations, writer):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(iterations):
        
        print(i+1)
        # Scroll down to the bottom.
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        sleep(5)
        soup = getSoup(driver)
                
        links = soup.findAll(class_='snize-product')
        
        for link in links:
            l = [link.find('a').get('href')]
            
            writer.writerow(l)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    html = driver.execute_script('return document.documentElement.outerHTML')
    return html


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def is_email(string):
    return re.search('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', string)


def is_website(string):
    return re.search('^([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', string)

def clickButton(element, driver):
    driver.execute_script("arguments[0].click();", element)
    
if __name__ == "__main__":
    driver = webdriver.Chrome()
    
    # driver.get('https://na.account.amazon.com/ap/signin?_encoding=UTF8&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.pape.max_auth_age=0&ie=UTF8&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_lwa_na&marketPlaceId=ATVPDKIKX0DER&arb=80cfa011-4999-424b-88e1-c0fe086b9b63&language=en_US&openid.return_to=https%3A%2F%2Fna.account.amazon.com%2Fap%2Foa%3FmarketPlaceId%3DATVPDKIKX0DER%26arb%3D80cfa011-4999-424b-88e1-c0fe086b9b63%26language%3Den_US&enableGlobalAccountCreation=1&metricIdentifier=amzn1.application.eb539eb1b9fb4de2953354ec9ed2e379&signedMetricIdentifier=fLsotU64%2FnKAtrbZ2LjdFmdwR3SEUemHOZ5T2deI500%3D')

    # openTabs(driver, 10, 'https://www.linkedin.com/', 'https://www.linkedin.com/')

    # closeTabs(driver, 10)
    # driver.get('https://www.five8industries.com/five8-coilovers/')
    #removeDuplicate('links.csv')
