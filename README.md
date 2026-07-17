# APIVerve MCP Server

<div align="center">

<img src="https://apiverve.com/images/favicon.png" alt="APIVerve Logo" width="80" />

**360+ APIs accessible through the Model Context Protocol**

[![npm version](https://img.shields.io/npm/v/@apiverve/mcp-server)](https://www.npmjs.com/package/@apiverve/mcp-server)
[![PyPI version](https://img.shields.io/pypi/v/apiverve-mcp)](https://pypi.org/project/apiverve-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)

[Website](https://apiverve.com) • [Documentation](https://docs.apiverve.com) • [API Explorer](https://apiverve.com/marketplace) • [Report Bug](https://github.com/apiverve/mcp-server/issues)

</div>

## 🚀 Overview

The **APIVerve MCP Server** provides seamless access to 360+ production-ready APIs through the [Model Context Protocol](https://modelcontextprotocol.io). Connect AI assistants like Claude, ChatGPT, and other MCP-compatible clients to a vast ecosystem of data and functionality.

### ✨ Features

- 🎯 **360+ APIs** - Weather, news, geocoding, validation, conversion, and more
- 🔐 **OAuth 2.0 Authentication** - Secure, industry-standard authentication
- 📊 **Token-Based Pricing** - Pay only for what you use
- 🚀 **High Performance** - Cloud-hosted with 99%+ uptime
- 📖 **Rich Documentation** - Complete API documentation with examples
- 🔄 **Auto-Updated** - Always access the latest API features

## 📦 Installation

APIVerve is a **remote** MCP server — there is nothing to run locally. Point your client at the URL below and it will handle sign-in for you.

### Quick setup

```bash
npx @apiverve/mcp-server
```

Configures VS Code and Cursor, and prints the manual step for Claude Desktop. Target one client with `npx @apiverve/mcp-server cursor`.

For headless setups, pass a key instead of using sign-in:

```bash
npx @apiverve/mcp-server --api-key YOUR_API_KEY
```

Python users can do the same with `pip install apiverve-mcp` then `apiverve-mcp` (or `apiverve-mcp --api-key YOUR_API_KEY`).

### Manual setup

**Claude Desktop** — remote servers are added through the app, not a config file:

> Settings → Connectors → Add custom connector → `https://api.apiverve.com/v1/mcp`

**VS Code** (`mcp.json`):
```json
{
  "servers": {
    "apiverve": {
      "type": "http",
      "url": "https://api.apiverve.com/v1/mcp"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "apiverve": {
      "url": "https://api.apiverve.com/v1/mcp"
    }
  }
}
```

## 🔑 Authentication

Two ways in — pick whichever fits:

**OAuth (default, recommended)** — leave the config as shown above. On first use the server returns an authorization challenge and your client walks you through sign-in. No key is stored on disk, and access can be revoked from the dashboard.

**API key** — add your key as a header. Useful for CI and headless environments where no browser is available:

```json
{
  "mcpServers": {
    "apiverve": {
      "url": "https://api.apiverve.com/v1/mcp",
      "headers": { "x-api-key": "YOUR_API_KEY" }
    }
  }
}
```

Claude Desktop's Custom Connectors cannot send custom headers, so it is OAuth-only.

Get a key at [https://apiverve.com](https://apiverve.com). **Free tier available** — no credit card required to start!

## 🎯 Available APIs

<details>
<summary><b>Click to see all 360+ available APIs</b></summary>

### 🌤️ Weather & Environment
- Weather Forecast
- Air Quality
- Marine Weather
- UV Index
- Weather Seasons
- And more...

### 🌍 Location & Geocoding
- Reverse Geocoding
- IP Lookup
- Timezone Lookup
- Airports Lookup
- Distance Calculator
- And more...

### ✅ Validation & Verification
- Email Validator
- Phone Number Validator
- Domain Availability
- SSL Certificate Checker
- And more...

### 🔄 Conversion & Calculation
- Currency Converter
- Unit Converter
- Date Calculator
- BMI Calculator
- And more...

### 📰 News & Content
- World News
- RSS to JSON
- Web Scraper
- Metadata Extractor
- And more...

### 🎲 Random Data Generators
- Random User Generator
- Password Generator
- Lorem Ipsum Generator
- And more...

**[See complete API list →](https://apiverve.com/marketplace)**

</details>

## 💡 Usage Examples

Once configured, use APIs naturally in conversation:

### With Claude Desktop

```
User: What's the weather in San Francisco?
Claude: [Uses Weather API]

User: Validate this email: test@example.com
Claude: [Uses Email Validator API]

User: Convert 100 USD to EUR
Claude: [Uses Currency Converter API]
```

### Programmatic Usage (Python)

Connect straight to the remote server — no local process involved:

```python
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

url = "https://api.apiverve.com/v1/mcp"
headers = {"x-api-key": "YOUR_API_KEY"}

async with streamablehttp_client(url, headers=headers) as (read, write, _):
    async with ClientSession(read, write) as session:
        await session.initialize()

        # List available tools
        tools = await session.list_tools()

        # Call a tool
        result = await session.call_tool("emailvalidator", {
            "email": "test@example.com"
        })
```

## 📊 Pricing

APIVerve uses a flexible token-based pricing model with multiple tiers to fit your needs:

- **Free Tier Available** - Start building immediately, no credit card required
- **Pay-as-you-go** - Scale up as your usage grows
- **Enterprise Plans** - Custom solutions for high-volume users

**[View Pricing Plans →](https://apiverve.com/pricing)**

Credit costs vary by API complexity - simple APIs start at 1 credit per call.

## 🛠️ Technical Details

### Server Information

- **Transport**: Streamable HTTP
- **Protocol**: MCP 2025-06-18 (negotiates down to 2025-03-26 and 2024-11-05)
- **Authentication**: OAuth 2.0 with PKCE, or `x-api-key` header
- **Base URL**: `https://api.apiverve.com/v1/mcp`
- **API Version**: 1.1.0

### OAuth Endpoints

- **Discovery**: `https://api.apiverve.com/.well-known/openid-configuration`
- **Authorization**: `https://api.apiverve.com/authorize`
- **Token**: `https://api.apiverve.com/token`
- **Registration**: `https://api.apiverve.com/register` (Dynamic client registration)

### Tool Schema

Each API is exposed as an MCP tool with:
- **name**: API identifier (e.g., `emailvalidator`)
- **description**: Human-readable description with token cost
- **inputSchema**: JSON Schema defining required/optional parameters

## 🔧 Troubleshooting

### Connection Issues

If you see authentication errors:

1. Check your API key at [https://apiverve.com/dashboard](https://apiverve.com/dashboard)
2. Ensure OAuth redirect URI is correct
3. Try re-authorizing the connection

### Token Limits

If you hit token limits:
- Check usage at [https://apiverve.com/dashboard](https://apiverve.com/dashboard)
- Upgrade your plan
- Contact support for enterprise options

## 📚 Documentation

- **API Documentation**: [https://docs.apiverve.com](https://docs.apiverve.com)
- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Getting Started Guide**: [https://apiverve.com/docs/getting-started](https://apiverve.com/docs/getting-started)

## 🤝 Support

- **GitHub Issues**: [apiverve/mcp-server/issues](https://github.com/apiverve/mcp-server/issues)
- **Email**: hello@apiverve.com
- **Discord**: [Join our community](https://apiverve.com/discord)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star Us!

If you find this useful, please consider starring the repo on GitHub!

---

<div align="center">

**Built with ❤️ by [APIVerve](https://apiverve.com)**

[Website](https://apiverve.com) • [Dashboard](https://apiverve.com/dashboard) • [API Explorer](https://apiverve.com/marketplace) • [Documentation](https://docs.apiverve.com)

</div>
