import http.server
import socketserver
import os

PORT = 3000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif not os.path.exists(self.path.lstrip('/')) and not self.path.endswith('.html'):
            # Try finding a .html file matching the path
            potential_file = self.path.lstrip('/') + '.html'
            if os.path.exists(potential_file):
                self.path = '/' + potential_file
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving frontend at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
