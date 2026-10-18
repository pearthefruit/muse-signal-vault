#!/usr/bin/env python3
"""Verify the stored Gemini credential with a harmless authenticated read.

Calls GET https://generativelanguage.googleapis.com/v1/models, which requires
a valid key and lists the models available to it. The key travels as the
x-goog-api-key header. No secret ever appears in this file, in arguments, or
in output: authd swaps a surrogate for the real credential only on an approved
request to a registered host.

NOTE: the vault holds a single value. If several keys were pasted
comma-separated, the swap delivers the whole string as one header value and
Google rejects it. Use one key per connector for a working setup.
"""
import json
import sys
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def main() -> int:
    request = urllib.request.Request("https://generativelanguage.googleapis.com/v1/models")
    add_surrogate_to_request(
        request, "custom.gemini", allowed_hosts=["generativelanguage.googleapis.com"]
    )
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
            data = read_json_response(response)
    except urllib.error.HTTPError as exc:
        print(json.dumps({"http_error": exc.code, "body": exc.read().decode("utf-8", "replace")[:500]}))
        return 1
    models = data.get("models", []) if isinstance(data, dict) else []
    print(json.dumps({"model_count": len(models),
                      "models": [m.get("name") for m in models][:10]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
