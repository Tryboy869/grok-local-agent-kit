#!/usr/bin/env bash
# One-command install for grok-local-agent-kit
set -euo pipefail
python3 -m pip install -U "git+https://github.com/Tryboy869/grok-local-agent-kit.git"
echo
echo "Installed. Next:"
echo "  grok-agent doctor"
echo "  grok-agent init"
echo "  grok-agent chat -v --stream --router"
