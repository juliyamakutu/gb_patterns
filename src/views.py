from engine import Engine
from makutu_framework import render

engine = Engine()


class Index:
    def __call__(self, request):
        return "200 OK", render("index.html")


class Contacts:
    def __call__(self, request):
        if request["method"] == "POST":
            print(request["data"])
        if request["method"] == "GET":
            print(request["request_params"])
        return "200 OK", render("contact.html")


class CoursesList:
    def __call__(self, request):
        category = engine.get_category(request.get("request_params", {}).get("id"))
        if category:
            return "200 OK", render(
                "course_list.html",
                objects_list=category.courses,
                name=category.name,
                id=category.id,
            )
        return "200 OK", "No courses found"


class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request["method"] == "POST":
            data = request["data"]

            name = data["name"]
            name = engine.decode_value(name)

            category = None
            if self.category_id != -1:
                category = engine.get_category(int(self.category_id))

                course = engine.create_course("record", name, category)
                engine.courses.append(course)

            return "200 OK", render(
                "course_list.html",
                objects_list=category.courses if category else None,
                name=category.name if category else None,
                id=category.id if category else None,
            )

        else:
            raw_category_id = request.get("request_params", {}).get("id")
            if raw_category_id:
                category_id = int(raw_category_id)
            else:
                category_id = None
            if category_id:
                self.category_id = category_id
                category = engine.get_category(int(self.category_id))
                if category:
                    return "200 OK", render(
                        "create_course.html", name=category.name, id=category.id
                    )
        return "200 OK", "No categories found"


class CreateCategory:
    def __call__(self, request):
        if request["method"] == "POST":
            data = request["data"]

            name = data["name"]
            name = engine.decode_value(name)

            category_id = data.get("category_id")

            category = None
            if category_id:
                category = engine.get_category(int(category_id))

            new_category = engine.create_category(name, category)

            engine.categories.append(new_category)

            return "200 OK", render("index.html", objects_list=engine.categories)
        else:
            categories = engine.categories
            return "200 OK", render("create_category.html", categories=categories)


class CategoryList:
    def __call__(self, request):
        return "200 OK", render("category_list.html", objects_list=engine.categories)


class CopyCourse:
    def __call__(self, request):
        name = request.get("request_params", {}).get("name")

        if name:
            old_course = engine.get_course(name)
            if old_course:
                new_name = f"copy_{name}"
                new_course = old_course.clone()
                new_course.name = new_name
                engine.courses.append(new_course)

                return "200 OK", render(
                    "course_list.html",
                    objects_list=engine.courses,
                    name=new_course.category.name,
                )

        return "200 OK", "No courses have been added yet"
