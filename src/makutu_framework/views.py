"""Default framework views"""


class PageNotFound404:
    """404 Not Found view"""

    def __call__(self, request):
        return "404 NOT FOUND", "Page Not Found"
