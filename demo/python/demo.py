#!/usr/bin/env python3

# Initialize
import httpx
import os
import time
import requests
import json
import openai
from openai.types.chat import ChatCompletionChunk
import uuid
from dotenv import load_dotenv

load_dotenv(".env")

# User Input
MODEL = "gpt-4-0125-preview" # "gpt-3.5-turbo" 
SYSTEM_PROMPT = "You are a polite receptionist for Dr. Smith's dental office. Your name is Ben. Your office is located on Oak Grove Road in Walnut Creek. Don't say you're on Oak Grove Road unless you're asked about your location. There's another Dr Smith's dental office in Concord on Oak Grove."
ASSISTANT_PROMPT = "Hello, Dr. Smith's dental office. This is Ben. How can I help you today?"

# Clients
CACHE_CLIENT = openai.OpenAI(
    base_url=os.environ["CANONICAL_CACHE_HOST"],
    api_key="canbeanything",
    http_client=httpx.Client(
        headers={
            "X-Canonical-Api-Key": os.environ["CANONICAL_CACHE_API_KEY"],
        },
    ),
)

OPENAI_CLIENT = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

# Functions
def complete(client, messages, stream):
    return client.chat.completions.create(
        model=MODEL, 
        stream=stream,
        max_tokens=256,
        temperature=0.0,
        messages=messages,
    )

def update_cache(messages, temp: int = 0):
    response = requests.request(
        method="POST",
        url=f"{os.environ['CANONICAL_CACHE_HOST']}api/v1/cache",
        headers={
            "Content-Type": "application/json",
            "X-Canonical-Api-Key": os.environ["CANONICAL_CACHE_API_KEY"],
        },
        data=json.dumps(
            {
                "messages": messages,
                "temperature": temp,
                "model": MODEL,
            }
        ),
    )
    return response

def display_completion(completion, cache_hit, duration, stream):
    print("")
    print(f"CACHE HIT: {cache_hit}. TIME TO FIRST TOKEN: {round(duration, 3)} seconds.")
    print("")
    msg = ""
    if stream:
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:                
                print(chunk.choices[0].delta.content, end="", flush=True)
                msg += chunk.choices[0].delta.content     
        print("")
        print("")
    else:
        msg = completion.choices[0].message.content
        print(msg)
        print("")
    return msg

# Main
def main():
    
    # Edit system and assistant prompts here
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "assistant",
            "content": ASSISTANT_PROMPT,
        },
    ]

    # Print the conversation starter
    print(messages[-1]["content"])

    # Run the chat
    while True:
        messages.append(
            {
                "role": "user",
                "content": input(">>> "),
            }
        )
        try:
            start = time.perf_counter()
            response = complete(CACHE_CLIENT, messages, False)
            finish = time.perf_counter()
            duration = finish - start
            msg = display_completion(response, True, duration, False)
            messages.append({"role": "assistant", "content": msg})
        except openai.NotFoundError as e:
            response = complete(OPENAI_CLIENT, messages, True)
            finish = time.perf_counter()
            duration = finish - start
            msg = display_completion(response, False, duration, True)
            messages.append({"role": "assistant", "content": msg})
            update_cache(messages)


if __name__ == "__main__":
    main()