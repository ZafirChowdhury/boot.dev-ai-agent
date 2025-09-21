import os
import sys

from dotenv import load_dotenv

from google import genai
from google.genai import types

def main(): 
    if (len(sys.argv) < 2):
        print(f"Usage: python3 main.py <prompt> [--verbose]")
        sys.exit(1)

    load_dotenv() # find .env file and sets the key for the current session
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("API key not foud!")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )

    print(response.text)

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

main()
