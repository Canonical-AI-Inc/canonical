# Canonical AI

Context-Aware Semantic Cache for Conversational AI

## How Does Simple Semantic Caching Work?

For simple, context-agnostic semantic caching, take the user query and perform a vector search on the cache to find what is essentially the same query – even if the user query phrasing is different. If a match is found in the semantic cache, return the response from the semantic cache rather than calling the LLM. A semantic cache hit has a faster response time and costs less compared to an LLM.

![canonical-ai-semantic-cache-demo--dentist-office-location-40s](https://github.com/Canonical-AI-Inc/canonical/assets/640297/91116289-d86e-4f96-8057-ea987525e39d)

In the first conversation, the user asks new questions, the LLM responds, and the cache gets populated. 

In the second conversation (after the terminal is cleared), the user asks the same questions, but with different phrasing. The responses are returned from the semantic cache and the time to first token is 10x faster.

## Doesn't My Vector DB Have A Semantic Cache?

We’ve talked to many developers who try semantic caching with a simple cosine similarity search (like the ones that come with vector databases), see the unsurprisingly poor accuracy from this context-agnostic approach, and kick the can on LLM caching’s cost and latency improvements.

An accurate and effective LLM cache needs to understand the context of the conversation with the user. It’s lifetimes of work. Lifetimes that AI developers should spend building their core user product rather than infrastructure.

## Canonical AI Context-Aware Semantic Caching

- **High Precision Semantic Caching.** For conversational AI (i.e., Voice AI agents), get cache hits only when it's [contextually appropriate](https://canonical.chat/blog/how_to_build_context_aware_semantic_cache). 
- **High Recall Semantic Caching.** For many AI applications, the Canonical AI Cache hit rate is above 20%. Even in open-ended conversations without much repetition, our cache gets hits in the beginning and end of a session. The first and final impressions are critical for user experience.
- **Fast Semantic Caching.** Response times are ~50 ms for on-prem deployments and ~120 ms for over-the-network. 
- **Secure Semantic Caching.** Personally Identifiable Information (PII) is never cached so user data is safe.
- **Tunable Cache Temperature.** You decide whether you want a cache hit to return the same response or differently phrased responses.
- **One Call For Caching and Knowledge Retrieval.** On cache misses, we retrieve knowledge (i.e., the R in RAG), which you augment and return to the user.

## Integration

You call the Canonical AI Cache before you call the LLM API. If there's a cache hit, we return the response from the cache. On a cache miss, we return a 404 and you then call the LLM. Send the LLM response to the user, then update the cache.

_API and Proxy_

Most users get started with the API. You can also integrate Canonical AI via proxy integration using the Open AI base URL. See [here](https://github.com/Canonical-AI-Inc/canonical/tree/main/examples) for a more detailed guide to getting started.

_On-Prem_

To take full advantage of caching's latency improvements, you can self-host the Canonical AI Cache. We built it with the goal of minimizing the configuration burden. [Reach out](mailto:hello@canonical.chat) to tell us more about your architecture and application.

## Pricing

_Free Tier_

If you have less than 10k of input and output tokens on your cache hits per month, Canonical AI Cache is free. 

_Paid Tier_

The paid tier is for developers with 10k of input and output tokens on cache hits per month. We charge only for cache hits. On cache hits, we charge 50% of the per token price of your LLM model.

## Don't Delay On Dropping Latency

Whether you’re a startup or an established player, you’re in a race with everyone else to capture the spoils of Generative AI. Deploy the Canonical AI Cache and get there faster.

Visit [our website](https://canonical.chat/) to get an API key for a free two-week trial! 

Or [email us](mailto:hello@canonical.chat) to set up a time to learn more about conversational AI caching. We'd love to hear from you!
