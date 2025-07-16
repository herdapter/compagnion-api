from django.urls import path
from .views import *
urlpatterns = [
    path("create/", BingoRoomsListView.as_view(), name="bingoroom-create"),
    path("list/", BingoRoomsListView.as_view(), name="bingoroom-list"),
]
