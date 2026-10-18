#!/usr/bin/env python3
"""Verify the stored FRED credential with a harmless read.

Fetches the latest observation of the GDP series from the FRED API. The key
travels as an Authorization: Bearer header per the v2 API docs. No secret
ever appears in this file, in arguments, or in output: authd swaps a surrogate
for the real credential only on an approved request to a registered host.
"""
import json
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def main() -> int:
    params = urllib.parse.urlencode({
        "release_id": 52,
        "format": "json",
        "limit": 1,
    })
    request = urllib.request.Request(
        "https://api.stlouisfed.org/fred/v2/release/observations?" + params
    )
    add_surrogate_to_request(request, "custom.fred", allowed_hosts=["api.stlouisfed.org"])
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
            data = read_json_response(response)
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8", "replace")[:500]
        except Exception:
            body = "<unreadable>"
        print(json.dumps({"http_error": exc.code, "body": body}))
        return 1
    obs = data.get("series", [])
    release = data.get("release", {})
    first = obs[0] if obs else {}
    print(json.dumps({
        "release": release.get("name"),
        "first_series_id": first.get("series_id"),
        "first_series_title": first.get("title"),
        "has_more": data.get("has_more"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
