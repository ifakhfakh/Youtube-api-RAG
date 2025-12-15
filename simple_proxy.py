#!/usr/bin/env python3
"""
Simple HTTP/HTTPS proxy server to bypass YouTube IP blocking
Run this in the background: python simple_proxy.py
"""
import http.server
import socketserver
import urllib.request
import urllib.error
import sys
import socket

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle HTTP GET requests"""
        try:
            req = urllib.request.Request(self.path)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                self.send_response(response.status)
                
                for header, value in response.headers.items():
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except Exception as e:
            self.send_error(502, f"Bad Gateway: {e}")
    
    def do_CONNECT(self):
        """Handle HTTPS CONNECT tunneling"""
        try:
            # Parse host and port
            host, port = self.path.split(':')
            port = int(port)
            
            # Create connection to target server
            sock = socket.create_connection((host, port), timeout=10)
            
            # Send 200 Connection established
            self.send_response(200)
            self.end_headers()
            
            # Tunnel data between client and server
            self.tunnel_to_server(sock)
            
        except Exception as e:
            self.send_error(502, f"Bad Gateway: {e}")
    
    def tunnel_to_server(self, sock):
        """Tunnel data between client and remote server"""
        try:
            while True:
                # Read from client
                data = self.rfile.read(4096)
                if not data:
                    break
                sock.sendall(data)
                
                # Read from server
                try:
                    data = sock.recv(4096)
                    if not data:
                        break
                    self.wfile.write(data)
                except socket.timeout:
                    continue
        finally:
            sock.close()
    
    def log_message(self, format, *args):
        print(f"[PROXY] {format % args}")

if __name__ == '__main__':
    port = 8888
    server = http.server.HTTPServer(('0.0.0.0', port), ProxyHandler)
    print(f"✅ Proxy running on http://0.0.0.0:{port}")
    print(f"   HTTP_PROXY=http://127.0.0.1:{port}")
    print(f"   HTTPS_PROXY=http://127.0.0.1:{port}")
    print("\nNote: HTTPS CONNECT tunneling is supported!")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✋ Proxy stopped")
        sys.exit(0)
