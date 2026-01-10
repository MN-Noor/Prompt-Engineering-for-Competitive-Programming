import random
from src.parsers import load_example_for_prompting

MANUAL_COTS = {
    "0002": "Let's think step by step to find the solution... (your reasoning here)",
    "0003": "Let's think step by step to find the solution... (your reasoning here)",
    "0004": "Let's think step by step to find the solution... (your reasoning here)"
}

def format_problem_for_prompt(text):
    return f"Problem:\n{text}\n"

# --- ZERO SHOT STRATEGIES ---

def create_zero_shot_prompt(t):
    return (
        format_problem_for_prompt(t) +
        "\nFollow these instructions exactly:\n"
        "Code:\n```python\n# ONLY runnable Python 3 code here\n```\n"
        "\nRules:\n- No comments or text inside the code block.\n"
        "- Follow input/output format exactly.\n"
        "- The Python code block must be fully closed with the ``` tag.\n"
        "\n[BEGIN REASONING]\n- Restate the problem briefly.\n"
        "- Describe a correct and efficient algorithm.\n"
        "- State the time complexity (e.g., O(N)).\n"
        "- List critical edge cases.\n[END REASONING]\n"
    )

def create_zero_shot_cot_prompt(t):
    return format_problem_for_prompt(t) + "\nLet's think step by step."

def create_analytic_cot_prompt(t): 
    return (
        f"Problem:\n{t}\n\nPlease provide:\n"
        "1. Problem analysis\n2. Algorithm design\n3. Edge cases\n\n"
        "Then give the final Python 3 code:\n```python\n(your code here)\n```"
    )

# --- FEW SHOT STRATEGIES ---

def create_few_shot_prompt(t, examples):
    prompt = "You will be given example problems and solutions.\n\n"
    for ex in examples:
        prompt += f"--- EXAMPLE ---\n{ex['question']}\nSolution:\n```python\n{ex['solution_code']}\n```\n\n"
    return prompt + "--- NEW PROBLEM ---\n" + t

def create_few_shot_cot_prompt(t, examples):
    prompt = "You will be given examples with reasoning and solutions.\n\n"
    for ex in examples:
        prompt += f"--- EXAMPLE ---\n{ex['question']}\n{ex['reasoning']}\nSolution:\n```python\n{ex['solution_code']}\n```\n\n"
    return prompt + "--- NEW PROBLEM ---\n" + t + "\nLet's think step by step to find the solution."

# --- AUTO & RANDOM DYNAMIC STRATEGIES ---

def create_random_few_shot_cot_prompt(problem_text, data_path, k=3):
    train_dir = os.path.join(data_path, "train")
    all_ids = os.listdir(train_dir)
    random_ids = random.sample(all_ids, k)
    
    examples = []
    for pid in random_ids:
        q, s = load_example_for_prompting(pid, data_path, "train")
        if q and s:
            reasoning = MANUAL_COTS.get(pid, "Let's think step by step to find the solution.")
            examples.append({"question": q, "reasoning": reasoning, "solution_code": s})
            
    return create_few_shot_cot_prompt(problem_text, examples)

def create_auto_few_shot_cot_prompt(problem_text, examples):
    prompt = "Here are some automatically reasoned examples with their final solutions.\n\n"
    for ex in examples:
        prompt += f"--- EXAMPLE PROBLEM ---\n{ex['question']}\n{ex['reasoning']}\nSolution:\n```python\n{ex['solution_code']}\n```\n\n"
    return prompt + "--- NEW PROBLEM TO SOLVE ---\n" + problem_text + "\nLet's think step by step to find the solution."
