import ollama

def run_local_agent(prompt: str):
    response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

print('Agent ready!')