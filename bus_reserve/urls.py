from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("buses/", views.BusesView.as_view(), name="buses"),
    path("book-bus/<str:bsid>", views.BookView.as_view(), name="book_bus")
]
