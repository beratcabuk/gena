> a Python cli secretary
# Gena the Cat
![image](https://github.com/beratcabuk/gena/assets/102920898/c5362e58-4abf-45b0-b611-c6ad6a83fd55)

# Gena the Software
 Gena is a GENerative ai powered Assistant that sets up hangout sessions via WhatsApp messages.
 
# A Quick Primer
 You need to set your own api key under a .env file. You can do this by adding the following line in the file.
 ```
 OPENAI_API_KEY=<your-api-key-here>
 ```

You currently use Gena by logging in via scanning the QR code it downloads, and stating a contact and an event. The driver does currently run in headless mode, so you can see the actions it takes live. You currently have to set up the Firefox driver by downloading [geckodriver](https://github.com/mozilla/geckodriver/releases/) and ensuring that it's findable from your PATH.
