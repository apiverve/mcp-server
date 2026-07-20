#!/bin/sh
# Bridge stdio (spoken by the Docker MCP gateway / client) to the remote APIVerve MCP
# server. With APIVERVE_API_KEY set, the key is forwarded as an x-api-key header; without
# it, the bridge falls back to the server's OAuth challenge.
set -e

URL="https://api.apiverve.com/v1/mcp"

if [ -n "$APIVERVE_API_KEY" ]; then
  exec mcp-remote "$URL" --header "x-api-key:${APIVERVE_API_KEY}"
else
  echo "APIVERVE_API_KEY not set — using OAuth. Get a key at https://apiverve.com to run headless." >&2
  exec mcp-remote "$URL"
fi
