# Frozen model panel

The Phase II primary panel contains eight model endpoints chosen for cross-lab and deployment diversity while remaining feasible under the fixed 7.25 USD OpenRouter balance.

| Family | OpenRouter request ID | Canonical slug at freeze | Pinned provider |
| --- | --- | --- | --- |
| OpenAI | `openai/gpt-5.4-mini` | `openai/gpt-5.4-mini-20260317` | `openai` |
| OpenAI small | `openai/gpt-5.4-nano` | `openai/gpt-5.4-nano-20260317` | `openai` |
| Anthropic | `anthropic/claude-sonnet-5` | `anthropic/claude-sonnet-5-20260630` | `anthropic` |
| Google | `google/gemini-3.6-flash` | `google/gemini-3.6-flash-20260721` | `google-ai-studio` |
| DeepSeek | `deepseek/deepseek-v4-flash-0731` | `deepseek/deepseek-v4-flash-20260731` | `deepseek` |
| Qwen | `qwen/qwen3.7-max` | `qwen/qwen3.7-max-20260520` | `alibaba` |
| Mistral | `mistralai/mistral-medium-3-5` | `mistralai/mistral-medium-3.5-20260430` | `mistral` |
| Meta | `meta-llama/llama-4-maverick` | `meta-llama/llama-4-maverick-17b-128e-instruct` | `deepinfra` |

The public OpenRouter model catalogue was checked on 2026-08-10 before this freeze. The runner also contains a verification step that compares the live catalogue against these frozen identities before execution. A mismatch causes failure, not auto-updating.

Provider fallbacks are disabled. The provider pin is part of the scientific identity of each model endpoint.

## Inference normalization

Reasoning is minimized rather than assumed identical across architectures. GPT-5.4 mini/nano and Llama 4 Maverick receive no reasoning parameter; Claude Sonnet 5 receives low reasoning; Gemini 3.6 Flash receives mandatory-minimal reasoning; DeepSeek V4 Flash receives low reasoning; Qwen3.7 Max has reasoning explicitly disabled; and Mistral Medium 3.5 uses its `none` reasoning effort. Reasoning text is excluded and never stored. Unsupported temperature parameters are omitted rather than retried.

The cost snapshot uses the pinned provider's list price where provider-specific routing changes the public aggregate price, including DeepSeek's native provider and DeepInfra for Llama 4 Maverick. Actual run cost is taken from OpenRouter usage accounting and enforced by the hard budget guard.
