#!/usr/bin/env python3
"""Backend startup script."""

import uvicorn
import os
import sys
import argparse
from pathlib import Path

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Start KERAG Web Backend Server")
    parser.add_argument(
        "--global-root",
        type=str,
        help="Global knowledge base root path (default: KERAG_HOME env or example directory)"
    )
    parser.add_argument(
        "--local-root",
        type=str,
        help="Local knowledge base root path (optional)"
    )
    parser.add_argument(
        "--lang",
        type=str,
        help="The language perference of the knowledge base (optional)"
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Server port (default: KERAG_PORT env or 8001)"
    )

    args = parser.parse_args()

    # Set default paths relative to this script
    backend_dir = Path(__file__).parent

    # Determine global root from args, env, or default
    if args.global_root:
        global_root = args.global_root
        # Set environment variables
        os.environ["KERAG_HOME"] = global_root

    if args.local_root:
        os.environ["KERAG_LOCAL"] = args.local_root
    if args.lang:
        os.environ["KERAG_LANG"] = args.lang

    # Determine port from args, env, or default
    if args.port:
        port = args.port
    else:
        port = int(os.getenv("KERAG_PORT", "8001"))

    print(f"Starting KERAG Web API...")
    print(f"Port: {port}")
    if args.local_root:
        print(f"Local root: {args.local_root}")

    # Determine if running from installed package or source
    try:
        import kerag_web
        app_module = "kerag_web.app.main:app"
    except ImportError:
        # If not installed, add parent to path to support running from source
        import sys
        sys.path.insert(0, str(backend_dir.parent))
        app_module = "app.main:app"

    uvicorn.run(
        app_module,
        host="localhost",
        port=port,
        reload=False,  # Disable reload for production packaging
        log_level="info"
    )

if __name__ == "__main__":
    main()
