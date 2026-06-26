from setuptools import setup, find_packages
setup(
    name='grok-local-agent-kit',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['ollama', 'langchain'],
)