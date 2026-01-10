import os
import json
import re

def parse_problem_from_files(problem_id, base_path, data_split="test"):

    try:
        problem_path = os.path.join(base_path, data_split, str(problem_id))
        question_file = os.path.join(problem_path, "question.txt")
        test_file = os.path.join(problem_path, "input_output.json")

        if not os.path.exists(question_file) or not os.path.exists(test_file):
            return None, None

        with open(question_file, "r", encoding="utf-8") as f:
            question = f.read()

        with open(test_file, "r", encoding="utf-8") as f:
            test_cases = json.load(f)

        return question, test_cases
    except Exception as e:
        print(f"Error reading problem {problem_id}: {e}")
        return None, None

def load_example_for_prompting(problem_id, base_path, data_split="train"):

    path = os.path.join(base_path, data_split, str(problem_id))
    qfile = os.path.join(path, "question.txt")
    sfile = os.path.join(path, "solutions.json")
    try:
        with open(qfile, "r", encoding="utf-8") as f:
            question = f.read()
        with open(sfile, "r", encoding="utf-8") as f:
            sols = json.load(f)
        if sols:
            return question, sols[0]
    except Exception as e:
        print(f"Error loading example {problem_id}: {e}")
    return None, None

def extract_reasoning(text: str) -> str:

    m = re.search(r"```.*?```", text, re.DOTALL)
    if m:
        return text[:m.start()].strip()
    return text.strip()