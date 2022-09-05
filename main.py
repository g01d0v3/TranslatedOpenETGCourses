from selenium import webdriver
from selenium.webdriver.common.by import By
import time

browser = webdriver.Chrome()
browser.get('https://edube.org')
strong = 31
def DataProcessing():
    ForP = browser.find_elements(By.TAG_NAME, 'p')
    ForStrong = browser.find_elements(By.TAG_NAME, 'strong')
    for p in ForP:
        print(p.text)
    for strong in ForStrong:
        print(strong.text)
    WaitForSwitchSite()

def WaitForSwitchSite():
    url = browser.current_url
    while browser.current_url == url:
        print(url)
        time.sleep(6)
    print ('Site Switched to ', browser.current_url)

DataProcessing()
