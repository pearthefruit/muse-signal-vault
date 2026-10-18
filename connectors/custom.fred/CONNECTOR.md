# Fred

- `custom.fred` connects Muse to the FRED API (Federal Reserve Economic Data, St. Louis Fed). It authenticates with the registered `api_key` credential, sent as an `Authorization: Bearer` header per the v2 API docs, and calls only `api.stlouisfed.org`.

- Helpers live in `~/workspace/custom-connectors/custom.fred/bin/`. `observations.py` fetches release observations.

## Connect

- The connection was registered with `credentials.request_api_access` and these details. Reuse them unchanged to reconnect:

```json
{
  "provider": "fred",
  "auth_scheme": "api_key",
  "placement": "bearer_header",
  "api_hosts": ["api.stlouisfed.org"]
}
```

- Before the first change in a conversation, prove access with a harmless read:

```text
python3 ~/workspace/custom-connectors/custom.fred/bin/observations.py
```

## Credentials

- The registered connection holds the credential. Helpers import `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`, which returns an `hsurr:` surrogate and places it where the provider reads the key. Muse swaps in the real credential only on an approved request to a registered host.

- Never put a key, token, password or cookie in this doc, a helper, a command argument, an environment variable or a log. Never ask the user to paste one in chat.

- Keep redirects disabled on authenticated requests.

- On a 401 or 403, check the request first. Confirm that the helper attached the credential, that the host is registered and that the placement matches.

- Only when a request that carried the credential is still rejected, call `credentials.request_api_access` with the details above and `"reconnect": true`.

## Release observations

- Calls `GET https://api.stlouisfed.org/fred/v2/release/observations`. This is a read. The only required parameter is `release_id` (integer); `format` defaults to json, `limit` defaults to 500000, `next_cursor` pages. Verified live 2026-10-17: release 52 (Z.1 Financial Accounts of the United States) returned series data, key works.

```text
python3 ~/workspace/custom-connectors/custom.fred/bin/observations.py
```

- Output is a JSON object with the release name, first series id and title, and whether more pages exist. The v2 response nests data under `release` and `series`, not `observations`.

## Recover from errors

- 400 means the endpoint path or parameters were wrong. The v2 API is release-oriented; the old v1 per-series paths are stale.

- 401 or 403 means the key was rejected. Check the helper, host registration and placement before reconnecting.

- After a failed or timed-out change, check the current state with a read before trying again, because the first request may have completed.

## Limits

- This connector cannot manage keys or quotas.

- Only the release-observations endpoint is documented here. Other v2 endpoints are untested.

## Related skills

- Use `muse.skill_search` to find other skills and `muse.connector_search` to find other connectors.
