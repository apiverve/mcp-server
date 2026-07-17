"""
APIVerve MCP Server - client configuration for Python
"""

import json
import os
import platform
from pathlib import Path
from typing import Optional

__version__ = "1.0.0"

SERVER_URL = "https://api.apiverve.com/v1/mcp"
TARGETS = ("claude", "vscode", "cursor", "all")


def _user_config_dir(app_name: str) -> Path:
    """Per-OS location for an app's user config directory."""
    system = platform.system()

    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / app_name
    elif system == "Windows":
        appdata = os.getenv("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA environment variable not found")
        return Path(appdata) / app_name
    else:
        return Path.home() / ".config" / app_name


def get_vscode_config_path() -> Path:
    """VS Code moved MCP config out of settings.json into its own mcp.json."""
    return _user_config_dir("Code") / "User" / "mcp.json"


def get_cursor_config_path() -> Path:
    """Cursor reads ~/.cursor/mcp.json, not the app support dir."""
    return Path.home() / ".cursor" / "mcp.json"


def _read_json(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise RuntimeError(
            f"{config_path} exists but is not valid JSON. Fix or remove it, then re-run."
        )


def _write_json(config_path: Path, data: dict) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _auth_headers(api_key: Optional[str]) -> dict:
    return {"headers": {"x-api-key": api_key}} if api_key else {}


def configure_claude_desktop() -> bool:
    """
    Claude Desktop only accepts remote MCP servers through Custom Connectors, which
    cannot be configured from a file - claude_desktop_config.json is stdio-only. Print
    the manual step rather than writing config Claude ignores.
    """
    print("[!] Claude Desktop - manual step required")
    print("  Claude Desktop only accepts remote MCP servers through Custom Connectors,")
    print("  which cannot be configured from a file. Add it in the app:")
    print("")
    print("    Settings -> Connectors -> Add custom connector")
    print(f"    URL: {SERVER_URL}")
    print("")
    print("  Claude will prompt you to sign in on first use.")
    print("")
    return True


def configure_vscode(api_key: Optional[str] = None) -> bool:
    """Configure VS Code with the APIVerve MCP server."""
    config_path = get_vscode_config_path()
    config = _read_json(config_path)

    config.setdefault("servers", {})
    config["servers"]["apiverve"] = {
        "type": "http",
        "url": SERVER_URL,
        **_auth_headers(api_key),
    }

    _write_json(config_path, config)
    print(f"[ok] VS Code configured - {config_path}")
    return True


def configure_cursor(api_key: Optional[str] = None) -> bool:
    """Configure Cursor with the APIVerve MCP server."""
    config_path = get_cursor_config_path()
    config = _read_json(config_path)

    # Cursor infers the transport from the presence of url; type is for stdio servers only.
    config.setdefault("mcpServers", {})
    config["mcpServers"]["apiverve"] = {
        "url": SERVER_URL,
        **_auth_headers(api_key),
    }

    _write_json(config_path, config)
    print(f"[ok] Cursor configured - {config_path}")
    return True


def _print_manual_config() -> None:
    print("\nConfigure manually instead:")
    print("")
    print("  VS Code - mcp.json")
    print(f'    {{ "servers": {{ "apiverve": {{ "type": "http", "url": "{SERVER_URL}" }} }} }}')
    print("")
    print("  Cursor - ~/.cursor/mcp.json")
    print(f'    {{ "mcpServers": {{ "apiverve": {{ "url": "{SERVER_URL}" }} }} }}')
    print("")
    print("  Claude Desktop - Settings -> Connectors -> Add custom connector")
    print(f"    {SERVER_URL}")
    print("")


def configure_mcp(target: str = "all", api_key: Optional[str] = None) -> bool:
    """
    Configure an MCP client with the APIVerve server.

    Auth is negotiated, not configured: with no headers the server answers 401 with a
    WWW-Authenticate challenge and the client runs OAuth. Passing api_key skips that for
    headless setups by sending the key directly instead.

    Args:
        target: Which client to configure ("claude", "vscode", "cursor", or "all")
        api_key: Optional API key. Omit to use OAuth.

    Returns:
        bool: True if successful, False otherwise
    """
    print("\nAPIVerve MCP Server Configuration\n")

    # An unrecognised target used to match no branch and report success having done nothing.
    if target not in TARGETS:
        print(f'[error] Unknown target "{target}".')
        print(f"Usage: apiverve-mcp [{'|'.join(TARGETS)}] [--api-key KEY]\n")
        return False

    if api_key:
        print("Using API key auth - the key will be written into the config file.\n")
    else:
        print("Using OAuth - no key is stored; your client will prompt you to sign in.\n")

    try:
        if target in ("claude", "all"):
            configure_claude_desktop()

        if target in ("vscode", "all"):
            configure_vscode(api_key)

        if target in ("cursor", "all"):
            configure_cursor(api_key)

        print("\nDone. Restart your MCP client to pick up the change.")
        print("   Manage access and API keys at https://apiverve.com\n")

        return True
    except Exception as e:
        print(f"\n[error] Configuration failed: {e}")
        _print_manual_config()
        return False
