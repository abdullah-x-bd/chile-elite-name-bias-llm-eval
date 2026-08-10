# Protocol Amendment 1, pre-outcome

Date: 2026-08-10

Status: frozen before any Phase II scientific response was collected.

The original Phase II protocol and fingerprint remain preserved. Exact-routing technical smoke tests identified two provider-compatibility problems before the primary confirmatory matrix began. No scientific prompt was executed.

## A1. Anthropic structured-output schema serialization

The Anthropic endpoint for `anthropic/claude-sonnet-5` returned HTTP 400 because its structured-output dialect does not accept JSON Schema `minimum` and `maximum` keywords on integer fields. The scientific response variables remain exactly the same integers and categories defined in the frozen protocol.

For Anthropic only, the provider-facing JSON Schema recursively omits `minimum` and `maximum`. The frozen post-response semantic validator still enforces every original bound, including score/confidence in [0,100] and association probabilities in [0,100] with the original sum constraints. A response outside those ranges therefore remains semantically invalid exactly as originally specified.

This is a serialization compatibility amendment, not a change to the measured construct or permissible analyzed values.

## A2. DeepSeek endpoint replacement

The frozen `deepseek/deepseek-v4-flash-0731` slug was present in the catalogue during preflight but returned HTTP 404 at inference time with `No endpoints found` before any scientific call.

It is replaced by:

- request model: `deepseek/deepseek-v3.2`
- canonical model: `deepseek/deepseek-v3.2-20251201`
- provider: `deepinfra`
- provider endpoint observed at amendment time: `deepinfra/fp4`

DeepSeek V3.2 supports structured outputs, response format, reasoning, temperature, and seed on OpenRouter. The DeepInfra endpoint was live at amendment time. All other seven frozen model/provider cells remain unchanged.

## A3. Label and analysis

The replacement cell is labeled `deepseek_v32`. The analysis plan, prompt manifest, hypotheses, primary estimands, surname groups, profiles, language, and multiple-testing policy are unchanged.

## A4. Outcome blindness

Only non-study smoke prompts were used before this amendment. No Phase II prompt from the 1,032-cell scientific manifest was sent to any model before Amendment 1 was frozen.
