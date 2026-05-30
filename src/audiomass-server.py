import functools
import http.server
import mimetypes
import socketserver
from pathlib import Path

PORT = 5055
HOST = "127.0.0.1"
ROOT = Path(__file__).resolve().parent

mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("font/woff", ".woff")
mimetypes.add_type("font/ttf", ".ttf")
mimetypes.add_type("image/svg+xml", ".svg")


class AudioMassHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        if self.path.endswith((".js", ".css", ".html", ".woff", ".ttf", ".svg")):
            self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()


class ReusableThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


Handler = functools.partial(AudioMassHandler, directory=str(ROOT))

with ReusableThreadingTCPServer((HOST, PORT), Handler) as httpd:
    print(f"Serving AudioMass from {ROOT}")
    print(f"Open http://{HOST}:{PORT}/")
    httpd.serve_forever()
