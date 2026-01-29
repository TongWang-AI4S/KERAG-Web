#!/usr/bin/env python3
"""KERAG Web One-Click Launcher."""

import subprocess
import sys
import os
import time
import argparse
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a shell command and return the process."""
    return subprocess.Popen(command, cwd=cwd, shell=shell)

def main():
    parser = argparse.ArgumentParser(description="KERAG Web One-Click Launcher")
    parser.add_argument("--dev", action="store_true", help="Run in development mode (with hot reload)")
    parser.add_argument("--build", action="store_true", help="Build frontend before starting")
    parser.add_argument("--port", type=int, default=8001, help="Backend port (default: 8001)")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    backend_dir = base_dir / "backend"
    frontend_dir = base_dir / "frontend"

    processes = []

    try:
        # 1. Start Backend
        print(f"[*] Starting Backend API on port {args.port}...")
        env = os.environ.copy()
        env["KERAG_PORT"] = str(args.port)

        # Use python -m uvicorn or just python start.py
        backend_proc = run_command(
            [sys.executable, "start.py", "--port", str(args.port)],
            cwd=backend_dir
        )
        processes.append(backend_proc)

        # 2. Handle Frontend
        if args.dev:
            print("[*] Starting Frontend Development Server (Vite)...")
            if not (frontend_dir / "node_modules").exists():
                print("[!] node_modules not found, running npm install...")
                subprocess.run("npm install", cwd=frontend_dir, shell=True)

            frontend_proc = run_command("npm run dev", cwd=frontend_dir)
            processes.append(frontend_proc)
        else:
            dist_dir = frontend_dir / "dist"
            if args.build or not dist_dir.exists():
                print("[*] Building Frontend...")
                if not (frontend_dir / "node_modules").exists():
                    subprocess.run("npm install", cwd=frontend_dir, shell=True)
                subprocess.run("npm run build", cwd=frontend_dir, shell=True)

            print(f"[*] Frontend is ready. Access it at http://localhost:{args.port}")

        # Keep the script running
        while True:
            time.sleep(1)
            for p in processes:
                if p.poll() is not None:
                    print(f"[!] Process {p.pid} terminated unexpectedly.")
                    return

    except KeyboardInterrupt:
        print("\n[!] Stopping all services...")
    finally:
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()
