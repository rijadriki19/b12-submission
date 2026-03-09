import os
import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

URL = "https://b12.io/apply/submission"
SIGNING_SECRET = b"hello-there-from-b12"

run_id = os.environ.get("GITHUB_RUN_ID")
if not run_id:
    raise RuntimeError("GITHUB_RUN_ID environment variable not found")

# Build the payload
payload = {
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    "name": "Rijad Foco",
    "email": "rijad.foco@hotmail.com",
    "resume_link": "https://github.com/rijadriki19/b12-submission",
    "repository_link": "https://github.com/rijadriki19/b12-submission",
    "action_run_link": f"https://github.com/rijadriki19/b12-submission/actions/runs/{run_id}"
}

body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

# HMAC-SHA256 signature
digest = hmac.new(SIGNING_SECRET, body, hashlib.sha256).hexdigest()
signature = f"sha256={digest}"

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": signature
}

response = requests.post(URL, data=body, headers=headers)

print("Status:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    receipt = response.json().get("receipt")
    print("Submission receipt:", receipt)