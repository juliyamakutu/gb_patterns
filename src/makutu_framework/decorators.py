class Route:
    routes = {}

    def __init__(self, url: str):
        self.url = url

    def __call__(self, cls):
        Route.routes[self.url] = cls()
