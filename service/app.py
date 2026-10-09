import json
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket


CONFIG_DIR = Path("/etc/enterprise-bot/config")


def get_config(key, default):
    """Read projected ConfigMap files, falling back to environment variables."""
    config_file = CONFIG_DIR / key

    try:
        if config_file.is_file():
            return config_file.read_text().strip()
    except OSError:
        pass

    return os.environ.get(key, default)


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
                "app": get_config("APP_NAME", "demo-service"),
                "version": get_config("VERSION", "1.0.0"),
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
