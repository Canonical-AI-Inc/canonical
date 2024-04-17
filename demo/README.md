# Python Demo Script

This is a simple demo that can be run from the command line. 

## Setup

First, create a virtual environment and install the necessary dependencies

```bash
conda create -n canonical python=3.10
conda activate canonical
pip install -r requirements.txt
```

Next, create a `.env` file in the root of the project with the following contents:

```bash
cp .env.example .env
```

Then, replace the `CANONICAL_API_KEY` ([email us](mailto:hello@canonical.chat) for a key) and the `OPENAI_API_KEY` values in the `.env` file with their actual values.

Then, run the script:

```bash
python demo.py
```

## How To Use The Demo

1. Update the `SYSTEM_PROMPT` in `demo.py` to start a new cache.
2. Save `demo.py`.
3. Run the script.
3. Start chatting with the LLM.

## When Can I Expect a Cache Hit?

The Canonical AI Semantic Cache is built for Conversational AI. For caching to work in a conversational application, the semantic cache must be aware of the chat history and the context of each query. In other words, a cache hit requires the user query and previous user-LLM interactions to match. As such, asking the same thing over and over won't necessarily produce a cache hit. After all, you wouldn't want that to be the experience in human conversations!

Here are some tips:
1. Start a new cache by updating `SYSTEM_PROMPT` in `demo.py`.
2. Save `demo.py`.
2. Run the script and have a conversation with the LLM in your terminal. The new cache will get populated with LLM responses.
3. Type `Ctrl + C` to stop the session. Then, type `python demo.py` to start a new conversation.
4. Have a new conversation with the LLM. When you ask questions similar to what you asked in your last conversation, you'll get cache hits.
5. Note: the cache update lag is set to five seconds for this demo. This is important for conversational LLM caching because it prevents the user and LLM from getting stuck in a loop.

## Example

Update the `SYSTEM_PROMPT` in `demo.py` to start a new cache. Then, run the script with `python demo.py` to start a conversation.

```
Assistant: Hello, Dr. Smith's dental office. This is Tim. How can I help you today?

User (you): Hi, do you have any appointments for today?

Assistant: I'm sorry, we don't. (Cache Hit: False, assuming you've updated the System Prompt and you're working in a new cache.)

User (you): How about Sunday?

Assistant: I apologize for any inconvenience, but our office is closed on Sundays. (Cache Hit: False, assuming you've updated the System Prompt and you're working in a new cache.)

```

Type `Ctrl + C` to end the conversation. Then, type `python demo.py` to start a new conversation.

```
Assistant: Hello, Dr. Smith's dental office. This is Tim. How can I help you today?

User (you): Hi, do you have any appointments for later today?

Assistant: I'm sorry, we don't. (Cache Hit: True)

User (you): What about Sunday?

Assistant: I apologize for any inconvenience, but our office is closed on Sundays. (Cache Hit: True)

User (you): What about Monday?

Assistant: Certainly! We have availability on Monday. (Cache Hit: False)

```

## Learn More

For more information about the Canonical AI LLM Cache, visit us [here!](https://canonical.chat/) Or [email us](mailto:hello@canonical.chat) for an API key for your project! We'd love to hear from you!
