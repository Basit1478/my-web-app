from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class WebAppHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the main page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Simple Web App</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    .nav {
                        background: #f0f0f0;
                        padding: 10px;
                        margin-bottom: 20px;
                    }
                    .nav a {
                        margin-right: 10px;
                        text-decoration: none;
                        color: #333;
                    }
                    #message {
                        color: green;
                    }
                </style>
            </head>
            <body>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/about">About</a>
                </div>
                <h1>Welcome to My Web App</h1>
                <p>This is a simple web app with no external dependencies!</p>
                <form id="messageForm">
                    <input type="text" id="nameInput" placeholder="Enter your name">
                    <button type="submit">Submit</button>
                </form>
                <p id="message"></p>

                <script>
                    document.getElementById('messageForm').onsubmit = function(e) {
                        e.preventDefault();
                        const name = document.getElementById('nameInput').value;
                        fetch('/greet', {
                            method: 'POST',
                            body: JSON.stringify({name: name})
                        })
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('message').textContent = data.message;
                        });
                    };
                </script>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
            
        elif self.path == '/about':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            about_html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>About - Simple Web App</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    .nav {
                        background: #f0f0f0;
                        padding: 10px;
                        margin-bottom: 20px;
                    }
                    .nav a {
                        margin-right: 10px;
                        text-decoration: none;
                        color: #333;
                    }
                </style>
            </head>
            <body>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/about">About</a>
                </div>
                <h1>About</h1>
                <p>This is a simple web application built using Python's built-in http.server module.</p>
            </body>
            </html>
            '''
            self.wfile.write(about_html.encode())

    def do_POST(self):
        if self.path == '/greet':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            response_data = {'message': f"Hello, {data['name']}!"}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebAppHandler)
    print(f"Server running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 