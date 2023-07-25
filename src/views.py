from makutu_framework import render


class Index:
    def __call__(self, request):
        return "200 OK", render(
            "index.html", objects_list=request.get("objects_list", None)
        )


class Contacts:
    def __call__(self, request):
        return "200 OK", render("contact.html")
