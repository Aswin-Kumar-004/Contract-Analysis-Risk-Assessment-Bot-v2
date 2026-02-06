import json
from datetime import datetime

AUDIT_FILE = "data/audit_logs.json"

def log_event(event):
    try:
        with open(AUDIT_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({
        "timestamp": datetime.utcnow().isoformat(),
        "event": event
    })

    with open(AUDIT_FILE, "w") as f:
        json.dump(data, f, indent=2)
