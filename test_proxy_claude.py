import urllib.request
import json
import ssl
import uuid

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    "http://127.0.0.1:28795/v1internal:generateContent",
    data=json.dumps({
        "model": "claude-opus-4-6-thinking",
        "request": {
            "messages": [{"role": "user", "content": "Halo, tes Opus Thinking."}],
            "stream": False,
            "thinking_budget": 1024
        },
        "requestId": f"agent-{uuid.uuid4()}",
        "requestType": "agent",
        "userAgent": "antigravity"
    }).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Antigravity/4.2.4"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, context=ctx) as res:
        print("Status:", res.status)
        print("Response:", res.read().decode("utf-8")[:200])
except urllib.error.HTTPError as e:
    print("Status:", e.code)
    print("Response:", e.read().decode("utf-8")[:200])
except Exception as e:
    print("Error:", e)

