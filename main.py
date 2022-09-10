from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from deep_translator import GoogleTranslator
import setts


class EdubeTranslator():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://edube.org/login')

    def find_elements(self):
        return self.browser.find_elements(By.TAG_NAME, 'p') + self.browser.find_elements(By.TAG_NAME, 'strong') + self.browser.find_elements(By.TAG_NAME, 'li')

    def __send_keys(self, mail, password):
        self.browser.find_element(By.ID, "email").send_keys(mail)
        self.browser.find_element(By.ID, "password").send_keys(password)
        self.browser.find_element(By.XPATH, "//*[@id='content-wrap']/div/div/div/div/form/button").click()
        time.sleep(2)
        self.browser.get('https://edube.org/')

    def login(self):
        if setts.mail and setts.password:
            if input('Wanna use recent data(y/n)?\n').lower() == "y":
                self.__send_keys(setts.mail, setts.password)
        mail = input("ur mail ")
        password = input("ur password ")
        self.__send_keys(mail, password)


    def __translate_text(self, text):
        return GoogleTranslator(source="en", target="ru").translate(text)

    def wait_for_switch_site(self):
        url = self.browser.current_url
        while self.browser.current_url == url:
            print(url)
            time.sleep(3)
        print('Site Switched to ', self.browser.current_url)
        return True

    def process_data(self):
        ForAll = self.find_elements()
        if ForAll:
            for all in ForAll:
                print(all.text)
                try:
                    self.browser.execute_script(
                        f"var e = arguments[0]; e.insertAdjacentHTML('beforeend', '<br>{str(self.__translate_text(all.text))}')", all)
                except Exception as e:
                    print('woops, some error stack process: ', e)


if __name__ == "__main__":
    Chrome = EdubeTranslator()
    Chrome.login()
    Chrome.process_data()
    while Chrome.wait_for_switch_site():
        Chrome.process_data()
