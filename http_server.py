import mimetypes
import socket
import logging
from urllib.parse import urlparse
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

from constants import HTTP_HOST, HTTP_PORT, SOCKET_HOST, SOCKET_PORT

BASE_DIR = Path(__file__).parent


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        router = urlparse(self.path)
        match router.path:
            case "/":
                self._send_html("index.html")
            case "/message":
                self._send_html("message.html")
            case _:
                file = BASE_DIR.joinpath(router.path[1:])
                if file.exists():
                    self._send_static(file)
                else:
                    self._send_html("error.html", 404)

    def do_POST(self):
        size = self.headers.get("Content-Length")
        data = self.rfile.read(int(size)).decode()

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.sendto(data.encode(), (SOCKET_HOST, SOCKET_PORT))

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def _send_html(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(filename, "rb") as f:
            self.wfile.write(f.read())

    def _send_static(self, filename):
        self.send_response(200)
        self.send_header("Content-type", mimetypes.guess_type(filename)[0])
        self.end_headers()

        with open(filename, "rb") as f:
            self.wfile.write(f.read())


def run_http_server():
    try:
        with HTTPServer((HTTP_HOST, HTTP_PORT), MyHandler) as httpd:
            logging.info(f"HTTP server started on {HTTP_HOST}:{HTTP_PORT}")
            httpd.serve_forever()
    except Exception as e:
        logging.error(f"HTTP server error: {e}")

    logging.info("HTTP server stopped")
