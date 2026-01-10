from huggingface_hub import InferenceClient

def generate_response(question, api_key):
    """Sends a problem to LLaMA via Hugging Face Inference API."""
    client = InferenceClient(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct:novita",
            messages=[{"role": "user", "content": question.strip()}],
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"Error: {e}"