import os
import requests
from typing import Dict, Any
import subprocess

def web_search(query: str) -> str:
    try:
        resp = requests.get(f'https://api.duckduckgo.com/?q={query}&format=json', timeout=5)
        return str(resp.json())[:1000] if resp.ok else 'Search failed.'
    except:
        return 'Offline: web unavailable.'

def file_read(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()[:2000]
    except Exception as e:
        return f'Error: {e}'

def file_write(path: str, content: str) -> str:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return 'Success.'
    except Exception as e:
        return f'Error: {e}'

def shell_exec(cmd: str) -> str:
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout + '\n' + result.stderr
    except Exception as e:
        return f'Exec error: {e}'

TOOLS = {
    'web_search': web_search,
    'file_read': file_read,
    'file_write': file_write,
    'shell_exec': shell_exec,
}