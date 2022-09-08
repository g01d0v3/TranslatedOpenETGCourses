from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from deep_translator import GoogleTranslator
import setts


class EdubeTranslator():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://edube.org/login')
        self.login()

    def FindElements(self):
        ForAll = self.browser.find_elements(By.TAG_NAME, 'p') + self.browser.find_elements(By.TAG_NAME, 'strong') + self.browser.find_elements(By.TAG_NAME, 'li')
        return ForAll


    def login(self):
        if setts.mail and setts.password:
                if input('Wanna use recent data(y/n)?\n').lower() == "y":
                    mail, password = setts.mail, setts.password
                else:
                    mail = input("ur mail ")
                    password = input("ur password ")
        else:
            mail = input("ur mail ")
            password = input("ur password ")
        login_field = self.browser.find_element(By.ID, "email").send_keys(mail)
        password_field = self.browser.find_element(By.ID, "password").send_keys(password)
        self.browser.find_element(By.XPATH, "//*[@id='content-wrap']/div/div/div/div/form/button").click()
        time.sleep(3)
        self.browser.get('https://edube.org/')
        self.DataProcessing()


    def translator(self, text):
        translated = GoogleTranslator(source="en", target="ru").translate(text)
        print(translated)
        return translated


    def WaitForSwitchSite(self):
        url = self.browser.current_url
        while self.browser.current_url == url:
            print(url)
            time.sleep(6)
        print ('Site Switched to ', self.browser.current_url)
        self.DataProcessing()


    def DataProcessing(self):
        ForAll = self.FindElements()
        if ForAll:
            i=0
            for all in ForAll:
                print(all.text)
                try:
                    self.browser.execute_script(f"var e = arguments[0]; e.insertAdjacentHTML('beforeend', '<br>{str(self.translator(all.text))}')", all)
                except Exception as e:
                    print('woops, some error stack process: ', e)
        self.WaitForSwitchSite()


if __name__ == "__main__":
    Chrome = EdubeTranslator()
