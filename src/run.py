from wsgiref.simple_server import make_server

from makutu_framework import Framework
from urls import fronts, routes

PORT = 8080


app = Framework(routes, fronts)

with make_server("", PORT, app) as httpd:
    print(f"Launching on port {PORT}...")
    httpd.serve_forever()
