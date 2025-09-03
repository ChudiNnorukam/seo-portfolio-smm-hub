#!/bin/bash
# Agent Setup Script

echo "🤖 Setting up Agent Bridge..."

# Set environment variables
export AGENT_REPO_ROOT="/Users/chudinnorukam/Documents/Chudi's SEO Portfolio SMM Hub"
export AGENT_BRIDGE_URL="http://127.0.0.1:3333"
export AGENT_BRIDGE_TOKEN="43t39hhg478gh84g7342ty928hg479ghghihw8020390j2r3f0h"

echo "✅ Environment variables set:"
echo "   AGENT_REPO_ROOT: $AGENT_REPO_ROOT"
echo "   AGENT_BRIDGE_URL: $AGENT_BRIDGE_URL"
echo "   AGENT_BRIDGE_TOKEN: ${AGENT_BRIDGE_TOKEN:0:10}..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install --user requests fastapi uvicorn

echo ""
echo "🚀 Setup complete! Now you can:"
echo ""
echo "1. Start the bridge (in one terminal):"
echo "   cd scripts && uvicorn bridge:app --host 127.0.0.1 --port 3333"
echo ""
echo "2. Run the client (in another terminal):"
echo "   cd scripts && python3 agent_client.py"
echo ""
echo "3. Or run this setup script to set environment variables:"
echo "   source scripts/setup_agent.sh"
