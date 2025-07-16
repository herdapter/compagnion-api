from django.urls import path
from .views import *
urlpatterns = [
    path("create/", RoomCreateVIew.as_view(), name="room-create"),
    path("<int:pk>/delete/", RoomDeleteView.as_view(), name="room-delete"),
    path('admin-rooms/', AdminRoomsView.as_view(), name='admin-rooms-list'),
]
