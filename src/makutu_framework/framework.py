from typing import Any, Callable, Dict, List
from urllib.parse import unquote

from .utils import get_path_to_file
from .views import PageNotFound404


class Framework:
    """Main class of the framework"""

    def __init__(self, routes: Dict[str, object], fronts: List[Callable]):
        self.routes = routes
        self.fronts = fronts

    @staticmethod
    def _return_static(path: str, start_response: Callable) -> List[bytes]:
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

    @staticmethod
    def _decode_value(value: str) -> str:
        """Decodes value"""
        return unquote(value).replace("+", " ")

    def _parse_input_data(self, input_data: str) -> Dict[str, str]:
        """Slits input data to dict"""
        result = {}
        if input_data:
            params = input_data.split("&")
            for item in params:
                k, v = item.split("=")
                result[k] = self._decode_value(v)
        return result

    def _get_request_params(self, environ: Dict[str, Any]) -> Dict[str, str]:
        """Get query string"""
        query_string = environ["QUERY_STRING"]
        return self._parse_input_data(query_string)

    def _get_post_data(self, environ: Dict[str, Any]) -> Dict[str, str]:
        """Get POST data"""
        raw_content_length = environ.get("CONTENT_LENGTH")
        content_length = int(raw_content_length) if raw_content_length else 0

        data = environ["wsgi.input"].read(content_length) if content_length else None

        if not data:
            return {}

        return self._parse_input_data(data.decode(encoding="utf-8"))

    def __call__(
        self, environ: Dict[Any, Any], start_response: Callable
    ) -> List[bytes]:
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
        method = environ["REQUEST_METHOD"]
        request["method"] = method

        if method == "POST":
            request["data"] = self._get_post_data(environ)
        if method == "GET":
            request["request_params"] = self._get_request_params(environ)

        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])

        return [body.encode("utf-8")]
