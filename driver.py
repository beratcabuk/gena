from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

WEBSITE_URL = 'https://web.whatsapp.com/'

class Driver:
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get(WEBSITE_URL)
        sleep(10)

    def save_qr(self) -> None:
        self.qr_element = self.driver.find_element(By.CLASS_NAME, '_19vUU')
        self.qr_element.screenshot(filename='qr.png')
    
    def find_contact(self, contact_name: str) -> None:
        self.contact_name = contact_name
        self.search_box = self.driver.find_element(By.CSS_SELECTOR, '.qh0vvdkp')
        self.search_box.click()
        sleep(1)

        for i in range(len(self.contact_name)):
            self.search_box.send_keys(self.contact_name[i])
            sleep(0.1)
        self.search_box.send_keys(Keys.ENTER)
    
    def scroll_up(self) -> None:
        for i in range(5):
            self.driver.find_element(By.CSS_SELECTOR, '.n5hs2j7m').send_keys(Keys.PAGE_UP)
            sleep(0.5)

    def fetch_messaging_history(self, n_last_messages:int = 10) -> (str, bool):
        self.visible_msgs = self.driver.find_elements(By.CLASS_NAME, 'cm280p3y.to2l77zo.n1yiu2zv.c6f98ldp.ooty25bp.oq31bsqd')
        last_n = []
        for i in range(1, n_last_messages + 1):
            msg = self.visible_msgs[-i].find_element(By.TAG_NAME, 'div')
            msg_text = msg.text
            msg_metadata = msg.get_attribute('data-pre-plain-text')
            last_n.append(msg_metadata + msg_text)
        last_n_messages = ''.join(last_n[::-1])

        # If the last message is not from the contact, we sent it.
        sent_last_message = bool(last_n[0].split(' ')[2][:-1] != self.contact_name)
        return (last_n_messages, sent_last_message)

    def send_message(self, payload: str) -> None:
        input_box = self.driver.find_element(By.CSS_SELECTOR, '._3Uu1_ > div:nth-child(1) > div:nth-child(1)')
        sleep(1)
        input_box.click()
        sleep(1)
        for i in range(len(payload)):
            input_box.send_keys(payload[i])
            sleep(0.1)
        input_box.send_keys(Keys.ENTER)

    def quit(self) -> None:
        sleep(0.5)
        self.driver.quit()
