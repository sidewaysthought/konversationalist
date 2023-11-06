import json
import argparse
import os
import openai
import sys
from chatagent import ChatAgent
from dotenv import load_dotenv


def load_personality():

    parser = argparse.ArgumentParser()
    parser.add_argument('--personality', default='personality.json')
    args = parser.parse_args()
    personality_file = args.personality

    try:
        with open(personality_file, 'r') as f:
            personality = json.load(f)
    except FileNotFoundError:
        print("Error: personality not found.")
        sys.exit(1)

    return personality


def setup_api():

    # Set OpenAI API URL to OPENAI_API_URL environment variable
    if "OPENAI_API_URL" not in os.environ:
        os.environ["OPENAI_API_URL"] = "https://api.openai.com"
    openai.api_base = os.environ["OPENAI_API_URL"]

    # Read OpenAI API key from environment variable
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable not found.")
        sys.exit(1)
    openai.api_key = os.environ["OPENAI_API_KEY"]

    if "OPENAI_MODEL" not in os.environ:
        print("Error: OPENAI_MODEL environment variable not found.")
        sys.exit(1)
    model = os.environ["OPENAI_MODEL"]

    return model


def __main__():

    load_dotenv()
    model = setup_api()
    personality = load_personality()

    # Set-up the chatbot
    chatbot = ChatAgent(
        system_msg = personality["system_prompt"],
        api_model = model
    )

    while True:

        # Get user input
        user_input = input("You: ")
        if user_input in ["exit", "\x1b"]:
            break
        bot_response = chatbot.add_to_conversation(user_input)

        print("AI: " + bot_response)


if __name__ == "__main__":
    __main__()