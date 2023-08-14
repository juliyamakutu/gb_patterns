from wsgiref.simple_server import make_server

from makutu_framework import Framework
from urls import fronts
from views import engine

PORT = 8080

print(engine.routes)

app = Framework(engine.routes, fronts)

with make_server("", PORT, app) as httpd:
    print(f"Launching on port {PORT}...")
    httpd.serve_forever()
