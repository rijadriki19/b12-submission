import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

URL = "https://b12.io/apply/submission"
SIGNING_SECRET = b"hello-there-from-b12"

payload = {
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    "name": "Rijad Foco",
    "email": "rijad.foco@hotmail.com",
    "resume_link": "Na",
    "repository_link": "https://github.com/yourusername/yourrepo",
    "action_run_link": "https://github.com/yourusername/yourrepo/actions/runs/${{ github.run_id }}"
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
