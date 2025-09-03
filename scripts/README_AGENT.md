# Agent Bridge Setup

This directory contains the Agent Bridge system for safe AI agent interaction with your local development environment.

## Files

- `bridge.py` - FastAPI server that provides safe endpoints for AI agents
- `agent_client.py` - Interactive client for testing the bridge
- `setup_agent.sh` - Setup script for environment variables
- `README_AGENT.md` - This documentation

## Quick Start

### 1. Set Environment Variables (run once)

```bash
# Set these environment variables
export AGENT_REPO_ROOT="/Users/chudinnorukam/Documents/Chudi's SEO Portfolio SMM Hub"
export AGENT_BRIDGE_URL="http://127.0.0.1:3333"
export AGENT_BRIDGE_TOKEN="43t39hhg478gh84g7342ty928hg479ghghihw8020390j2r3f0h"

# Or run the setup script
source scripts/setup_agent.sh
```

### 2. Install Dependencies (run once)

```bash
python3 -m pip install --user requests fastapi uvicorn
```

### 3. Start the Bridge (in one terminal)

```bash
cd scripts
uvicorn bridge:app --host 127.0.0.1 --port 3333
```

### 4. Run the Client (in another terminal)

```bash
cd scripts
python3 agent_client.py
```

## Security Features

- **Path Validation**: All file paths are validated to prevent directory traversal
- **Command Whitelist**: Only pre-approved commands can be executed
- **Repository Sandbox**: All operations are restricted to the repository root
- **Request Logging**: All requests are logged for audit purposes
- **Kill Switch**: Stop the bridge server to revoke all access

## Allowed Commands

- `build` - Build the Astro site
- `preview` - Start preview server
- `check_perf` - Run performance check
- `check_orphans` - Check for orphan links
- `lighthouse` - Run Lighthouse audit
- `pa11y` - Run accessibility check

## API Endpoints

- `GET /` - Health check
- `POST /read_file` - Read a file from the repository
- `POST /write_file` - Write content to a file
- `POST /run_cmd` - Execute a whitelisted command
- `GET /allowed_commands` - List allowed commands

## Client Commands

- `help` - Show help
- `health` - Check bridge health
- `read <path>` - Read a file
- `write <path>` - Write to a file
- `run <command>` - Run a whitelisted command
- `commands` - List allowed commands
- `quit` - Exit the client

## Example Usage

```bash
# Start bridge
uvicorn bridge:app --host 127.0.0.1 --port 3333

# In another terminal, run client
python3 agent_client.py

# Client commands:
🤖 > health
🤖 > read seo-portfolio/package.json
🤖 > run build
🤖 > run check_perf
🤖 > quit
```

## Testing

Run the automated test suite to verify everything works:

```bash
cd scripts
python3 test_agent.py
```

This will:
- Start the bridge server
- Test all client functionality
- Verify file operations
- Test command execution
- Clean up and stop the server

## Troubleshooting

- **Bridge not responding**: Make sure the bridge is running on port 3333
- **Permission denied**: Check that scripts are executable (`chmod +x`)
- **Path errors**: Verify `AGENT_REPO_ROOT` is set correctly
- **Command not allowed**: Check the whitelist in `bridge.py`
- **500 errors**: Check the bridge server logs for detailed error messages
