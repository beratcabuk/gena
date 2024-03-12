from time import sleep
import sys
from driver import WhatsAppWeb
from chatbot import Bot
import terminalmessages

def main():
    # Initialize the driver and login to whatsaapp web.

    print(terminalmessages.SPLASH)
    print(terminalmessages.INTRO)
    user_name = input("Please enter your name and press ENTER...")
    input(terminalmessages.QR_BEFORE)
    waweb = WhatsAppWeb()
    waweb.save_qr()
    input(terminalmessages.QR_AFTER)

    # Find the contact.
    contact_name = input('''Please enter the name of the contact that you'd
                         like to message, and press ENTER...\n''')
    waweb.find_contact(contact_name)

    # Scroll up to load enough messages for context.
    waweb.scroll_up()

    # The messaging logic.
    conv_objective = input('''Please state the event that you want to set-up
                           with this person, and your availability. Then, press
                           ENTER...\n''')
    objective_achieved = False
    bot = Bot(model="gpt-4-1106-preview", user_full_name=user_name)
    while not objective_achieved:
        payload, sent_last = waweb.fetch_messaging_history()
        if sent_last:  # To ensure that the chatbot does not spam.
            sleep(2)  # Waiting for a response to our message here.
            continue

        msg = bot.respond(payload=payload, objective=conv_objective)

        # This is the conversation end signal.
        if bot.KILL_SIGNAL == msg[-5:]:
            msg = msg[:-5]
            objective_achieved = True
            waweb.send_message(payload=msg)
            break

        waweb.send_message(payload=msg)

    print(terminalmessages.SUCCESS)
    waweb.quit()
    sys.exit(1)

if __name__ == '__main__':
    main()
