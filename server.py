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

CARGO_DATA = {
    "cargoData": [
        {"name": "Уголь", "revenue": 420, "share": 35, "color": "#1e3a8a", "icon": "🪨", "trend": "+12%"},
        {"name": "Нефть", "revenue": 300, "share": 25, "color": "#2563eb", "icon": "🛢️", "trend": "+8%"},
        {"name": "Металл", "revenue": 240, "share": 20, "color": "#3b82f6", "icon": "⚙️", "trend": "+5%"},
        {"name": "Контейнеры", "revenue": 180, "share": 15, "color": "#60a5fa", "icon": "📦", "trend": "+18%"},
        {"name": "Прочее", "revenue": 60, "share": 5, "color": "#94a3b8", "icon": "📊", "trend": "-2%"},
    ],
    "companyData": [
        {"name": "РЖД Логистика", "revenue": 350, "growth": "+15%", "color": "#1e3a8a", "marketShare": 29},
        {"name": "СУЭК", "revenue": 280, "growth": "+22%", "color": "#2563eb", "marketShare": 23},
        {"name": "Роснефть", "revenue": 250, "growth": "+10%", "color": "#3b82f6", "marketShare": 21},
        {"name": "НЛМК", "revenue": 200, "growth": "+7%", "color": "#60a5fa", "marketShare": 17},
        {"name": "FESCO", "revenue": 120, "growth": "+25%", "color": "#94a3b8", "marketShare": 10},
    ],
}

RATES_DATA = {
    "coal": {"name": "Уголь", "rate": 1.5},
    "oil": {"name": "Нефть", "rate": 2.2},
    "containers": {"name": "Контейнеры", "rate": 3.5},
    "grain": {"name": "Зерно", "rate": 1.8},
    "metals": {"name": "Металлы", "rate": 2.5},
    "timber": {"name": "Лес", "rate": 1.4},
    "chemicals": {"name": "Химия", "rate": 2.8},
}

STATIONS_DATA = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    "Екатеринбург",
    "Казань",
    "Владивосток",
    "Красноярск",
    "Иркутск",
]

ROUTES_DATA = [
    {"id": 1, "name": "Москва", "x": 420, "y": 320, "region": "Центральный", "cargoTypes": ["coal", "oil", "containers", "metals", "grain"], "population": "12.6M"},
    {"id": 2, "name": "Санкт-Петербург", "x": 380, "y": 220, "region": "Северо-Запад", "cargoTypes": ["containers", "timber", "oil", "metals"], "population": "5.4M"},
    {"id": 3, "name": "Мурманск", "x": 340, "y": 100, "region": "Северо-Запад", "cargoTypes": ["oil", "containers", "metals"], "population": "0.3M"},
    {"id": 4, "name": "Архангельск", "x": 380, "y": 140, "region": "Северо-Запад", "cargoTypes": ["timber", "coal", "containers"], "population": "0.3M"},
    {"id": 5, "name": "Петрозаводск", "x": 370, "y": 180, "region": "Северо-Запад", "cargoTypes": ["timber", "metals"], "population": "0.3M"},
    {"id": 6, "name": "Великий Новгород", "x": 370, "y": 230, "region": "Северо-Запад", "cargoTypes": ["grain", "timber"], "population": "0.2M"},
    {"id": 7, "name": "Псков", "x": 350, "y": 240, "region": "Северо-Запад", "cargoTypes": ["grain", "timber"], "population": "0.2M"},
    {"id": 8, "name": "Калининград", "x": 290, "y": 250, "region": "Северо-Запад", "cargoTypes": ["containers", "oil", "grain"], "population": "0.5M"},
    {"id": 9, "name": "Владимир", "x": 460, "y": 310, "region": "Центральный", "cargoTypes": ["metals", "coal"], "population": "0.3M"},
    {"id": 10, "name": "Нижний Новгород", "x": 540, "y": 300, "region": "Поволжье", "cargoTypes": ["metals", "grain", "coal", "oil"], "population": "1.2M"},
    {"id": 11, "name": "Ярославль", "x": 440, "y": 260, "region": "Центральный", "cargoTypes": ["oil", "metals"], "population": "0.6M"},
    {"id": 12, "name": "Кострома", "x": 460, "y": 250, "region": "Центральный", "cargoTypes": ["timber", "metals"], "population": "0.3M"},
    {"id": 13, "name": "Иваново", "x": 450, "y": 270, "region": "Центральный", "cargoTypes": ["metals", "coal"], "population": "0.4M"},
    {"id": 14, "name": "Тула", "x": 430, "y": 350, "region": "Центральный", "cargoTypes": ["coal", "metals"], "population": "0.5M"},
    {"id": 15, "name": "Рязань", "x": 470, "y": 340, "region": "Центральный", "cargoTypes": ["grain", "oil"], "population": "0.5M"},
    {"id": 16, "name": "Воронеж", "x": 490, "y": 410, "region": "Южный", "cargoTypes": ["grain", "coal", "metals"], "population": "1.0M"},
    {"id": 17, "name": "Белгород", "x": 460, "y": 420, "region": "Южный", "cargoTypes": ["grain", "metals"], "population": "0.4M"},
    {"id": 18, "name": "Курск", "x": 480, "y": 390, "region": "Центральный", "cargoTypes": ["grain", "coal"], "population": "0.4M"},
    {"id": 19, "name": "Казань", "x": 600, "y": 340, "region": "Поволжье", "cargoTypes": ["oil", "grain", "chemicals", "containers"], "population": "1.3M"},
    {"id": 20, "name": "Ульяновск", "x": 620, "y": 370, "region": "Поволжье", "cargoTypes": ["oil", "grain", "metals"], "population": "0.6M"},
    {"id": 21, "name": "Самара", "x": 640, "y": 380, "region": "Поволжье", "cargoTypes": ["oil", "metals", "grain"], "population": "1.1M"},
    {"id": 22, "name": "Саратов", "x": 620, "y": 420, "region": "Поволжье", "cargoTypes": ["grain", "oil", "chemicals"], "population": "0.8M"},
    {"id": 23, "name": "Волгоград", "x": 600, "y": 470, "region": "Южный", "cargoTypes": ["oil", "grain", "metals"], "population": "1.0M"},
    {"id": 24, "name": "Астрахань", "x": 620, "y": 520, "region": "Южный", "cargoTypes": ["oil", "grain"], "population": "0.5M"},
    {"id": 25, "name": "Пенза", "x": 580, "y": 360, "region": "Поволжье", "cargoTypes": ["grain", "metals"], "population": "0.5M"},
    {"id": 26, "name": "Чебоксары", "x": 570, "y": 320, "region": "Поволжье", "cargoTypes": ["chemicals", "grain"], "population": "0.5M"},
    {"id": 27, "name": "Йошкар-Ола", "x": 560, "y": 310, "region": "Поволжье", "cargoTypes": ["timber", "grain"], "population": "0.3M"},
    {"id": 28, "name": "Ростов-на-Дону", "x": 520, "y": 450, "region": "Южный", "cargoTypes": ["grain", "coal", "oil", "containers"], "population": "1.1M"},
    {"id": 29, "name": "Краснодар", "x": 480, "y": 490, "region": "Южный", "cargoTypes": ["grain", "oil", "fertilizers"], "population": "0.9M"},
    {"id": 30, "name": "Сочи", "x": 500, "y": 530, "region": "Южный", "cargoTypes": ["containers", "grain"], "population": "0.4M"},
    {"id": 31, "name": "Ставрополь", "x": 540, "y": 490, "region": "Южный", "cargoTypes": ["grain", "oil"], "population": "0.4M"},
    {"id": 32, "name": "Владикавказ", "x": 560, "y": 530, "region": "Южный", "cargoTypes": ["metals", "grain"], "population": "0.3M"},
    {"id": 33, "name": "Грозный", "x": 580, "y": 540, "region": "Южный", "cargoTypes": ["oil", "grain"], "population": "0.3M"},
    {"id": 34, "name": "Махачкала", "x": 620, "y": 560, "region": "Южный", "cargoTypes": ["oil", "grain"], "population": "0.6M"},
    {"id": 35, "name": "Екатеринбург", "x": 760, "y": 320, "region": "Уральский", "cargoTypes": ["metals", "coal", "chemicals", "containers"], "population": "1.5M"},
    {"id": 36, "name": "Челябинск", "x": 740, "y": 360, "region": "Уральский", "cargoTypes": ["metals", "coal"], "population": "1.2M"},
    {"id": 37, "name": "Уфа", "x": 680, "y": 360, "region": "Поволжье", "cargoTypes": ["oil", "chemicals", "grain"], "population": "1.1M"},
    {"id": 38, "name": "Оренбург", "x": 700, "y": 420, "region": "Поволжье", "cargoTypes": ["oil", "grain"], "population": "0.6M"},
    {"id": 39, "name": "Пермь", "x": 680, "y": 290, "region": "Поволжье", "cargoTypes": ["oil", "timber", "metals"], "population": "1.0M"},
    {"id": 40, "name": "Тюмень", "x": 800, "y": 270, "region": "Уральский", "cargoTypes": ["oil", "gas", "metals"], "population": "0.8M"},
    {"id": 41, "name": "Сургут", "x": 780, "y": 200, "region": "Уральский", "cargoTypes": ["oil", "gas"], "population": "0.4M"},
    {"id": 42, "name": "Нижневартовск", "x": 800, "y": 220, "region": "Уральский", "cargoTypes": ["oil", "gas"], "population": "0.3M"},
    {"id": 43, "name": "Курган", "x": 780, "y": 360, "region": "Уральский", "cargoTypes": ["metals", "grain"], "population": "0.3M"},
    {"id": 44, "name": "Магнитогорск", "x": 720, "y": 380, "region": "Уральский", "cargoTypes": ["metals", "coal"], "population": "0.4M"},
    {"id": 45, "name": "Омск", "x": 880, "y": 340, "region": "Сибирский", "cargoTypes": ["oil", "grain", "chemicals"], "population": "1.1M"},
    {"id": 46, "name": "Новосибирск", "x": 960, "y": 330, "region": "Сибирский", "cargoTypes": ["coal", "grain", "metals", "containers"], "population": "1.6M"},
    {"id": 47, "name": "Томск", "x": 920, "y": 300, "region": "Сибирский", "cargoTypes": ["oil", "timber", "metals"], "population": "0.6M"},
    {"id": 48, "name": "Кемерово", "x": 990, "y": 340, "region": "Сибирский", "cargoTypes": ["coal", "metals"], "population": "0.5M"},
    {"id": 49, "name": "Новокузнецк", "x": 1010, "y": 360, "region": "Сибирский", "cargoTypes": ["coal", "metals"], "population": "0.5M"},
    {"id": 50, "name": "Красноярск", "x": 1100, "y": 340, "region": "Сибирский", "cargoTypes": ["coal", "metals", "timber", "aluminum"], "population": "1.1M"},
    {"id": 51, "name": "Иркутск", "x": 1200, "y": 360, "region": "Сибирский", "cargoTypes": ["coal", "timber", "containers"], "population": "0.6M"},
    {"id": 52, "name": "Улан-Удэ", "x": 1240, "y": 380, "region": "Сибирский", "cargoTypes": ["coal", "timber"], "population": "0.4M"},
    {"id": 53, "name": "Чита", "x": 1300, "y": 380, "region": "Сибирский", "cargoTypes": ["coal", "timber", "metals"], "population": "0.3M"},
    {"id": 54, "name": "Абакан", "x": 1070, "y": 380, "region": "Сибирский", "cargoTypes": ["coal", "metals"], "population": "0.2M"},
    {"id": 55, "name": "Кызыл", "x": 1110, "y": 420, "region": "Сибирский", "cargoTypes": ["coal", "timber"], "population": "0.1M"},
    {"id": 56, "name": "Владивосток", "x": 1420, "y": 420, "region": "Дальневосточный", "cargoTypes": ["containers", "oil", "timber", "fish"], "population": "0.6M"},
    {"id": 57, "name": "Хабаровск", "x": 1380, "y": 380, "region": "Дальневосточный", "cargoTypes": ["timber", "containers", "metals"], "population": "0.6M"},
    {"id": 58, "name": "Благовещенск", "x": 1320, "y": 360, "region": "Дальневосточный", "cargoTypes": ["grain", "timber", "metals"], "population": "0.2M"},
    {"id": 59, "name": "Комсомольск-на-Амуре", "x": 1360, "y": 340, "region": "Дальневосточный", "cargoTypes": ["metals", "timber", "oil"], "population": "0.2M"},
    {"id": 60, "name": "Южно-Сахалинск", "x": 1520, "y": 480, "region": "Дальневосточный", "cargoTypes": ["oil", "gas", "fish", "coal"], "population": "0.2M"},
    {"id": 61, "name": "Петропавловск-Камчатский", "x": 1600, "y": 440, "region": "Дальневосточный", "cargoTypes": ["fish", "containers"], "population": "0.2M"},
    {"id": 62, "name": "Магадан", "x": 1480, "y": 320, "region": "Дальневосточный", "cargoTypes": ["gold", "coal", "fish"], "population": "0.1M"},
    {"id": 63, "name": "Якутск", "x": 1220, "y": 240, "region": "Дальневосточный", "cargoTypes": ["diamonds", "coal", "timber", "gold"], "population": "0.3M"},
    {"id": 64, "name": "Уссурийск", "x": 1410, "y": 410, "region": "Дальневосточный", "cargoTypes": ["grain", "containers"], "population": "0.2M"},
    {"id": 65, "name": "Находка", "x": 1440, "y": 440, "region": "Дальневосточный", "cargoTypes": ["containers", "oil", "coal"], "population": "0.1M"},
]

EDGES_DATA = [
    {"id": 1, "from": 1, "to": 10, "distance": 400, "capacity": 150, "type": "main"},
    {"id": 2, "from": 10, "to": 19, "distance": 380, "capacity": 140, "type": "main"},
    {"id": 3, "from": 19, "to": 35, "distance": 650, "capacity": 160, "type": "main"},
    {"id": 4, "from": 35, "to": 46, "distance": 1600, "capacity": 180, "type": "main"},
    {"id": 5, "from": 46, "to": 50, "distance": 800, "capacity": 150, "type": "main"},
    {"id": 6, "from": 50, "to": 51, "distance": 1100, "capacity": 140, "type": "main"},
    {"id": 7, "from": 51, "to": 57, "distance": 1200, "capacity": 120, "type": "main"},
    {"id": 8, "from": 57, "to": 56, "distance": 800, "capacity": 130, "type": "main"},
    {"id": 9, "from": 1, "to": 2, "distance": 650, "capacity": 120, "type": "main"},
    {"id": 10, "from": 1, "to": 9, "distance": 180, "capacity": 100, "type": "regional"},
    {"id": 11, "from": 1, "to": 11, "distance": 250, "capacity": 90, "type": "regional"},
    {"id": 12, "from": 1, "to": 14, "distance": 180, "capacity": 110, "type": "regional"},
    {"id": 13, "from": 1, "to": 15, "distance": 190, "capacity": 95, "type": "regional"},
    {"id": 14, "from": 1, "to": 16, "distance": 470, "capacity": 100, "type": "regional"},
    {"id": 15, "from": 2, "to": 3, "distance": 1100, "capacity": 80, "type": "regional"},
    {"id": 16, "from": 2, "to": 4, "distance": 350, "capacity": 70, "type": "regional"},
    {"id": 17, "from": 2, "to": 5, "distance": 250, "capacity": 60, "type": "regional"},
    {"id": 18, "from": 2, "to": 8, "distance": 400, "capacity": 75, "type": "regional"},
    {"id": 19, "from": 10, "to": 21, "distance": 420, "capacity": 110, "type": "main"},
    {"id": 20, "from": 19, "to": 21, "distance": 370, "capacity": 100, "type": "regional"},
    {"id": 21, "from": 21, "to": 22, "distance": 320, "capacity": 95, "type": "regional"},
    {"id": 22, "from": 22, "to": 23, "distance": 420, "capacity": 100, "type": "main"},
    {"id": 23, "from": 23, "to": 24, "distance": 400, "capacity": 85, "type": "regional"},
    {"id": 24, "from": 19, "to": 37, "distance": 450, "capacity": 105, "type": "main"},
    {"id": 25, "from": 16, "to": 28, "distance": 460, "capacity": 120, "type": "main"},
    {"id": 26, "from": 28, "to": 29, "distance": 270, "capacity": 90, "type": "regional"},
    {"id": 27, "from": 28, "to": 31, "distance": 250, "capacity": 80, "type": "regional"},
    {"id": 28, "from": 29, "to": 30, "distance": 280, "capacity": 70, "type": "regional"},
    {"id": 29, "from": 23, "to": 28, "distance": 460, "capacity": 110, "type": "main"},
    {"id": 30, "from": 35, "to": 36, "distance": 250, "capacity": 130, "type": "main"},
    {"id": 31, "from": 35, "to": 39, "distance": 450, "capacity": 100, "type": "regional"},
    {"id": 32, "from": 35, "to": 40, "distance": 330, "capacity": 110, "type": "main"},
    {"id": 33, "from": 40, "to": 41, "distance": 420, "capacity": 90, "type": "regional"},
    {"id": 34, "from": 36, "to": 44, "distance": 220, "capacity": 120, "type": "regional"},
    {"id": 35, "from": 37, "to": 38, "distance": 320, "capacity": 85, "type": "regional"},
    {"id": 36, "from": 40, "to": 45, "distance": 570, "capacity": 100, "type": "main"},
    {"id": 37, "from": 45, "to": 46, "distance": 650, "capacity": 120, "type": "main"},
    {"id": 38, "from": 46, "to": 47, "distance": 240, "capacity": 80, "type": "regional"},
    {"id": 39, "from": 46, "to": 48, "distance": 260, "capacity": 110, "type": "regional"},
    {"id": 40, "from": 48, "to": 49, "distance": 200, "capacity": 130, "type": "regional"},
    {"id": 41, "from": 50, "to": 54, "distance": 380, "capacity": 90, "type": "regional"},
    {"id": 42, "from": 51, "to": 52, "distance": 280, "capacity": 75, "type": "regional"},
    {"id": 43, "from": 52, "to": 53, "distance": 450, "capacity": 70, "type": "regional"},
    {"id": 44, "from": 53, "to": 58, "distance": 650, "capacity": 65, "type": "regional"},
    {"id": 45, "from": 56, "to": 64, "distance": 100, "capacity": 60, "type": "regional"},
    {"id": 46, "from": 56, "to": 65, "distance": 170, "capacity": 80, "type": "regional"},
    {"id": 47, "from": 57, "to": 59, "distance": 360, "capacity": 70, "type": "regional"},
    {"id": 48, "from": 56, "to": 60, "distance": 850, "capacity": 50, "type": "regional"},
    {"id": 49, "from": 1, "to": 13, "distance": 300, "capacity": 80, "type": "regional"},
    {"id": 50, "from": 11, "to": 12, "distance": 120, "capacity": 60, "type": "regional"},
    {"id": 51, "from": 10, "to": 25, "distance": 240, "capacity": 75, "type": "regional"},
    {"id": 52, "from": 21, "to": 25, "distance": 280, "capacity": 70, "type": "regional"},
    {"id": 53, "from": 35, "to": 43, "distance": 320, "capacity": 65, "type": "regional"},
    {"id": 54, "from": 45, "to": 42, "distance": 450, "capacity": 60, "type": "regional"},
]


class RequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        routes = {
            "/revenues": REVENUES_DATA,
            "/prediction": PREDICTION_DATA,
            "/cargo": CARGO_DATA,
            "/rates": RATES_DATA,
            "/stations": STATIONS_DATA,
            "/routes": ROUTES_DATA,
            "/edges": EDGES_DATA,
        }

        if self.path not in routes:
            self.send_response(404)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))
            return

        response = json.dumps(routes[self.path]).encode("utf-8")
        self.send_response(200)
        self._set_cors_headers()
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
