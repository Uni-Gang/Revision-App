# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""Serve the OS revision app on the local network.

Usage:  uv run serve.py [port]   (or: python serve.py [port])
Then open the printed http://<your-ip>:<port>/ on any device on the same Wi-Fi.
"""
import http.server
import os
import socket
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # no packets sent; just picks the outbound interface
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


handler = http.server.SimpleHTTPRequestHandler
with http.server.ThreadingHTTPServer(("0.0.0.0", PORT), handler) as httpd:
    print(f"OS revision app running:")
    print(f"  this PC:      http://localhost:{PORT}/")
    print(f"  other devices: http://{lan_ip()}:{PORT}/")
    print("Ctrl+C to stop. (If other devices can't connect, allow Python through Windows Firewall on Private networks.)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
