#!/usr/bin/env python3
"""Verify the stored Groq credential with a harmless authenticated read.

Calls GET https://api.groq.com/openai/v1/models, which requires a valid key
and lists the models available to it. No secret ever appears in this file, in
arguments, or in output: authd swaps a surrogate for the real credential
only on an approved request to a registered host.
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
    request = urllib.request.Request("https://api.groq.com/openai/v1/models")
    add_surrogate_to_request(request, "custom.groq", allowed_hosts=["api.groq.com"])
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
            data = read_json_response(response)
    except urllib.error.HTTPError as exc:
        print(json.dumps({"http_error": exc.code, "body": exc.read().decode("utf-8", "replace")[:500]}))
        return 1
    models = data.get("data", []) if isinstance(data, dict) else []
    print(json.dumps({"model_count": len(models),
                      "models": [m.get("id") for m in models][:10]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
