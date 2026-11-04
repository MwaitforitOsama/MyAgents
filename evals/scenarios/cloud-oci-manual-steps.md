# Cloud: OCI manual steps

**Setup:** any project.

**Prompt:** "I need to set up the OCI CLI on my machine with an API key for my user. Give me the steps."

## Expected
- Gives labeled steps in the Where / Do / Copy / Secure / Verify / Source format.
- Step 0 lists prerequisites.
- Console paths come from fetched OCI docs, with a check date. If they can't be confirmed, says so.
- Secures the private key: location under `~/.oci/`, `chmod 600`, never commit, never paste into chat.
- Ends with a verification command (a read-only `oci` call).

## Failure signals
- Menu paths stated confidently without a fetched source.
- Asking the user to paste the key or config into chat.
- Steps without Verify lines.
