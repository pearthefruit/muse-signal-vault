# Openrouter

- `custom.openrouter` connects Muse to the OpenRouter API. It authenticates with the registered `api_key` credential, sent as a bearer header, and calls only `openrouter.ai`.

- Helpers live in `~/workspace/custom-connectors/custom.openrouter/bin/`. `key_info.py` performs a harmless authenticated read of key metadata.

## Connect

- The connection was registered with `credentials.request_api_access` and these details. Reuse them unchanged to reconnect:

```json
{
  "provider": "openrouter",
  "auth_scheme": "api_key",
  "placement": "bearer_header",
  "api_hosts": ["openrouter.ai"]
}
```

- Before the first change in a conversation, prove access with a harmless read:

```text
python3 ~/workspace/custom-connectors/custom.openrouter/bin/key_info.py
```

## Credentials

- The registered connection holds the credential. Helpers import `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`, which returns an `hsurr:` surrogate and places it where the provider reads the key. Muse swaps in the real credential only on an approved request to a registered host.

- Never put a key, token, password or cookie in this doc, a helper, a command argument, an environment variable or a log. Never ask the user to paste one in chat.

- Keep redirects disabled on authenticated requests.

- On a 401 or 403, check the request first. Confirm that the helper attached the credential, that the host is registered and that the placement and scopes match.

- Only when a request that carried the credential is still rejected, call `credentials.request_api_access` with the details above and `"reconnect": true`.

## Check key metadata

- Calls `GET https://openrouter.ai/api/v1/auth/key`. This is a read. It returns the key label, usage and limit. Use it to prove the credential works and to see remaining free-tier headroom before a large run.

```text
python3 ~/workspace/custom-connectors/custom.openrouter/bin/key_info.py
```

- Output is the JSON body of the key-info response. Untested as of 2026-10-17: the surrogate egress swap did not fire from the agent exec environment, so live verification is still pending. The failure is in the swap, not proven to be the key.

## Recover from errors

- 401 means the request arrived without a usable key. First confirm the helper attached the surrogate and the host is registered. The 401 message "Missing Authentication header" with a surrogate-shaped bearer means the egress swap did not happen.

- 429 means rate limited. Back off and retry, or fall back to running the analysis in the agent context on the Muse plan.

- After a failed or timed-out change, check the current state with a read before trying again, because the first request may have completed.

## Limits

- This connector cannot spend or top up credits. It cannot list the user's other keys.

- Chat completions (`POST /api/v1/chat/completions`) are untested through this connector.

## Related skills

- Use `muse.skill_search` to find other skills and `muse.connector_search` to find other connectors.
