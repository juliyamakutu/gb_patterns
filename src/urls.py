from fronts import date_front
from views import (CategoryList, Contacts, CopyCourse, CoursesList,
                   CreateCategory, CreateCourse, Index)

fronts = [date_front]


routes = {
    "/": Index(),
    "/contacts/": Contacts(),
    "/courses-list/": CoursesList(),
    "/create-course/": CreateCourse(),
    "/create-category/": CreateCategory(),
    "/category-list/": CategoryList(),
    "/copy-course/": CopyCourse(),
}
