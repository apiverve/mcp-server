"""
CLI entry point for apiverve-mcp
Usage: python -m apiverve_mcp [claude|vscode|cursor|all] [--api-key KEY]
       apiverve-mcp [claude|vscode|cursor|all] [--api-key KEY]

Omit --api-key to authenticate via OAuth (nothing is stored on disk).
"""

import sys
from . import SERVER_URL, TARGETS, configure_mcp

USAGE = f"Usage: apiverve-mcp [{'|'.join(TARGETS)}] [--api-key KEY]"


def _parse_args(argv):
    target, api_key, help_, unknown = "all", None, False, None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("-h", "--help"):
            help_ = True
        elif arg == "--api-key":
            i += 1
            api_key = argv[i] if i < len(argv) else None
        elif arg.startswith("--api-key="):
            api_key = arg[len("--api-key="):]
        elif arg.startswith("-"):
            unknown = unknown or arg
        else:
            target = arg
        i += 1
    return target, api_key, help_, unknown


def main():
    """Main CLI entry point"""
    target, api_key, help_, unknown = _parse_args(sys.argv[1:])
    # Without this, --help fell through to the default target and wrote every client's config.
    if help_:
        print(f"{USAGE}\n\nAdds the APIVerve MCP server ({SERVER_URL}) to Claude Desktop, VS Code and Cursor.")
        print("Omit --api-key to sign in with OAuth; nothing is stored on disk.")
        sys.exit(0)
    if unknown:
        print(f'Unknown option "{unknown}".\n{USAGE}', file=sys.stderr)
        sys.exit(1)
    success = configure_mcp(target, api_key)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
