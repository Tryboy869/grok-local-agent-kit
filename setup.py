from setuptools import setup, find_packages

setup(
    name="grok-local-agent-kit",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["ollama"],
    python_requires=">=3.10",
    description="Local AI Agent Kit",
)