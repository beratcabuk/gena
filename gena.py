import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from openai import OpenAI
import json
import sys

# Initialize the driver and login to whatsaapp web.
print('Welcome to GenA, your Generative AI powered personal assistant!\n')
input('Press ENTER to get the login QR code...\n')
driver = webdriver.Firefox()
driver.get('https://web.whatsapp.com/')
time.sleep(10)
content = driver.find_element(By.CLASS_NAME, '_19vUU')
content.screenshot(filename='./qr.png')
input('Press ENTER after scanning the QR code...\n')

# Find the contact.
contact_name = input("Please enter the exact name of the contact that you'd like to message, as it is saved in your WhatsApp, and press ENTER.\n")
search_box = driver.find_element(By.CSS_SELECTOR, '.qh0vvdkp')
search_box.click()
time.sleep(1)
for i in range(len(contact_name)):
    search_box.send_keys(contact_name[i])
    time.sleep(0.1)
search_box.send_keys(Keys.ENTER)

# Scroll up to load enough messages for context.
for i in range(5):
    driver.find_element(By.CSS_SELECTOR, '.n5hs2j7m').send_keys(Keys.PAGE_UP)
    time.sleep(0.5)

# The messaging logic.
conv_objective = input("Please state the event that you want to set-up with this person, and your availability. Then, press ENTER.\n")
objective_achieved = False
while not objective_achieved:
    incoming_msgs = driver.find_elements(By.CLASS_NAME, 'cm280p3y.to2l77zo.n1yiu2zv.c6f98ldp.ooty25bp.oq31bsqd')
    last_10 = []
    for i in range(1, 10):
        msg = incoming_msgs[-i].find_element(By.TAG_NAME, 'div')
        msg_text = msg.text
        msg_metadata = msg.get_attribute('data-pre-plain-text')
        last_10.append(msg_metadata + msg_text)
        payload = ''.join(last_10[::-1])
    if last_10[0].split(' ')[2][:-1] != contact_name:  # To ensure that the chatbot does not spam.
        time.sleep(2)
        continue

    client = OpenAI(api_key='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')

    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": f"""You are a helpful assistant designed to output JSON.
                                        The output should just include the response message, no additional data.
                                        Use the 'message' tag for the JSON object. You are designed to act as my secretary,
                                        respond to the incoming messages on my behalf. Do not use any emojis or special characters.
                                        The objective of this conversation is this: {conv_objective}.
                                        The messages you will get will be in a fixed format: 
                                        [HH:MM, DD/MM/YYYY] The name of the sender: The message. If the message is a 
                                        reply to another, it's in the following format: [HH:MM, DD/MM/YYYY] The name of the sender: The name of the 
                                        person being replied to\\nThe message being replied to\\nThe reply. My name is Berat Çabuk, any other name
                                        you see refers to the contact I am messaging. You will be provided with the last 10 messages for context.
                                        Please converse with the contact on my behalf by returning a response message as if you are me.
                                        Once the objective is reached, but you have to send a final message, return *123# at the end of the message.
                                        If the objective is reached, but you do not have to send another message, just return *123#."""},
        {"role": "user", "content": payload}
    ]
    )

    msg = json.loads(response.choices[0].message.content)['message']

    if '*123#' == msg[-5:]:
        print(msg, "\n")
        msg = msg[:-5]
        print(msg, "\n")
        objective_achieved = True
        input_box = driver.find_element(By.CSS_SELECTOR, '._3Uu1_ > div:nth-child(1) > div:nth-child(1)')
        time.sleep(1)
        input_box.click()
        time.sleep(1)
        for i in range(len(msg)):
            input_box.send_keys(msg[i])
            time.sleep(0.1)
        input_box.send_keys(Keys.ENTER)
        time.sleep(0.5)
        break

    input_box = driver.find_element(By.CSS_SELECTOR, '._3Uu1_ > div:nth-child(1) > div:nth-child(1)')
    time.sleep(1)
    input_box.click()
    time.sleep(1)
    for i in range(len(msg)):
        input_box.send_keys(msg[i])
        time.sleep(0.1)
    input_box.send_keys(Keys.ENTER)

print('The objective you set is achieved.')
driver.quit()
sys.exit(1)
