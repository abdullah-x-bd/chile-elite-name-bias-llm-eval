# Budget

Approved grant amount is 100 USD.

The budget is mainly for API calls and scoring. Hosting will use free static hosting.

| Use | Amount | Notes |
| --- | ---: | --- |
| OpenAI model calls | 35 USD | Main frontier and lower cost model runs |
| Anthropic model calls | 25 USD | Sonnet class and lower cost model runs |
| Google model calls | 15 USD | Gemini model runs |
| LLM assisted scoring and checks | 10 USD | Parsing difficult outputs and checking classification quality |
| Reruns, debugging, failed calls | 10 USD | Pilot failures, invalid JSON, repeated runs |
| Final result checks | 5 USD | Small reserve for final validation runs |

## Cost control rules

- Keep model output short
- Prefer JSON output
- Use cheaper models for pilot tests
- Run expensive models only after prompts are stable
- Save every request and response for reproducibility
- Track spend by provider
- Stop full scale runs if early cost is higher than planned

## Hosting

The public results page will use GitHub Pages or another free static host.

Planned hosting cost is 0 USD.

## Spending log

| Date | Provider | Purpose | Amount | Notes |
| --- | --- | --- | ---: | --- |
| Pending | Pending | Pending | 0 USD | No spend recorded yet |