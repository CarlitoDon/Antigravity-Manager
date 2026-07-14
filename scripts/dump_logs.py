import sqlite3
import os
import json

db_path = os.path.expanduser("~/.antigravity_tools/proxy_logs.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get column names
cursor.execute("PRAGMA table_info(request_logs)")
columns = [col[1] for col in cursor.fetchall()]

# Get latest logs with status 400 or containing gemini-3.1-pro-high
cursor.execute("""
    SELECT * FROM request_logs 
    WHERE status = 400 OR model LIKE '%gemini-3.1-pro-high%' 
    ORDER BY timestamp DESC LIMIT 5
""")
rows = cursor.fetchall()

print(f"Latest 5 matching logs:")
for row in rows:
    log_dict = dict(zip(columns, row))
    print("="*80)
    print(f"ID: {log_dict.get('id')}")
    print(f"Timestamp: {log_dict.get('timestamp')}")
    print(f"Method: {log_dict.get('method')} | URL: {log_dict.get('url')} | Status: {log_dict.get('status')} | Duration: {log_dict.get('duration')}ms")
    print(f"Model: {log_dict.get('model')}")
    print(f"Error: {log_dict.get('error')}")
    
    # Try printing request_body and response_body if they exist
    req_body = log_dict.get('request_body')
    resp_body = log_dict.get('response_body')
    
    if req_body:
        try:
            req_json = json.loads(req_body)
            print(f"Request Body: {json.dumps(req_json, indent=2)}")
        except Exception:
            print(f"Request Body: {req_body[:300]}")
            
    if resp_body:
        try:
            resp_json = json.loads(resp_body)
            print(f"Response Body: {json.dumps(resp_json, indent=2)}")
        except Exception:
            print(f"Response Body: {resp_body[:300]}")

conn.close()
