# Canonical AI
Context-Aware LLM Latency and Cost Optimization Engine for Conversational AI

## Problem
The old Natural Language Processing approaches to voice AI fell short of user expectations. With the arrival of LLMs, voice and multimodal AI will eat the world. 

But first, we have to address latency. In voice conversation, users expect a 300 millisecond or less response from the AI. In applications with a sufficiently well-written system prompt, the context window bogs the latency down to seconds – and that’s before conversation turns add to the context window.

## Solution
Canonical AI is an optimization engine for conversational AI. A ultra-low latency semantic cache is the core of our technology. In order for the semantic cache to work in a conversation, we make the cache aware of the conversational context.

Here is a basic description of a simple semantic cache. For each new user query, the code first semantically searches the cache for what is essentially the same query – even if the query phrasing is different. If a match is found in the cache, the code returns the answer from the cache rather than calling the LLM. Cache hits return responses faster and cost less compared to calling a foundational LLM API. 

For conversational AI, the cache needs to know about the context of the user query. For example, a user may ask a question about something in the beginning of a conversation, then ask the very same question about a different matter later in the conversation. Without awareness of the context, a semantic cache will cache the first response and use it to incorrectly answer the user’s second question. 

To address the contextual requirements of conversation AI caching, a newly-deployed Canonical Cache observes before acting. In observation mode, the Canonical Cache detects the parts of the conversation that can be cached and the parts that should not be cached. With each new detection of a cache opportunity, the key-value pairs are added to the cache. Other technologies, such as cache seeding, also build context for the Canonical Cache. 

## Features

 - **Fast Semantic Caching.** Cache hits return responses faster than an LLM. Cache misses add to the latency of calling an LLM. We minimize the latency penalty of cache misses with our sub-100 ms response time. 
 - **Accurate Semantic Caching.** The high precision Canonical Cache returns hits that answer the query correctly. The high recall of the cache means you don’t miss out on hits – and opportunities for latency and cost reduction. 
 - **Caching for Conversational AI**. The Canonical Cache is context-aware. It learns the conversation and identifies the appropriate opportunities for caching before acting. 
 - **Multitenancy**. Each product, each AI persona, or each user can have its own cache. You decide the scope of the cache.  
 - **Cache Seeding**. Rephrasings of each query get stored in the Canonical Cache to increase the likelihood of cache hits. 
 - **Tunable Variation on Cache Hits**. You decide whether you want a cache hit to return the same response or differently phrased responses. 
 - **Speedy Input Validation**. Sometimes a conversation can’t proceed without making sure a user input is correct. Canonical uses the appropriate model for each validation task.
 - **Simple Integration**. Deploy the Canonical Cache to your data pipeline via an API call one step upstream of your LLM call. If there’s a cache miss, then send the LLM completion to the Canonical Cache after you’ve responded to the user.
   
## Metrics

The Canonical Cache is benchmarked against other solutions using the [Quora Duplicate Questions](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs) dataset. Each pair of questions in the dataset may or may not be semantically the same. The dataset scores each pair as duplicated questions or dissimilar questions. Of the 2,000 pairs in the test dataset used for this analysis, there are 1,000 duplicate pairs and 1,000 dissimilar pairs. 

| Cache                    | Precision | Recall |
|--------------------------|-----------|--------|
| Cosine Similarity Search | 0.57      | 0.77   |
| GPTCache                 | 0.57      | 0.68   |
| Canonical Cache          | 0.84      | 0.85   |

A simple semantic cache using cosine similarity vector search has low precision. It returns so many false positives that the cache hits are untrustworthy. 

The GPTCache configuration with the albert-duplicate-onnx model evaluator performs overall worse than the simple cosine similarity search. Note, the GPTCache configuration with a model evaluator trained on the Quora Duplicate Questions dataset has a precision and recall of 0.59 and 0.78, respectively. 

The Canonical Cache has a precision of 0.84 and recall of 0.85. In other words, 84% of cache hits are actually duplicate questions, and the Canonical Cache finds 85% of the duplicated questions. The mean response time is about 300 milliseconds.

## Build Versus Buy

It turns out it is difficult to build a semantic cache for conversation AI. There are two main reasons.

First, as you can see in the Metrics section above, the simple semantic cache and the open source solution return a high rate of false positives. False positives are bad because you answer the user’s question with the incorrect response. Users would stop trusting your AI. 

Second, simple semantic caching works okay for question and answer applications, like you might have in a Retrieval Augmented Generation app. For conversational AI, the semantic cache needs to know about the context. A semantic cache for conversational AI is not something you can ship in a week. 

Remember the ‘90s? Servers were neat and novel! Engineers loved setting up servers! Nobody does that anymore. A startup races against time to find product-market fit before it dies. It’s fun to build LLM infrastructure because Generative AI is interesting and novel, but it’s not the best use of a startup’s limited engineering resources and precious time.

## Integration

*API and Proxy*

You connect with the Canonical Cache via an API call. You call the Canonical Cache before you call the LLM API. If the Canonical Cache finds a hit, it returns the cached response. If there is no cache hit, then Canonical returns a 404 and you then call the LLM. You can also integrate Canonical via proxy integration using the Open AI base URL. More details about the integration can be found on our demo page \(see below\). 

*On-Prem*

Coming soon!

## Try it out

You can try out the semantic cache on [our demo](https://pg-demo.streamlit.app/).

## Pricing

For the semantic cache, we charge only for cache hits. Whatever model you're using, we charge 50% of the per token price on cache hits.

## Get In Touch!

We’d love to hear from you! Email us at hello@canonical.chat.
