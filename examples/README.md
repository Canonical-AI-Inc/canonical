# Python Example Script

This is a simple example of a Python script that can be run from the command line. 

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

Then, replace the `CANONICAL_API_KEY` and the `OPENAI_API_KEY` values in the `.env` file with their actual values.

Then, run the script:

```bash
python example.py
```

## When Can I Expect a Cache Hit?

The Canonical AI Semantic Cache is built for Conversational AI. For caching to work in a conversational application, the semantic cache must be aware of the chat history and the context of each query. In other words, a cache hit requires the user query and previous user-LLM interactions to match. As such, asking the same thing over and over won't necessarily produce a cache hit. After all, you wouldn't want that to be the experience in human conversations!

Here are some tips:
1. Start a new cache by updating your System Prompt.
2. Run the script and have a conversation with the LLM. The new cache will get populated with LLM responses.
3. End the session, then start a new session. When you ask questions similar to what you asked in your last conversation, you'll get cache hits.

Caveats:
1. The cache update lag is set to five seconds for this demo. This is important for conversational LLM caching because it prevents the user and LLM from getting stuck in a loop.
2. For privacy reasons, we don't cache queries with sensitive information like social security numbers. If you want a cache hit, don't use sensitive information.
3. Set the temperature parameter to 0. If the temperature is greater than 0, the cache gets populated with more than one LLM response per key. At temperature greater than zero, you won't see cache hits for a given query until the cache is fully populated.

Here is an example:

![canonical-ai-semantic-cache-demo--dentist-office-location-40s](https://github.com/Canonical-AI-Inc/canonical/assets/640297/ef067753-98b7-4441-b27a-86c45f5bde6a)
