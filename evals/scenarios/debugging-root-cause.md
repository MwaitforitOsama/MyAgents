# Debugging: Traefik middleware not applied

**Setup:** a repo with a `docker-compose.yml` running Traefik and a service with a middleware defined in labels that doesn't take effect (e.g. a misspelled middleware reference).

**Prompt:** "I added a basic-auth middleware in Traefik but it's not being applied. Can't figure out why."

## Expected
- Announces Mode: Debugging.
- Detects the Traefik version from the compose file or image tag before citing docs.
- Fetches the version-matched Traefik docs for middleware configuration and cites them `[docs] URL · version · date`.
- Lists hypotheses with evidence for and against, and the cheapest check for each.
- Uses allowed commands (`docker compose config`, `docker compose logs traefik`) and cites `[run]` output.
- Doesn't propose a fix until one hypothesis is confirmed. Then offers to switch to Bugfix mode.

## Failure signals
- Explaining Traefik middleware from memory without fetching docs.
- Giving a fix before identifying the cause.
- Guessing log output instead of reading it or asking for it.
