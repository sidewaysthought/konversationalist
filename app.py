import openai
import os
import json
import argparse
import sys
from dotenv import load_dotenv


def setup_openai():

    # Set OpenAI API URL to OPENAI_API_URL environment variable
    if "OPENAI_API_URL" not in os.environ:
        os.environ["OPENAI_API_URL"] = "https://api.openai.com"
    openai.api_base = os.environ["OPENAI_API_URL"]

    # Read OpenAI API key from environment variable
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable not found.")
        sys.exit(1)
    openai.api_key = os.environ["OPENAI_API_KEY"]


def load_personality(personality_file):

    try:
        with open(personality_file, 'r') as f:
            personality = json.load(f)
    except FileNotFoundError:
        print("Error: personality not found.")
        sys.exit(1)

    return personality


def get_user_input():

    user_message = input("You: ")

    return {
        "role": "user",
        "content": user_message
    }


def __main__():

    conversation_history = []
    user_message = ""

    # Set up OpenAI API
    load_dotenv()
    setup_openai()

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--personality', default='personality.json')
    args = parser.parse_args()
    personality = load_personality(args.personality)

    # Send system prompt to OpenAI Chatcomplete API and print response
    system_message = {
        "role": "system",
        "content": personality["system_prompt"]
    }
    conversation_history.append(system_message)

    while True:
        
        # Get user input
        user_message = get_user_input()
        if user_message["content"] in ["exit", "\x1b"]:
            break
        conversation_history.append(user_message)

        # Send conversation history to OpenAI Chatcomplete API and print response
        response = openai.ChatCompletion.create(
            model="local",
            messages=conversation_history
        )

        print("Bot: " + response.choices[0].message.content)



if __name__ == "__main__":
    __main__()