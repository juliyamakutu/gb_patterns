from wsgiref.simple_server import make_server

from makutu_framework import Framework, Route
from urls import fronts

PORT = 8080

print(Route.routes)

app = Framework(Route.routes, fronts)

with make_server("", PORT, app) as httpd:
    print(f"Launching on port {PORT}...")
    httpd.serve_forever()
