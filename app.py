import json
import argparse
import os
import openai
import sys
from chatagent import ChatAgent
from dotenv import load_dotenv


def load_personality():

    """
    Load personality from JSON file
    """

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

    """
    Set-up OpenAI API
    """

    # Response
    api_config = {
        "model": "",
        "context": 0
    }

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
    api_config["model"] = os.environ["OPENAI_MODEL"]

    if "OPENAI_CONTEXT" not in os.environ:
        print("Error: OPENAI_CONTEXT environment variable not found.")
        sys.exit(1)
    api_config["context"] = int(os.environ["OPENAI_CONTEXT"])

    return api_config


def __main__():

    """
    Main function
    """

    load_dotenv()
    api_config = setup_api()
    personality = load_personality()

    # Set-up the chatbot
    chatbot = ChatAgent(
        system_msg = personality["system_prompt"],
        api_model = api_config["model"],
        context_size = api_config["context"]
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