#!/usr/bin/env python3
"""
Local Bridge for AI Agent
Safe local bridge pattern for AI agents to interact with the local development environment.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agent Bridge", version="1.0.0")

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security: Whitelisted commands
ALLOWED_COMMANDS = {
    "build": "cd seo-portfolio && npm run build",
    "preview": "cd seo-portfolio && npm run preview -- --port 4321",
    "check_perf": "./scripts/check-performance.sh",
    "check_orphans": "python3 scripts/check-orphans.py",
    "lighthouse": "npx lighthouse http://localhost:4321 --output=json --output-path=lighthouse-report.json",
    "pa11y": "npx pa11y http://localhost:4321/",
}

# Get repo root from environment
REPO_ROOT = os.getenv("AGENT_REPO_ROOT", "/Users/chudinnorukam/Documents/Chudi's SEO Portfolio SMM Hub")

def validate_path(path: str) -> Path:
    """Validate and sanitize file paths to prevent directory traversal."""
    full_path = Path(REPO_ROOT) / path
    try:
        # Resolve to absolute path and check if it's within repo root
        resolved = full_path.resolve()
        repo_root_resolved = Path(REPO_ROOT).resolve()
        
        if not str(resolved).startswith(str(repo_root_resolved)):
            raise HTTPException(status_code=403, detail="Path outside repository root")
        
        return resolved
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid path: {e}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for audit purposes."""
    logger.info(f"{request.method} {request.url} - {request.client.host}")
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "repo_root": REPO_ROOT}

@app.post("/read_file")
async def read_file(data: Dict[str, Any]):
    """Read a file from the repository."""
    try:
        path = data.get("path")
        if not path:
            raise HTTPException(status_code=400, detail="Path required")
        
        file_path = validate_path(path)
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise HTTPException(status_code=400, detail=f"Path is not a file: {file_path}")
        
        content = file_path.read_text(encoding='utf-8')
        
        logger.info(f"Read file: {file_path}")
        return {"content": content, "path": str(file_path)}
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/write_file")
async def write_file(data: Dict[str, Any]):
    """Write content to a file in the repository."""
    try:
        path = data.get("path")
        content = data.get("content")
        
        if not path:
            raise HTTPException(status_code=400, detail="Path required")
        
        if content is None:
            raise HTTPException(status_code=400, detail="Content required")
        
        file_path = validate_path(path)
        
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        file_path.write_text(content, encoding='utf-8')
        
        logger.info(f"Wrote file: {file_path}")
        return {"status": "success", "path": str(file_path)}
        
    except Exception as e:
        logger.error(f"Error writing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run_cmd")
async def run_cmd(data: Dict[str, Any]):
    """Run a whitelisted command."""
    try:
        name = data.get("name")
        if not name:
            raise HTTPException(status_code=400, detail="Command name required")
        
        if name not in ALLOWED_COMMANDS:
            raise HTTPException(
                status_code=403, 
                detail=f"Command not allowed. Allowed: {list(ALLOWED_COMMANDS.keys())}"
            )
        
        command = ALLOWED_COMMANDS[name]
        
        logger.info("Running command: %s -> %s", name, command)
        
        # Execute command
        import subprocess
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=False
        )
        
        return {
            "status": "success",
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error running command: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/allowed_commands")
async def get_allowed_commands():
    """Get list of allowed commands."""
    return {"allowed_commands": list(ALLOWED_COMMANDS.keys())}

if __name__ == "__main__":
    print(f"Starting Agent Bridge on http://127.0.0.1:3333")
    print(f"Repository root: {REPO_ROOT}")
    print(f"Allowed commands: {list(ALLOWED_COMMANDS.keys())}")
    
    uvicorn.run(
        "bridge:app",
        host="127.0.0.1",
        port=3333,
        reload=True,
        log_level="info"
    )
