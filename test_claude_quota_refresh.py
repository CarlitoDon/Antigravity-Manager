import json, urllib.request, ssl, uuid

ctx = ssl._create_unverified_context()
account_file = "/Users/wecik/.antigravity_tools/accounts/1046988a-37ff-4de0-bb73-f33f5cf6e027.json"
data = json.load(open(account_file))

# Refresh token
payload_refresh = {
    "client_id": "872401655596-tvnsno5h67v0a7u0257u9k3336u0r6r9.apps.googleusercontent.com",
    "client_secret": "",
    "refresh_token": data['token']['refresh_token'],
    "grant_type": "refresh_token"
}
req_ref = urllib.request.Request("https://oauth2.googleapis.com/token", data=json.dumps(payload_refresh).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req_ref, context=ctx) as res:
    ref_res = json.loads(res.read().decode())
    access_token = ref_res["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "User-Agent": "Antigravity/4.2.4"
}
payload = {
    "project": data['token']['project_id'],
    "model": "claude-sonnet-4-6",
    "request": {
        "messages": [{"role": "user", "content": "hello"}],
        "stream": False
    },
    "requestId": f"agent-{uuid.uuid4()}",
    "requestType": "agent",
    "userAgent": "antigravity"
}

req = urllib.request.Request(
    "https://cloudcode-pa.googleapis.com/v1internal:generateContent", 
    data=json.dumps(payload).encode("utf-8"),
    headers=headers, 
    method="POST"
)
try:
    with urllib.request.urlopen(req, context=ctx) as res:
        print("Status:", res.status)
        print("Response:", res.read().decode("utf-8")[:200])
except urllib.error.HTTPError as e:
    print("Status:", e.code)
    print("Response:", e.read().decode("utf-8")[:200])

