#!/usr/bin/env python3
"""Verify the stored USPTO credential with a harmless read.

POSTs a minimal search to the USPTO Open Data Portal patent-applications
endpoint asking for a single record. The key travels as the X-API-Key header.
No secret ever appears in this file, in arguments, or in output: authd swaps
a surrogate for the real credential only on an approved request to a
registered host.
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
    body = json.dumps({
        "q": "applicationMetaData.firstApplicantName:International Business Machines",
        "sort": [{"field": "applicationMetaData.filingDate", "order": "desc"}],
        "pagination": {"offset": 0, "limit": 1},
    }).encode("utf-8")
    request = urllib.request.Request(
        "https://api.uspto.gov/api/v1/patent/applications/search",
        data=body,
        method="POST",
    )
    request.add_header("Content-Type", "application/json")
    add_surrogate_to_request(request, "custom.uspto", allowed_hosts=["api.uspto.gov"])
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
            data = read_json_response(response)
    except urllib.error.HTTPError as exc:
        print(json.dumps({"http_error": exc.code, "body": exc.read().decode("utf-8", "replace")[:500]}))
        return 1
    print(json.dumps({"count": data.get("count"),
                      "returned": len(data.get("patentFileWrapperDataBag", []))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
