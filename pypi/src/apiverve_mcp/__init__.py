"""
APIVerve MCP Server - Auto-configuration for Python
"""

import json
import os
import platform
from pathlib import Path
from typing import Optional

__version__ = "1.0.0"

SERVER_CONFIG = {
    "type": "sse",
    "url": "https://api.apiverve.com/v1/mcp"
}


def get_claude_config_path() -> Path:
    """Get the Claude Desktop config file path for the current OS."""
    system = platform.system()

    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        appdata = os.getenv("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA environment variable not found")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def get_vscode_config_path() -> Path:
    """Get the VS Code config file path for the current OS."""
    system = platform.system()

    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Code" / "User" / "settings.json"
    elif system == "Windows":
        appdata = os.getenv("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA environment variable not found")
        return Path(appdata) / "Code" / "User" / "settings.json"
    else:  # Linux
        return Path.home() / ".config" / "Code" / "User" / "settings.json"


def get_cursor_config_path() -> Path:
    """Get the Cursor config file path for the current OS."""
    system = platform.system()

    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "settings.json"
    elif system == "Windows":
        appdata = os.getenv("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA environment variable not found")
        return Path(appdata) / "Cursor" / "User" / "settings.json"
    else:  # Linux
        return Path.home() / ".config" / "Cursor" / "User" / "settings.json"


def configure_claude_desktop() -> bool:
    """
    Configure Claude Desktop with APIVerve MCP server.

    Returns:
        bool: True if successful, False otherwise
    """
    config_path = get_claude_config_path()

    print(f"📍 Claude Desktop config path: {config_path}")

    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing config
    config = {}
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Could not parse existing config, creating new one")

    # Ensure mcpServers section exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Add APIVerve server
    config["mcpServers"]["apiverve"] = SERVER_CONFIG

    # Write config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    print("✅ APIVerve MCP server added to Claude Desktop config")
    return True


def configure_vscode() -> bool:
    """
    Configure VS Code with APIVerve MCP server.

    Returns:
        bool: True if successful, False otherwise
    """
    config_path = get_vscode_config_path()

    print(f"📍 VS Code config path: {config_path}")

    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing config
    config = {}
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Could not parse existing config, creating new one")

    # Ensure mcp section exists
    if "mcp" not in config:
        config["mcp"] = {"servers": {}}
    if "servers" not in config["mcp"]:
        config["mcp"]["servers"] = {}

    # Add APIVerve server
    config["mcp"]["servers"]["APIVerve"] = {
        "type": "sse",
        "url": SERVER_CONFIG["url"],
        "headers": {}
    }

    # Write config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    print("✅ APIVerve MCP server added to VS Code config")
    return True


def configure_cursor() -> bool:
    """
    Configure Cursor with APIVerve MCP server.

    Returns:
        bool: True if successful, False otherwise
    """
    config_path = get_cursor_config_path()

    print(f"📍 Cursor config path: {config_path}")

    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing config
    config = {}
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Could not parse existing config, creating new one")

    # Ensure mcpServers section exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Add APIVerve server
    config["mcpServers"]["apiverve"] = SERVER_CONFIG

    # Write config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    print("✅ APIVerve MCP server added to Cursor config")
    return True


def configure_mcp(target: str = "all") -> bool:
    """
    Auto-configure MCP client with APIVerve server.

    Args:
        target: Which client to configure ("claude", "vscode", "cursor", or "all")

    Returns:
        bool: True if successful, False otherwise
    """
    print("\n🔌 APIVerve MCP Server Configuration\n")

    try:
        if target in ("claude", "all"):
            configure_claude_desktop()

        if target in ("vscode", "all"):
            configure_vscode()

        if target in ("cursor", "all"):
            configure_cursor()

        print("\n✨ Configuration complete!")
        print("\n📖 Next steps:")
        print("   1. Restart your MCP client (Claude Desktop, VS Code, or Cursor)")
        print("   2. Sign up at https://apiverve.com")
        print("   3. Authorize when prompted")
        print("   4. Start using 249+ APIs!\n")

        return True
    except Exception as e:
        print(f"\n❌ Configuration failed: {e}")
        print("\n💡 Manual configuration:")
        print("   Add this to your MCP client config:\n")
        print("   {")
        print('     "mcpServers": {')
        print('       "apiverve": {')
        print('         "type": "sse",')
        print('         "url": "https://api.apiverve.com/v1/mcp"')
        print("       }")
        print("     }")
        print("   }\n")
        return False
