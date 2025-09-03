#!/usr/bin/env python3
"""
Agent Client - Interactive client for the Agent Bridge
"""

import os
import json
import requests
import sys
from typing import Dict, Any

# Configuration
BRIDGE_URL = os.getenv("AGENT_BRIDGE_URL", "http://127.0.0.1:3333")
BRIDGE_TOKEN = os.getenv("AGENT_BRIDGE_TOKEN", "43t39hhg478gh84g7342ty928hg479ghghihw8020390j2r3f0h")

class AgentClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the bridge."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Details: {error_detail}")
                except:
                    print(f"   Response: {e.response.text}")
            return {}
    
    def health_check(self) -> bool:
        """Check if the bridge is running."""
        result = self._make_request("GET", "/")
        if result and result.get("status") == "ok":
            print(f"✅ Bridge is running at {self.base_url}")
            print(f"   Repository root: {result.get('repo_root')}")
            return True
        else:
            print(f"❌ Bridge is not responding at {self.base_url}")
            return False
    
    def read_file(self, path: str) -> str:
        """Read a file from the repository."""
        result = self._make_request("POST", "/read_file", {"path": path})
        if result and "content" in result:
            print(f"✅ Read file: {result.get('path')}")
            return result["content"]
        else:
            print(f"❌ Failed to read file: {path}")
            return ""
    
    def write_file(self, path: str, content: str) -> bool:
        """Write content to a file in the repository."""
        result = self._make_request("POST", "/write_file", {"path": path, "content": content})
        if result and result.get("status") == "success":
            print(f"✅ Wrote file: {result.get('path')}")
            return True
        else:
            print(f"❌ Failed to write file: {path}")
            return False
    
    def run_command(self, name: str) -> Dict[str, Any]:
        """Run a whitelisted command."""
        result = self._make_request("POST", "/run_cmd", {"name": name})
        if result and result.get("status") == "success":
            print(f"✅ Command '{name}' completed")
            print(f"   Return code: {result.get('returncode')}")
            if result.get("stdout"):
                print(f"   Output:\n{result['stdout']}")
            if result.get("stderr"):
                print(f"   Errors:\n{result['stderr']}")
            return result
        else:
            print(f"❌ Command '{name}' failed")
            return {}
    
    def get_allowed_commands(self) -> list:
        """Get list of allowed commands."""
        result = self._make_request("GET", "/allowed_commands")
        if result and "allowed_commands" in result:
            return result["allowed_commands"]
        return []

def print_help():
    """Print help information."""
    print("""
🤖 Agent Client - Interactive Bridge Client

Commands:
  help, h          - Show this help
  health           - Check bridge health
  read <path>      - Read a file
  write <path>     - Write to a file (will prompt for content)
  run <command>    - Run a whitelisted command
  commands         - List allowed commands
  quit, q, exit    - Exit the client

Examples:
  read seo-portfolio/package.json
  write test.txt
  run build
  run check_perf
""")

def main():
    """Main interactive loop."""
    print("🤖 Agent Client Starting...")
    print(f"   Bridge URL: {BRIDGE_URL}")
    print(f"   Token: {BRIDGE_TOKEN[:10]}...")
    
    client = AgentClient(BRIDGE_URL, BRIDGE_TOKEN)
    
    # Check bridge health
    if not client.health_check():
        print("\n❌ Cannot connect to bridge. Make sure it's running:")
        print("   uvicorn bridge:app --host 127.0.0.1 --port 3333")
        sys.exit(1)
    
    print("\n✅ Connected to bridge successfully!")
    print_help()
    
    while True:
        try:
            command = input("\n🤖 > ").strip()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd in ["quit", "q", "exit"]:
                print("👋 Goodbye!")
                break
            
            elif cmd in ["help", "h"]:
                print_help()
            
            elif cmd == "health":
                client.health_check()
            
            elif cmd == "read" and len(parts) > 1:
                path = parts[1]
                content = client.read_file(path)
                if content:
                    print(f"\n📄 Content of {path}:")
                    print("-" * 50)
                    print(content)
                    print("-" * 50)
            
            elif cmd == "write" and len(parts) > 1:
                path = parts[1]
                print(f"📝 Enter content for {path} (end with Ctrl+D or 'END' on new line):")
                lines = []
                try:
                    while True:
                        line = input()
                        if line.strip() == "END":
                            break
                        lines.append(line)
                except EOFError:
                    pass
                
                content = "\n".join(lines)
                client.write_file(path, content)
            
            elif cmd == "run" and len(parts) > 1:
                command_name = parts[1]
                client.run_command(command_name)
            
            elif cmd == "commands":
                commands = client.get_allowed_commands()
                print(f"📋 Allowed commands: {', '.join(commands)}")
            
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
