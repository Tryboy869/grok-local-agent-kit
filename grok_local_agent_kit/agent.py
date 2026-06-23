import ollama
def run_local_agent(prompt):
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']
print('Basic agent ready!')