import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept, Origin')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

# Change to the directory where your HTML and JS files are located
# This assumes server.py is in the same directory as index.html and script.js
os.chdir(os.path.dirname(os.path.abspath(__file__)))

handler = MyHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"serving at port {PORT}")
    print(f"You can access the application at http://localhost:{PORT}/")
    
    # Open the browser automatically
    webbrowser.open_new_tab(f"http://localhost:{PORT}/")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.shutdown()
