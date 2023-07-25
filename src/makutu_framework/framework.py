from typing import Any, Callable

from .utils import get_path_to_file
from .views import PageNotFound404


class Framework:
    """Main class of the framework"""

    def __init__(self, routes: dict[str, object], fronts: list[Callable]):
        self.routes = routes
        self.fronts = fronts

    @staticmethod
    def _return_static(path: str, start_response: Callable) -> list[bytes]:
        """Returns static file"""
        with open(get_path_to_file(path), "rb") as file:
            content = file.read()

        if path.endswith(".css"):
            content_type = "text/css"
        elif path.endswith(".js"):
            content_type = "text/javascript"
        elif path.endswith(".jpg"):
            content_type = "image/jpeg"
        elif path.endswith(".png"):
            content_type = "image/png"
        elif path.endswith(".html"):
            content_type = "text/html"
        else:
            content_type = "text/plain"

        start_response("200 OK", [("Content-Type", content_type)])
        return [content]

    def __call__(
        self, environ: dict[Any, Any], start_response: Callable
    ) -> list[bytes]:
        path = environ["PATH_INFO"]

        if path.startswith("/static/"):
            return self._return_static(path, start_response=start_response)

        if not path.endswith("/"):
            path = f"{path}/"

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        request = {}
        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])

        return [body.encode("utf-8")]
