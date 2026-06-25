import ollama
from typing import List, Dict, Any, Optional
import json
from .tools import TOOLS
import requests

class LocalAgent:
    def __init__(self, llm_provider: str = "ollama", model: str = "llama3"):
        self.llm_provider = llm_provider
        self.model = model
        self.tools = TOOLS
        self.history = []

    def _call_llm(self, prompt: str) -> str:
        if self.llm_provider == "ollama":
            try:
                response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
                return response['message']['content']
            except Exception as e:
                return f"Ollama error: {e}"
        elif self.llm_provider == "lmstudio":
            try:
                resp = requests.post("http://localhost:1234/v1/chat/completions", json={
                    "model": self.model, "messages": [{"role": "user", "content": prompt}]
                }, timeout=30)
                return resp.json()["choices"][0]["message"]["content"]
            except:
                return "LM Studio not reachable."
        return "Unknown provider."

    def _parse_tool_call(self, response: str) -> Optional[Dict]:
        try:
            if "TOOL_CALL:" in response.upper():
                tool_str = response.split("TOOL_CALL:", 1)[1].strip().split("\n")[0]
                return json.loads(tool_str)
        except:
            pass
        return None

    def run(self, prompt: str, max_steps: int = 5) -> str:
        self.history.append({"role": "user", "content": prompt})
        for _ in range(max_steps):
            full_prompt = self._build_prompt()
            response = self._call_llm(full_prompt)
            self.history.append({"role": "assistant", "content": response})
            tool_call = self._parse_tool_call(response)
            if tool_call:
                tool_name = tool_call.get("tool")
                args = tool_call.get("args", {})
                if tool_name in self.tools:
                    try:
                        result = self.tools[tool_name](**args)
                        self.history.append({"role": "tool", "content": str(result)})
                    except Exception as e:
                        self.history.append({"role": "tool", "content": f"Error: {e}" })
                    continue
            return response  # final
        return "Agent completed." 

    def _build_prompt(self) -> str:
        tool_desc = "\n".join([f"- {name}: {func.__doc__ or 'No doc'}" for name, func in self.tools.items()])
        hist = "\n".join([f"{h['role']}: {h.get('content', '')[:200]}" for h in self.history])
        return f"""Local Agent instructions: Reason step by step. Use tools if needed by outputting TOOL_CALL: {{"tool": "xxx", "args": {{...}}}} exactly.

Tools:
{tool_desc}

Conversation:
{hist}

Respond:"""

def run_local_agent(prompt: str):
    agent = LocalAgent()
    return agent.run(prompt)