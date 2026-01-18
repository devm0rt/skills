#!/usr/bin/env python3
"""
Start one or more servers, wait for them to be ready, run a command, then clean up.

Usage:
    # Single server
    python scripts/with_server.py --server "npm run dev" --port 5173 -- python automation.py
    python scripts/with_server.py --server "npm start" --port 3000 -- python test.py

    # With working directory
    python scripts/with_server.py --server "python server.py" --port 3000 --cwd backend -- python test.py

    # Multiple servers
    python scripts/with_server.py \
      --server "python server.py" --port 3000 --cwd backend \
      --server "npm run dev" --port 5173 --cwd frontend \
      -- python test.py
"""

import subprocess
import socket
import time
import sys
import argparse
import shlex
import os

def is_server_ready(port, timeout=30):
    """Wait for server to be ready by polling the port."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def main():
    parser = argparse.ArgumentParser(description='Run command with one or more servers')
    parser.add_argument('--server', action='append', dest='servers', required=True, help='Server command (can be repeated)')
    parser.add_argument('--port', action='append', dest='ports', type=int, required=True, help='Port for each server (must match --server count)')
    parser.add_argument('--cwd', action='append', dest='cwds', help='Working directory for each server (optional, use "" to skip)')
    parser.add_argument('--timeout', type=int, default=30, help='Timeout in seconds per server (default: 30)')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Command to run after server(s) ready')

    args = parser.parse_args()

    # Remove the '--' separator if present
    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print("Error: No command specified to run")
        sys.exit(1)

    # Parse server configurations
    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port arguments must match")
        sys.exit(1)

    # Handle optional --cwd arguments
    cwds = args.cwds or []
    while len(cwds) < len(args.servers):
        cwds.append(None)

    servers = []
    for cmd, port, cwd in zip(args.servers, args.ports, cwds):
        # Resolve cwd to absolute path if provided
        resolved_cwd = None
        if cwd and cwd.strip():
            resolved_cwd = os.path.abspath(cwd)
            if not os.path.isdir(resolved_cwd):
                print(f"Error: Working directory does not exist: {cwd}")
                sys.exit(1)
        servers.append({'cmd': cmd, 'port': port, 'cwd': resolved_cwd})

    server_processes = []

    try:
        # Start all servers
        for i, server in enumerate(servers):
            cwd_msg = f" (cwd: {server['cwd']})" if server['cwd'] else ""
            print(f"Starting server {i+1}/{len(servers)}: {server['cmd']}{cwd_msg}")

            process = subprocess.Popen(
                shlex.split(server['cmd']),
                cwd=server['cwd'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            server_processes.append(process)

            # Wait for this server to be ready
            print(f"Waiting for server on port {server['port']}...")
            if not is_server_ready(server['port'], timeout=args.timeout):
                raise RuntimeError(f"Server failed to start on port {server['port']} within {args.timeout}s")

            print(f"Server ready on port {server['port']}")

        print(f"\nAll {len(servers)} server(s) ready")

        # Run the command
        print(f"Running: {' '.join(args.command)}\n")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)

    finally:
        # Clean up all servers
        print(f"\nStopping {len(server_processes)} server(s)...")
        for i, process in enumerate(server_processes):
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            print(f"Server {i+1} stopped")
        print("All servers stopped")


if __name__ == '__main__':
    main()