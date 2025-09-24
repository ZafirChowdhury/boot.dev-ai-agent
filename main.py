import os
import sys

from dotenv import load_dotenv

from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

from functions.call_function import call_function

def main(): 
    if (len(sys.argv) < 2):
        print(f"Usage: python3 main.py <prompt> [--verbose]")
        sys.exit(1)

    verbose = False
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        verbose = True

    load_dotenv() # find .env file and sets the key for the current session
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("API key not foud!")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # avalable fuctions
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
    )

    # prompts
    system_prompt = system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.    
    """

    user_prompt = sys.argv[1]
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages, 
        config=types.GenerateContentConfig(system_instruction=system_prompt, 
                                           tools=[available_functions])
    )

    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)

            if not function_call_result.parts[0]:
                raise Exception("Fatal exception: Unexpected fuction call return")
    else:
        print(response.text)
    
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        print(f"-> {function_call_result.parts[0].function_response.response}")

main()
