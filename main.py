from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from deep_translator import GoogleTranslator

browser = webdriver.Chrome()
browser.get('https://edube.org')
ForAll = browser.find_elements(By.XPATH, "//*[text()]")

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

def DataProcessing():
    for all in ForAll:
        i=0
        print(all.text)
        for one in str(all.text).split(sep='\n'):
            i+=1
            print(one)
            try:
                browser.execute_script(f"var e = arguments[0]; e.innerText = '{str(translator(one))}'", ForAll[i])
            except:
                pass
        WaitForSwitchSite()
DataProcessing()


