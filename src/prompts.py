def format_base_problem(text):
    return f"Problem:\n{text}\n"

def create_zero_shot_prompt(t):
    return (
        format_base_problem(t) +
        "\nFollow these instructions exactly:\n"
        "Code:\n```python\n# ONLY runnable Python 3 code here\n```\n"
        "\nRules:\n- No comments or text inside the code block.\n"
        "- Follow input/output format exactly.\n"
        "- The Python code block must be fully closed and contain the entire runnable solution.\n\n"
        "You are solving a competitive programming problem.\n"
        "[BEGIN REASONING]\n- Restate problem briefly.\n- Describe efficient algorithm.\n"
        "- State time complexity.\n- List edge cases.\n[END REASONING]\n"
    )

def create_few_shot_cot_prompt(t, examples):
    prompt = "You will be given examples with reasoning and solutions.\n\n"
    for ex in examples:
        prompt += f"--- EXAMPLE ---\n{ex['question']}\n{ex['reasoning']}\nSolution:\n```python\n{ex['solution_code']}\n```\n\n"
    return prompt + "--- NEW PROBLEM ---\n" + t + "\nLet's think step by step to find the solution."