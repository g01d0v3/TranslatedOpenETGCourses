from colorama import Fore
import selenium.common.exceptions
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

    def __write_config(self, mail, password):
        with open("setts.py", "a") as file:
            file.truncate(0)
            file.write(
                f"mail = \'{mail}\'\n"
                f"password = \'{password}\'"
            )
            file.close()

    def __send_keys(self, mail, password):
        self.browser.find_element(By.ID, "email").send_keys(mail)
        self.browser.find_element(By.ID, "password").send_keys(password)
        self.browser.find_element(By.XPATH, "//*[@id='content-wrap']/div/div/div/div/form/button").click()
        time.sleep(2)
        if self.browser.current_url=='https://edube.org/study':
            self.browser.get('https://edube.org/')
        else:
            print("Invalid credentials.")

    def login(self):
        if setts.mail and setts.password:
            if input('Wanna use recent data(y/n)?\n').lower() == "y":
                self.__send_keys(setts.mail, setts.password)
                return
        mail = input("ur mail ")
        password = input("ur password ")
        self.__write_config(mail, password)
        self.__send_keys(mail, password)

    def __translate_text(self, text):
        return GoogleTranslator(source="en", target="ru").translate(text)

    def wait_for_switch_site(self):
        url = self.browser.current_url
        while self.browser.current_url == url:
            time.sleep(2)
        print(Fore.BLUE + 'Site Switched to ', self.browser.current_url, Fore.RESET)

        return True

    def process_data(self):
        ForAll = self.find_elements()
        url = self.browser.current_url
        if ForAll:
            for one in ForAll:
                try:
                    self.browser.execute_script(
                        f"var e = arguments[0]; e.insertAdjacentHTML('beforeend', '<br>{str(self.__translate_text(one.text))}')", one)

                except selenium.common.exceptions.JavascriptException as e:
                    print(f'{Fore.RED}couldn\'t add text:\n{Fore.RESET}{one.text}\n', f'{Fore.BLUE}element:{Fore.RESET} {one}')

                except selenium.common.exceptions.StaleElementReferenceException:
                    if self.browser.current_url != url:
                        print("Site switched")
                        self.process_data()

                except Exception as e:
                    print(f'{Fore.RED}woops, some error stack process: {Fore.RESET}', e)


if __name__ == "__main__":
    try:
        Chrome = EdubeTranslator()
        Chrome.login()
        Chrome.process_data()
        while Chrome.wait_for_switch_site():
            Chrome.process_data()
    except KeyboardInterrupt:
        quit()
