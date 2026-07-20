# APIVerve MCP server, containerized for the Docker MCP Catalog / MCP Toolkit.
#
# The APIVerve MCP server is remote (streamable-http at api.apiverve.com/v1/mcp). This
# image is a thin stdio<->remote bridge: the Docker MCP gateway speaks stdio to the
# container, and the bridge forwards to the hosted server, injecting the API key as an
# x-api-key header. No API logic lives here — it stays a small, low-maintenance proxy.
FROM node:20-alpine

LABEL org.opencontainers.image.title="APIVerve MCP Server" \
      org.opencontainers.image.description="350+ APIVerve APIs over the Model Context Protocol." \
      org.opencontainers.image.url="https://apiverve.com" \
      org.opencontainers.image.source="https://github.com/apiverve/mcp-server" \
      org.opencontainers.image.licenses="MIT"

# Pin the stdio<->remote bridge so image builds are reproducible.
RUN npm install -g mcp-remote@0.1.38

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER node
ENTRYPOINT ["/entrypoint.sh"]
