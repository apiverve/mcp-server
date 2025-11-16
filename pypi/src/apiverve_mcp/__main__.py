"""
CLI entry point for apiverve-mcp
Usage: python -m apiverve_mcp [claude|vscode|all]
       apiverve-mcp [claude|vscode|all]
"""

import sys
from . import configure_mcp


def main():
    """Main CLI entry point"""
    target = sys.argv[1] if len(sys.argv) > 1 else "claude"
    success = configure_mcp(target)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
