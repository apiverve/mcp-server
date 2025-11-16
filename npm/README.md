# APIVerve MCP Server

<div align="center">

<img src="https://apiverve.com/images/favicon.png" alt="APIVerve Logo" width="80" />

**249+ APIs accessible through the Model Context Protocol**

[![npm version](https://img.shields.io/npm/v/@apiverve/mcp-server)](https://www.npmjs.com/package/@apiverve/mcp-server)
[![PyPI version](https://img.shields.io/pypi/v/apiverve-mcp)](https://pypi.org/project/apiverve-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)

[Website](https://apiverve.com) • [Documentation](https://docs.apiverve.com) • [API Explorer](https://apiverve.com/marketplace) • [Report Bug](https://github.com/apiverve/mcp-server/issues)

</div>

## 🚀 Overview

The **APIVerve MCP Server** provides seamless access to 249+ production-ready APIs through the [Model Context Protocol](https://modelcontextprotocol.io). Connect AI assistants like Claude, ChatGPT, and other MCP-compatible clients to a vast ecosystem of data and functionality.

### ✨ Features

- 🎯 **249+ APIs** - Weather, news, geocoding, validation, conversion, and more
- 🔐 **OAuth 2.0 Authentication** - Secure, industry-standard authentication
- 📊 **Token-Based Pricing** - Pay only for what you use
- 🚀 **High Performance** - Cloud-hosted with 99%+ uptime
- 📖 **Rich Documentation** - Complete API documentation with examples
- 🔄 **Auto-Updated** - Always access the latest API features

## 📦 Installation

### For Claude Desktop / MCP Clients

Add to your MCP settings file:

**Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "apiverve": {
      "type": "sse",
      "url": "https://api.apiverve.com/v1/mcp"
    }
  }
}
```

**VS Code / Cline:**
```json
{
  "inputs": [],
  "servers": {
    "APIVerve": {
      "type": "sse",
      "url": "https://api.apiverve.com/v1/mcp",
      "headers": {}
    }
  }
}
```

**Cursor:**
```json
{
  "mcpServers": {
    "apiverve": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything"],
      "env": {
        "MCP_BRIDGE_URL": "https://api.apiverve.com/v1/mcp"
      }
    }
  }
}
```

Or configure directly in Cursor settings (Settings > Features > Model Context Protocol)

### NPM Package

```bash
npm install -g @apiverve/mcp-server
```

Then run:
```bash
apiverve-mcp install
```

This will automatically configure your MCP client.

### Python Package

```bash
pip install apiverve-mcp
```

```python
from apiverve_mcp import configure_mcp

# Auto-configure MCP client
configure_mcp()
```

## 🔑 Authentication

APIVerve uses OAuth 2.0 for secure authentication:

1. **Sign up** at [https://apiverve.com](https://apiverve.com)
2. **Get your API key** from the dashboard
3. **Authorize** when prompted by your MCP client
4. **Start using** 249+ APIs immediately

**Free tier available** - No credit card required to start!

## 🎯 Available APIs

<details>
<summary><b>Click to see all 249+ available APIs</b></summary>

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

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async with stdio_client(StdioServerParameters(
    command="apiverve-mcp",
    args=[]
)) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize
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

Token costs vary by API complexity - simple APIs start at 1 token per call.

## 🛠️ Technical Details

### Server Information

- **Type**: Server-Sent Events (SSE)
- **Protocol**: MCP 2024-11-05
- **Authentication**: OAuth 2.0 with PKCE
- **Base URL**: `https://api.apiverve.com/v1/mcp`
- **API Version**: 1.0.1

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
