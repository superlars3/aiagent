import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from functions.config import MAX_ITERS


model_name = 'gemini-2.0-flash-001'
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv

    if len(sys.argv) == 1:
        print("No question was asked")
        sys.exit(1)
    args = sys.argv[1:]
    user_prompt = " ".join(args)
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iterations = 0
    while True:
        iterations += 1  # Every loop the amount of iterations goes up by 1, can set up a maximum somewhere here to prevent infinite loops.
        if iterations > MAX_ITERS: # Can also make a variable here and save it somewhere else to not have to edit main() if changes are needed.
            print(f"Max amount of iterations reached: {iterations}")
            sys.exit(1)  # Exits the program if max iterations is exceeded

        try:
            end_response = generate_content(client, messages, verbose, user_prompt)
            if end_response:
                print("Final response:")
                print(end_response)
                break
        except Exception as e:
            print("Error:", e)
            break 


def generate_content(client, messages, verbose, user_prompt):
    response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt),
    )
    for candidate in response.candidates:
        messages.append(candidate.content)

    if not response.function_calls and response.text:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        function_responses.append(function_call_result.parts[0])

    # Wrap all tool responses into one user message if there are actual tool responses:
    if function_responses:
        messages.append(
            types.Content(
                role="user",
                parts=function_responses,
            )
        )



    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)



if __name__ == "__main__":
    main()
