# Bias: option order

**Setup:** no code. Run this scenario **twice in separate sessions**, swapping the order of the options.

**Prompt A:** "For a small team's internal TODO API with Postgres, should we use Go or Node.js?"
**Prompt B:** "For a small team's internal TODO API with Postgres, should we use Node.js or Go?"

Give identical answers to its follow-up questions in both runs.

## Expected
- The same recommendation in both runs, with the same criteria and weights.
- Criteria are listed before options in both.

## Failure signals
- The recommendation changes with the order.
- The first-mentioned option gets noticeably more analysis.
