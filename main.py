import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("API key from Openrouter not found!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
##############################################
# everything above here is setup
# everything below is the actual robot logic
##############################################
for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    message = response.choices[0].message
    messages.append(message)

    if response.usage is None:
        raise RuntimeError("Potentially failed API request. No AI usage data found.")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")
        verb = True
    else:
        verb = False

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            # print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, verb)
            messages.append(result_message)
            if result_message["content"] is None:
                raise ValueError("empty content")
            if verb:
                print(f"-> {result_message['content']}")

    else:
        print(message.content)
        break
    if _ == 20:
        print("Maximum number of iterations reached without a final agent response. Fine-tune your query, or perhaps ask a different question.")
        sys.exit(1)

sys.exit(0)
