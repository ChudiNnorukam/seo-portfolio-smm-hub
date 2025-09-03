# Local Bridge Notes

This file describes a safe local bridge pattern — do not run anything here blindly.

- Purpose: allow an AI agent (Cursor/Claude/LLM) to request whitelisted actions on your machine.
- Allowed endpoints:
  - POST /read_file { path }
  - POST /write_file { path, content }
  - POST /run_cmd { name }  # name must be allowlisted (build, preview, check_perf)
- Security:
  - Sandbox all paths to repo root.
  - No free-form shell commands.
  - Require a kill switch (stop the server) to revoke access.
  - Log all requests for audit.
