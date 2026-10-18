# Groq

- `custom.groq` connects Muse to the Groq API. It authenticates with the registered `api_key` credential, sent as a bearer header, and calls only `api.groq.com`.

- Helpers live in `~/workspace/custom-connectors/custom.groq/bin/`. `models.py` lists the models available to the key.

## Connect

- The connection was registered with `credentials.request_api_access` and these details. Reuse them unchanged to reconnect:

```json
{
  "provider": "groq",
  "auth_scheme": "api_key",
  "placement": "bearer_header",
  "api_hosts": ["api.groq.com"]
}
```

- Before the first change in a conversation, prove access with a harmless read:

```text
python3 ~/workspace/custom-connectors/custom.groq/bin/models.py
```

## Credentials

- The registered connection holds the credential. Helpers import `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`, which returns an `hsurr:` surrogate and places it where the provider reads the key. Muse swaps in the real credential only on an approved request to a registered host.

- Never put a key, token, password or cookie in this doc, a helper, a command argument, an environment variable or a log. Never ask the user to paste one in chat.

- Keep redirects disabled on authenticated requests.

- On a 401 or 403, check the request first. Confirm that the helper attached the surrogate and the host is registered.

- Only when a request that carried the credential is still rejected, call `credentials.request_api_access` with the details above and `"reconnect": true`.

## List models

- Calls `GET https://api.groq.com/openai/v1/models`. This is a read. It returns the models available to the key. Untested as of 2026-10-17: the call is blocked by Cloudflare (error 1010) at the network edge before authentication, so the key itself is unverified. This is an egress-fingerprint block, not a key verdict.

```text
python3 ~/workspace/custom-connectors/custom.groq/bin/models.py
```

- Output is a JSON object with `model_count` and the first 10 model ids, once the edge block is cleared.

## Recover from errors

- 401 means the request arrived without a usable key. First confirm the helper attached the surrogate and the host is registered.

- 429 means rate limited. Groq publishes `x-ratelimit-*` and `retry-after` headers. Back off per `retry-after`, or fall back to running the analysis in the agent context on the Muse plan.

- Cloudflare 1010 means the egress fingerprint was blocked before the request reached Groq. Retry later. Do not treat the key as bad.

- After a failed or timed-out change, check the current state with a read before trying again, because the first request may have completed.

## Limits

- This connector cannot manage keys or billing. It cannot raise rate limits.

- Chat completions (`POST https://api.groq.com/openai/v1/chat/completions`) are untested through this connector.

## Related skills

- Use `muse.skill_search` to find other skills and `muse.connector_search` to find other connectors.
