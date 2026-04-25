import json
from http.server import BaseHTTPRequestHandler, HTTPServer


REVENUES_DATA = {
    "years": [2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036],
    "revenues": [980, 1050, 1120, 1180, 1240, 1290, 1330, 1360, 1380, 1395, 1400],
}

PREDICTION_DATA = {
    "baseData": {
        "years": [2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036],
        "cargo": [145, 152, 158, 165, 171, 178, 185, 191, 198, 205, 212],
        "distance": [1250, 1280, 1310, 1340, 1370, 1400, 1430, 1460, 1490, 1520, 1550],
        "accuracy": [95.0, 94.2, 93.5, 92.8, 92.0, 91.3, 90.5, 89.8, 89.0, 88.3, 87.5],
    },
    "cargoMultipliers": {
        "all": {"cargo": 1.00, "distance": 1.00, "accuracy": 1.00},
        "coal": {"cargo": 0.35, "distance": 0.85, "accuracy": 1.05},
        "oil": {"cargo": 0.28, "distance": 1.20, "accuracy": 1.02},
        "ore": {"cargo": 0.18, "distance": 0.70, "accuracy": 0.98},
        "construction": {"cargo": 0.12, "distance": 0.60, "accuracy": 0.95},
    },
}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/revenues": REVENUES_DATA,
            "/prediction": PREDICTION_DATA,
        }

        if self.path not in routes:
            self.send_response(404)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))
            return

        response = json.dumps(routes[self.path]).encode("utf-8")
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
