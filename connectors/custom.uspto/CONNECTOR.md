# Uspto

- `custom.uspto` connects Muse to the USPTO Open Data Portal API. It authenticates with the registered `api_key` credential, sent as the `X-API-Key` header, and calls only `api.uspto.gov`.

- Helpers live in `~/workspace/custom-connectors/custom.uspto/bin/`. `search.py` runs a minimal patent-application search.

## Connect

- The connection was registered with `credentials.request_api_access` and these details. Reuse them unchanged to reconnect:

```json
{
  "provider": "uspto",
  "auth_scheme": "api_key",
  "placement": "custom_header:X-API-Key",
  "api_hosts": ["api.uspto.gov"]
}
```

- Before the first change in a conversation, prove access with a harmless read:

```text
python3 ~/workspace/custom-connectors/custom.uspto/bin/search.py
```

## Credentials

- The registered connection holds the credential. Helpers import `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`, which returns an `hsurr:` surrogate and places it where the provider reads the key. Muse swaps in the real credential only on an approved request to a registered host.

- Never put a key, token, password or cookie in this doc, a helper, a command argument, an environment variable or a log. Never ask the user to paste one in chat.

- Keep redirects disabled on authenticated requests.

- On a 401 or 403, check the request first. Confirm that the helper attached the credential, that the host is registered and that the placement matches.

- Only when a request that carried the credential is still rejected, call `credentials.request_api_access` with the details above and `"reconnect": true`.

## Search patent applications

- POSTs to `https://api.uspto.gov/api/v1/patent/applications/search`. This is a read. The body uses `q` (query string), `sort`, `pagination` (`offset`/`limit`) and `fields`. Verified live 2026-10-17: an IBM applicant search returned count 373,967 with 1 record, key works.

```text
python3 ~/workspace/custom-connectors/custom.uspto/bin/search.py
```

- Output is a JSON object with `count` (total matches) and `returned` (records in the page).

## Recover from errors

- 400 means the request body was malformed. This endpoint wants `q`, `sort`, `pagination` and `fields`, not `size`/`page`.

- 401 or 403 means the key was rejected. Check the helper, host registration and placement before reconnecting.

- After a failed or timed-out change, check the current state with a read before trying again, because the first request may have completed.

## Limits

- This connector cannot manage keys or quotas.

- Only the patent-applications search endpoint is documented here. Other ODP endpoints are untested.

## Related skills

- Use `muse.skill_search` to find other skills and `muse.connector_search` to find other connectors.
