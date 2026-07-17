"""
CLI entry point for apiverve-mcp
Usage: python -m apiverve_mcp [claude|vscode|cursor|all] [--api-key KEY]
       apiverve-mcp [claude|vscode|cursor|all] [--api-key KEY]

Omit --api-key to authenticate via OAuth (nothing is stored on disk).
"""

import sys
from . import configure_mcp


def _parse_args(argv):
    target, api_key = "all", None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--api-key":
            i += 1
            api_key = argv[i] if i < len(argv) else None
        elif arg.startswith("--api-key="):
            api_key = arg[len("--api-key="):]
        elif not arg.startswith("-"):
            target = arg
        i += 1
    return target, api_key


def main():
    """Main CLI entry point"""
    target, api_key = _parse_args(sys.argv[1:])
    success = configure_mcp(target, api_key)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
