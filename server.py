import json
from http.server import BaseHTTPRequestHandler, HTTPServer


DATA = {
    "years": [2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036],
    "revenues": [980, 1050, 1120, 1180, 1240, 1290, 1330, 1360, 1380, 1395, 1400],
}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/revenues":
            self.send_response(404)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))
            return

        response = json.dumps(DATA).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        return


def run():
    server = HTTPServer(("0.0.0.0", 8000), RequestHandler)
    print("Server started on http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
