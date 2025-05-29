# chat/routing.py

from django.urls import path
from .consumer.client_consumer import ClientConsumer
from .consumer.manager_consumer import ManagerConsumer

websocket_urlpatterns = [
    path("ws/chat/client/<int:user_id>/", ClientConsumer.as_asgi()),
    path("ws/chat/manager/<str:room_name>/", ManagerConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#     re_path(r"^ws/chat/client/(?P<user_id>\d+)/$", ClientConsumer.as_asgi()),
#     re_path(r"^ws/chat/manager/(?P<room_name>client_\d+)/$", ManagerConsumer.as_asgi()),
# ]