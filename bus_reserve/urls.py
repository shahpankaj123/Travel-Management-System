from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("seats/<str:scid>/", views.SeatView.as_view(), name="seat"),
    path("ticket/", views.BookView.as_view(), name="ticket")
]
