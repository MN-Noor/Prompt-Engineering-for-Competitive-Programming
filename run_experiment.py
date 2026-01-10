import os
import random
import time
from src.api_client import generate_response
from src.parsers import parse_problem_from_files, extract_reasoning
from src.evaluator import extract_python_code, run_test_cases
from src.prompts import create_zero_shot_prompt
from src.utils import log_experiment_entry, get_timestamped_filename

# Paths
BASE_DIR = "/mnt/batch/tasks/shared/LS_root/mounts/clusters/noora1/code/Users/noora"
DATA_PATH = os.path.join(BASE_DIR, "APPS_extracted/APPS")
LOG_PATH = os.path.join(BASE_DIR, "experiment_results_with_reasoning.jsonl")

def run_experiment(problem_id, strategy="zero_shot"):
    # Load Data
    q, tests = parse_problem_from_files(problem_id, DATA_PATH)
    if not q: return None

    # Prompt Selection
    prompt = create_zero_shot_prompt(q)

    # Model Inference
    raw_response = generate_response(prompt, api_key="YOUR_KEY")
    if not raw_response: return None

    # Extraction
    code = extract_python_code(raw_response)
    reasoning = extract_reasoning(raw_response)

    # Testing
    result, details = run_test_cases(code, tests)

    # Logging
    entry = {
        "problem_id": problem_id,
        "strategy": strategy,
        "result": result,
        "details": details,
        "reasoning": reasoning,
        "generated_code": code
    }
    log_experiment_entry(LOG_PATH, entry)
    return entry

if __name__ == "__main__":
    pids = [f"{i:04d}" for i in range(10)]
    for pid in pids:
        print(f"Running Problem {pid}...")
        run_experiment(pid)
        time.sleep(2 + random.random())