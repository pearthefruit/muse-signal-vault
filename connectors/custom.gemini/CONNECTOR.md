# Gemini

- `custom.gemini` connects Muse to the Google Gemini API. It authenticates with the registered `api_key` credential, sent as the `X-Goog-Api-Key` header, and calls only `generativelanguage.googleapis.com`.

- Helpers live in `~/workspace/custom-connectors/custom.gemini/bin/`. `models.py` lists the models available to the key.

## Connect

- The connection was registered with `credentials.request_api_access` and these details. Reuse them unchanged to reconnect:

```json
{
  "provider": "gemini",
  "auth_scheme": "api_key",
  "placement": "custom_header:X-Goog-Api-Key",
  "api_hosts": ["generativelanguage.googleapis.com"]
}
```

- Before the first change in a conversation, prove access with a harmless read:

```text
python3 ~/workspace/custom-connectors/custom.gemini/bin/models.py
```

## Credentials

- The registered connection holds the credential. Helpers import `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`, which returns an `hsurr:` surrogate and places it where the provider reads the key. Muse swaps in the real credential only on an approved request to a registered host.

- Never put a key, token, password or cookie in this doc, a helper, a command argument, an environment variable or a log. Never ask the user to paste one in chat.

- Keep redirects disabled on authenticated requests.

- On a 401 or 403, check the request first. Confirm that the helper attached the credential, that the host is registered and that the placement matches.

- Only when a request that carried the credential is still rejected, call `credentials.request_api_access` with the details above and `"reconnect": true`.

- The vault holds one value per connector. Per-key rotation across several Gemini keys needs one connector per key; a comma-separated value is delivered to Google as a single key.

## List models

- Calls `GET https://generativelanguage.googleapis.com/v1/models`. This is a read. It returns the models available to the key. Verified live 2026-10-17: 24 models returned, key works.

```text
python3 ~/workspace/custom-connectors/custom.gemini/bin/models.py
```

- Output is a JSON object with `model_count` and the first 10 model names.

## Recover from errors

- 400 with an API key error means the key value was rejected. Check the stored value.

- 429 means rate limited. Back off, or fall back to running the analysis in the agent context on the Muse plan.

- After a failed or timed-out change, check the current state with a read before trying again, because the first request may have completed.

## Limits

- This connector cannot manage keys or billing. It cannot raise rate limits.

- Generate-content calls are untested through this connector.

## Related skills

- Use `muse.skill_search` to find other skills and `muse.connector_search` to find other connectors.
