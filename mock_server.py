#!/usr/bin/env python3
"""
Mock Backend Server for VideoClipper Reconstructed Web App
Provides static file serving + mock API endpoints (/api/credits, /api/submit, /api/progress, /api/cancel)
"""

import http.server
import socketserver
import json
import time
import uuid
import os
import sys

PORT = 8080

class VideoClipperHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Client-FP, Accept')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Mock credits endpoint
        if self.path.startswith('/api/credits'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = {
                "credits_left": 15.00,
                "reset_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 86400))
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        # Mock SSE progress endpoint
        if self.path.startswith('/api/progress/'):
            process_id = self.path.split('/api/progress/')[-1].split('?')[0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()

            try:
                # Simulate progress from 10% to 100%
                for p in [15, 35, 60, 85, 100]:
                    msg = f"event: progress\ndata: {json.dumps({'progress': str(p)})}\n\n"
                    self.wfile.write(msg.encode('utf-8'))
                    self.wfile.flush()
                    time.sleep(0.8)

                # Complete event
                complete_data = {
                    "downloadUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                    "filename": f"clip_{process_id[:8]}.mp4"
                }
                msg = f"event: complete\ndata: {json.dumps(complete_data)}\n\n"
                self.wfile.write(msg.encode('utf-8'))
                self.wfile.flush()
            except BrokenPipeError:
                pass
            return

        # Mock cancel endpoint
        if self.path.startswith('/api/cancel/'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "cancelled"}).encode('utf-8'))
            return

        # URL rewrite for clean routes
        if self.path == '/gif' or self.path == '/gif/':
            self.path = '/gif.html'
        elif self.path == '/supported-sites' or self.path == '/supported-sites/':
            self.path = '/supported-sites.html'
        elif self.path == '/faq' or self.path == '/faq/':
            self.path = '/faq.html'
        elif self.path == '/contact' or self.path == '/contact/':
            self.path = '/contact.html'
        elif self.path == '/terms' or self.path == '/terms/':
            self.path = '/terms.html'
        elif self.path == '/privacy' or self.path == '/privacy/':
            self.path = '/privacy.html'

        # Default static file handler
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        if self.path in ['/api/submit', '/api/gif/submit']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            proc_id = str(uuid.uuid4())
            response_data = {"processId": proc_id}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), VideoClipperHandler) as httpd:
        print(f"VideoClipper mock server running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
