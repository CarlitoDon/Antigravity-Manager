import os
import json
import glob

accounts_dir = os.path.expanduser("~/.antigravity_tools/accounts")
pattern = os.path.join(accounts_dir, "*.json")

print(f"Scanning for JSON files in: {accounts_dir}")
files = glob.glob(pattern)

count = 0
for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Clear live_limited_models if present
        if "live_limited_models" in data:
            if data["live_limited_models"]:
                print(f"Clearing live_limited_models for {data.get('email', os.path.basename(filepath))} (was: {list(data['live_limited_models'].keys())})")
                data["live_limited_models"] = {}
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                count += 1
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f"Cleared live limit locks in {count} accounts.")
