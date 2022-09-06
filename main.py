from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from deep_translator import GoogleTranslator

browser = webdriver.Chrome()
browser.get('https://edube.org/login')

def FindElements():
    ForAll = browser.find_elements(By.TAG_NAME, 'p') + browser.find_elements(By.TAG_NAME, 'strong')
    return ForAll
def login():
    mail = input("ur mail ")
    password = input("ur password ")
    login_field = browser.find_element(By.ID, "email").send_keys(mail)
    password_field = browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.XPATH, "//*[@id='content-wrap']/div/div/div/div/form/button").click()
def translator(text):
    translated = GoogleTranslator(source="en", target="ru").translate(text)
    print(translated)
    return translated

def WaitForSwitchSite():
    url = browser.current_url
    while browser.current_url == url:
        print(url)
        time.sleep(6)
    print ('Site Switched to ', browser.current_url)
    DataProcessing()
def DataProcessing():
    ForAll = FindElements()
    if ForAll:
        i=0
        for all in ForAll:
            print(all.text)
            browser.execute_script(f"var e = arguments[0]; e.insertAdjacentHTML('beforeend', '<br>{str(translator(all.text))}')", ForAll[i])
            i += 1
    WaitForSwitchSite()
login()
DataProcessing()
