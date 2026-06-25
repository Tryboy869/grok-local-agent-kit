from setuptools import setup, find_packages

setup(
    name="grok-local-agent-kit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ollama",
        "requests",
        "pydantic",
    ],
    python_requires=">=3.10",
    author="Tryboy869",
    author_email="",
    description="Local AI Agent Kit with Ollama/MCP support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tryboy869/grok-local-agent-kit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
