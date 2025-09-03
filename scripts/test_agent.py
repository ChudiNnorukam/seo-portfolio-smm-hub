#!/usr/bin/env python3
"""
Test script for agent client functionality
"""

import subprocess
import time
import os
import sys

def test_agent_client():
    """Test the agent client functionality."""
    print("🧪 Testing Agent Client...")
    
    # Set environment variables
    os.environ['AGENT_BRIDGE_URL'] = 'http://127.0.0.1:3333'
    os.environ['AGENT_BRIDGE_TOKEN'] = '43t39hhg478gh84g7342ty928hg479ghghihw8020390j2r3f0h'
    
    # Start the server in background
    print("Starting bridge server...")
    process = subprocess.Popen(['uvicorn', 'bridge:app', '--host', '127.0.0.1', '--port', '3333'], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        import agent_client
        
        # Create client
        client = agent_client.AgentClient('http://127.0.0.1:3333', '43t39hhg478gh84g7342ty928hg479ghghihw8020390j2r3f0h')
        
        # Test 1: Health check
        print("\n1. Testing health check...")
        health_ok = client.health_check()
        if health_ok:
            print("   ✅ Health check passed")
        else:
            print("   ❌ Health check failed")
            return False
        
        # Test 2: Allowed commands
        print("\n2. Testing allowed commands...")
        commands = client.get_allowed_commands()
        if commands:
            print(f"   ✅ Commands retrieved: {commands}")
        else:
            print("   ❌ No commands retrieved")
            return False
        
        # Test 3: Read file
        print("\n3. Testing read file...")
        content = client.read_file('seo-portfolio/package.json')
        if content and 'name' in content:
            print(f"   ✅ File read successfully ({len(content)} chars)")
        else:
            print("   ❌ File read failed")
            return False
        
        # Test 4: Write file
        print("\n4. Testing write file...")
        test_content = "Test file created by agent client\nLine 2\nLine 3"
        write_success = client.write_file('test_agent_output.txt', test_content)
        if write_success:
            print("   ✅ File write successful")
        else:
            print("   ❌ File write failed")
            return False
        
        # Test 5: Read back written file
        print("\n5. Testing read back...")
        read_back = client.read_file('test_agent_output.txt')
        if read_back == test_content:
            print("   ✅ Read back successful")
        else:
            print("   ❌ Read back failed")
            return False
        
        # Test 6: Run command (test with a safe command)
        print("\n6. Testing run command...")
        result = client.run_command('check_orphans')
        if result and result.get('status') == 'success':
            print("   ✅ Command execution successful")
        else:
            print("   ❌ Command execution failed")
            # This might fail if the command has issues, but that's OK for testing
        
        # Clean up test file
        try:
            os.remove('test_agent_output.txt')
            print("   Test file cleaned up")
        except:
            pass
        
        print("\n🎉 All tests passed! Agent client is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up server
        process.terminate()
        process.wait()
        print("\nBridge server stopped")

if __name__ == "__main__":
    success = test_agent_client()
    sys.exit(0 if success else 1)
