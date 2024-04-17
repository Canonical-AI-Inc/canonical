# Canonical AI

Context-Aware Semantic Cache for Conversational AI

## How Does Semantic Caching Work?

For each user query, first semantically search the cache for what is essentially the same query – even if the query phrasing is different. If a match is found in the semantic cache, return the response from the semantic cache rather than calling the LLM. A cache hit has a faster response time and costs less compared to an LLM.

## Semantic Cache Demo

![canonical-ai-semantic-cache-demo--dentist-office-location-40s](https://github.com/Canonical-AI-Inc/canonical/assets/640297/91116289-d86e-4f96-8057-ea987525e39d)

In the first conversation, the user asks new questions, the LLM responds, and the cache gets populated. 

In the second conversation (after the terminal is cleared), the user asks the same questions, but with different phrasing. The responses are returned from the semantic cache and the time to first token is 10x faster.

## Features

- **Fast Semantic Caching.** Response times are ~40 ms for on-prem deployments and ~120 ms for over-the-network. 
- **High Precision Semantic Caching.** Quality is paramount for your user experience. On a cache hit, the Canonical Cache correctly answers the user query. 
- **High Recall Semantic Caching.** Get cache hits even for applications where you wouldn’t expect many cache hits. 
- **Multitenancy.** Each product, each AI persona, or each user can have its own cache. You decide the scope of the cache.
- **Tunable Cache Temperature.** You decide whether you want a cache hit to return the same response or differently phrased responses.
- **Simple Integration.** Deploy our LLM Cache one step upstream of your LLM call. If there’s a cache hit, don’t call your LLM. If there’s a cache miss, then update the semantic cache with the LLM completion after you’ve responded to the user.

## Performance

### _Accuracy_ 

Context-awareness is essential for accurate semantic caching. By including many conversation turns in each cache key, the Canonical Cache returns relevant and accurate values.

### _Speed_

Our LLM Cache returns responses in about 40 milliseconds for on-premise deployments and about 120 milliseconds for API calls. 

### _Hit Rate_

The average hit rate for the Canonical Cache is about 15%. Even in open-ended conversations, our LLM cache gets hits in the beginning and end of a session. The first and final impressions are critical for user experience.

### _Build Versus Buy_

A simple cosine similarity search cache is so inaccurate that it would kill your product. For more complicated applications, like conversational AI, semantic caching isn’t something developers build in an afternoon. 

Whether you’re a startup or an established player, you’re in a race with everyone else to capture the spoils of Generative AI. 

Deploy the Canonical Cache and get there faster.

## Integration

_API and Proxy_

You connect with the Canonical Cache via an API call. You call the Canonical Cache before you call the LLM API. If the Canonical Cache finds a hit, it returns the cached response. If there is no cache hit, then Canonical returns a 404 and you then call the LLM. You can also integrate Canonical via proxy integration using the Open AI base URL. Check out the python example below. [See here](https://github.com/Canonical-AI-Inc/canonical) for more detailed examples.

```python
import httpx
import openai
import os
import requests

# create an OpenAI client that points to Canonical
client = openai.OpenAI(
  base_url="https://cacheapp.canonical.chat/",
  http_client=httpx.Client(
      headers={
          "X-Canonical-Api-Key": "<api_key>",
      },
    ),
)

# Instead of sending the request to your LLM, send it to Canonical.
# Catch the 404 on a cache miss.
try:
    completion = client.chat.completions.create(...)
except openai.NotFoundError as e:
    # send to LLM

# After receiving the response from the LLM, send it to Canonical to cache it.
requests.request(
    method="POST",
    url="https://cacheapp.canonical.chat/api/v1/cache",
    headers={
        "Content-Type": "application/json",
        "X-Canonical-Api-Key": "<api_key>",
    },
    data=json.dumps({
        "temperature": "<temperature>",
        "messages": "<msglist>",
    })
)
```

_On-Prem_

Coming soon! We're working on seemless Docker and Helm deployments.

## Save 50% On Your LLM Token Costs

We charge only for cache hits. Whatever model you're using, we charge 50% of the per token price on cache hits.

## Don't Delay On Dropping Latency

If you're interested in trying out the Canonical Cache, please [email us!](mailto:hello@canonical.chat) We'll send you an API key. 
