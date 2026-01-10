import os
import json
from datetime import datetime

def log_experiment_entry(log_path, entry):
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Failed to write log: {e}")

def get_timestamped_filename(prefix, extension):
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.{extension}"