from time import sleep
import sys
from driver import Driver
from chatbot import Bot

def main():
    # Initialize the driver and login to whatsaapp web.
    print('Welcome to GenA, your Generative AI powered personal assistant!\n')
    user_name = input("Please enter your full name and press ENTER...")
    input('Press ENTER to get the login QR code...\n')
    driver = Driver()
    driver.save_qr()
    input('Press ENTER after scanning the QR code...\n')

    # Find the contact.
    contact_name = input("Please enter the name of the contact that you'd like to message, and press ENTER...\n")
    driver.find_contact(contact_name)

    # Scroll up to load enough messages for context.
    driver.scroll_up()

    # The messaging logic.
    conv_objective = input("Please state the event that you want to set-up with this person, and your availability. Then, press ENTER...\n")
    objective_achieved = False
    bot = Bot(model="gpt-4-1106-preview", user_full_name=user_name)
    while not objective_achieved:
        payload, sent_last = driver.fetch_messaging_history()
        if sent_last:  # To ensure that the chatbot does not spam.
            sleep(2)  # Waiting for a response to our message here.
            continue

        msg = bot.respond(payload=payload, objective=conv_objective)

        # This is the conversation end signal.
        if '*123#' == msg[-5:]:
            msg = msg[:-5]
            objective_achieved = True
            driver.send_message(payload=msg)
            break

        driver.send_message(payload=msg)

    print('The objective you set is achieved.')
    driver.quit()
    sys.exit(1)

if __name__ == '__main__':
    main()
