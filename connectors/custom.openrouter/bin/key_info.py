#!/usr/bin/env python3
"""Verify the stored OpenRouter credential with a harmless authenticated read.

Calls GET https://openrouter.ai/api/v1/auth/key, which requires a valid key
and returns the key's label, usage and rate limit. No secret ever appears in
this file, in arguments, or in output: authd swaps a surrogate for the real
credential only on an approved request to a registered host.
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
    request = urllib.request.Request("https://openrouter.ai/api/v1/auth/key")
    add_surrogate_to_request(request, "custom.openrouter", allowed_hosts=["openrouter.ai"])
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
            print(json.dumps(read_json_response(response), indent=2))
    except urllib.error.HTTPError as exc:
        print(json.dumps({"http_error": exc.code, "body": exc.read().decode("utf-8", "replace")[:500]}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
