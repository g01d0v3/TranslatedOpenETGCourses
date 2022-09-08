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
        self.browser.find_element(By.ID, "email").send_keys(mail)
        self.browser.find_element(By.ID, "password").send_keys(password)
        self.browser.find_element(By.XPATH, "//*[@id='content-wrap']/div/div/div/div/form/button").click()
        time.sleep(2)
        self.browser.get('https://edube.org/')

    def __translate_text(self, text):
        translated = GoogleTranslator(source="en", target="ru").translate(text)
        print(translated)
        return translated

    def wait_for_switch_site(self):
        url = self.browser.current_url
        while self.browser.current_url == url:
            print(url)
            time.sleep(6)
        print('Site Switched to ', self.browser.current_url)
        return True

    def process_data(self):
        if self.find_elements():
            for all in self.find_elements():
                print(all.text)
                try:
                    self.browser.execute_script(
                        f"var e = arguments[0]; e.insertAdjacentHTML('beforeend', '<br>{str(self.__translate_text(all.text))}')",
                        all)
                except Exception as e:
                    print('woops, some error stack process: ', e)


if __name__ == "__main__":
    Chrome = EdubeTranslator()
    Chrome.login()
    Chrome.process_data()
    while Chrome.wait_for_switch_site():
        Chrome.process_data()
