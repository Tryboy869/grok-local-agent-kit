# Security Policy

## Supported versions

The `main` branch and the latest tagged release are supported.

## Reporting a vulnerability

Do **not** open a public issue for security problems that could let an agent escape the sandbox or execute unexpected code.

Email the address on the GitHub profile of [@Tryboy869](https://github.com/Tryboy869) with:

- affected version / commit
- reproduction steps
- impact (RCE, data leak, prompt injection leading to shell, etc.)

We will acknowledge within a few days when possible.

## Known risk surface

This kit can run shell commands, fetch URLs, and execute restricted Python when those tools are enabled. Treat it like any local coding agent: do not point it at untrusted prompts with tools unlocked, and review traces before you automate.
