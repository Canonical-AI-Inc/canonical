import json
import os
from typing import List

import time
import httpx
import openai
import requests
from dotenv import load_dotenv

load_dotenv(".env")

TEMPERATURE = 0
CACHECLIENT = openai.OpenAI(
    base_url=os.environ["CANONICAL_CACHE_HOST"],
    api_key="canbeanything",
    http_client=httpx.Client(
        headers={
            "X-Canonical-Api-Key": os.environ["CANONICAL_CACHE_API_KEY"],
        },
    ),
)

OPENAICLIENT = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


def complete(
    client: openai.OpenAI,
    messages: List[dict[str:str]],
    stream: bool,
    temperature: int = 0,
) -> openai.ChatCompletion:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        stream=stream,
        temperature=temperature,
        messages=messages,
    )


def displaycompletion(completion: openai.ChatCompletion, stream: bool) -> str:
    msg = ""
    if stream:
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                msg += chunk.choices[0].delta.content
                print(msg, end="", flush=True)
    else:
        msg = completion.choices[0].message.content
        print(msg)
    return msg


def updatecache(messages: List[dict[str:str]], temp: int = 0) -> None:
    requests.request(
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
                "model": "gpt-3.5-turbo",
            }
        ),
    )


def main() -> None:
    examplemsgs = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "assistant",
            "content": "Hi, how can I assist you today?",
        },
        {
            "role": "user",
            "content": "How do I improve latency in my application?",
        },
    ]
    stream = False
    try:
        response = complete(CACHECLIENT, examplemsgs, stream, TEMPERATURE)
        msg = displaycompletion(response, stream)
        examplemsgs.append({"role": "assistant", "content": msg})
    except openai.NotFoundError as e:
        stream = True
        response = complete(OPENAICLIENT, examplemsgs, stream, TEMPERATURE)
        msg = displaycompletion(response, stream)
        examplemsgs.append({"role": "assistant", "content": msg})
        updatecache(examplemsgs, TEMPERATURE)
        time.sleep(5)                                      # see caveats section in README


if __name__ == "__main__":
    main()
