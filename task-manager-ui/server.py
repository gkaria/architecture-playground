"""Simple HTTP server for Task Manager UI."""

import http.server
import socketserver
import os

# Configuration
PORT = 9000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with CORS support."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests."""
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[Task Manager UI] {self.address_string()} - {format % args}")


def main():
    """Start the HTTP server."""
    os.chdir(DIRECTORY)

    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print("=" * 60)
        print("🎨 Task Manager UI Server")
        print("=" * 60)
        print(f"📂 Serving from: {DIRECTORY}")
        print(f"🌐 URL: http://localhost:{PORT}")
        print()
        print("📋 Quick Links:")
        print(f"   • Task Manager UI: http://localhost:{PORT}")
        print(f"   • Monolith API:    http://localhost:8001/docs")
        print()
        print("💡 Tips:")
        print("   1. Make sure a backend API is running (e.g., monolith on port 8001)")
        print("   2. Use the dropdown to switch between architectures")
        print("   3. Watch the response time metrics in the header")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")


if __name__ == "__main__":
    main()
