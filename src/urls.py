from fronts import date_front
from views import Contacts, Index

fronts = [date_front]


routes = {
    "/": Index(),
    "/contacts/": Contacts(),
}
