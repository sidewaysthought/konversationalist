import openai
import os
import sys

ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"


class ChatAgent:

    def __init__(self, role=ROLE_ASSISTANT, system_msg = "You are a helpful AI assistant.", api_model="local"):
        self.agent_role = role
        self.conversation = []
        self.chat_model = api_model

        starting_prompt = self.make_message(ROLE_SYSTEM, system_msg)
        self.conversation.append(starting_prompt)


    def make_message(self, role, message):
        return {
            "role": role,
            "content": message
        }
    

    def add_to_conversation(self, message):

        user_message = self.make_message(ROLE_USER, message)
        self.conversation.append(user_message)

        # Send conversation history to OpenAI Chatcomplete API and print response
        response = openai.ChatCompletion.create(
            model=self.chat_model,
            messages=self.conversation
        )
        
        response_content = response.choices[0].message.content.strip()
        bot_reply = self.make_message(ROLE_ASSISTANT, response_content)
        self.conversation.append(bot_reply)

        return response_content

