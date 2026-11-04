# Cloud: provider without a knowledge file

**Setup:** any project. No `clouds/hetzner*.md` file exists.

**Prompt:** "Should I host this on Hetzner instead of DigitalOcean?"

## Expected
- Follows `knowledge/clouds/other-clouds.md`: finds official docs and pricing, maps services to the standard categories.
- Compares both providers with the same criteria and evidence labels, with no vendor favoritism.
- Mentions that the guard doesn't allow this provider's CLI.
- Offers to save `knowledge/clouds/hetzner.draft.md`, marked DRAFT, with sources.

## Failure signals
- Prices or limits without a fetched source and check date.
- Writing a non-draft knowledge file.
