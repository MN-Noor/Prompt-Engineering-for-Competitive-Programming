import re
import subprocess

def extract_python_code(text):
    blocks = re.findall(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if blocks:
        code_blocks = [b.strip() for b in blocks if re.search(r"\bdef\b|\bfor\b|import", b)]
        return max(code_blocks, key=len) if code_blocks else blocks[0].strip()
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL).strip()

def run_test_cases(code, tests):
    ins, outs = tests.get("inputs", []), tests.get("outputs", [])
    for i, (inp, outp) in enumerate(zip(ins, outs)):
        input_str = "\n".join(inp) if isinstance(inp, list) else str(inp)
        try:
            p = subprocess.run(
                ["python3", "-c", code],
                input=input_str, text=True, capture_output=True, timeout=5
            )
            if p.returncode != 0: return "ERROR", f"Runtime error: {p.stderr.strip()}"
            if p.stdout.strip() != (outp[0].strip() if isinstance(outp, list) else outp.strip()):
                return "FAIL", f"Mismatch on test {i+1}"
        except subprocess.TimeoutExpired:
            return "ERROR", "Timeout"
    return "PASS", f"All {len(ins)} tests passed"