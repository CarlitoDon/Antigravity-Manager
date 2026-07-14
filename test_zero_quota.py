import json, requests, time

account_file = "/Users/wecik/.antigravity_tools/accounts/1046988a-37ff-4de0-bb73-f33f5cf6e027.json"
data = json.load(open(account_file))

headers = {
    "Authorization": f"Bearer {data['access_token']}",
    "Content-Type": "application/json"
}
payload = {
    "model": "claude-opus-4-6-thinking",
    "messages": [{"role": "user", "content": "hello"}],
    "stream": False
}

print(f"Testing account {data['email']} with 0% Claude quota...")
res = requests.post("https://daily-cloudcode-pa.sandbox.googleapis.com/v1/chat/completions", headers=headers, json=payload)
print("Status:", res.status_code)
print("Response:", res.text[:200])

