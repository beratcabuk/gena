from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from secrets import token_hex


load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")

class Bot:
    def __init__(self, model:str, user_full_name:str) -> None:
        self.client = OpenAI(api_key=API_KEY)
        self.model = model
        self.user_full_name = user_full_name
        self.KILL_SIGNAL = token_hex(3) # 3 bytes of random hexadecimal
    
    def respond(self, payload:str, objective:str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": f"""You are a helpful assistant designed to output JSON.
                                                The output should just include the response message, no additional data.
                                                Use the 'message' tag for the JSON object. You are designed to act as my secretary,
                                                respond to the incoming messages on my behalf. Do not use any emojis or special characters.
                                                Emulate my texting style, use all lowercase letters.
                                                The objective of this conversation is this: {objective}.
                                                The messages you will get will be in a fixed format: 
                                                [HH:MM, DD/MM/YYYY] The name of the sender: The message. If the message is a 
                                                reply to another, it's in the following format: [HH:MM, DD/MM/YYYY] The name of the sender: The name of the 
                                                person being replied to\\nThe message being replied to\\nThe reply. My name is {self.user_full_name}, any other name
                                                you see refers to the contact I am messaging. You will be provided with the last 10 messages for context.
                                                Please converse with the contact on my behalf by returning a response message as if you are me.
                                                Once the objective is reached, but you have to send a final message, return *123# at the end of the message.
                                                If the objective is reached, but you do not have to send another message, just return {self.KILL_SIGNAL}."""},
                {"role": "user", "content": payload}
            ]
            )
        msg = json.loads(response.choices[0].message.content)['message']

        return msg
