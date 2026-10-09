import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket


APP_NAME = os.environ.get("APP_NAME", "demo-service")
VERSION = os.environ.get("VERSION", "1.0.0")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return

        if self.path == "/":
            payload = {
                "app": os.environ.get("APP_NAME", APP_NAME),
                "version": os.environ.get("VERSION", VERSION),
                "pod": socket.gethostname(),
            }
            body = json.dumps(payload).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404, "Not Found")

    def log_message(self, format_string, *args):
        print("%s - %s" % (self.address_string(), format_string % args))


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8080), RequestHandler)
    print("Starting HTTP server on port 8080", flush=True)
    server.serve_forever()
