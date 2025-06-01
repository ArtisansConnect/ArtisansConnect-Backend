from django.urls import path
from .consumer.client_consumer import ClientConsumer
from .consumer.manager_consumer import ManagerConsumer

websocket_urlpatterns = [
    path("ws/chat/client/<int:user_id>/", ClientConsumer.as_asgi()),
    path("ws/chat/manager/<str:room_name>/", ManagerConsumer.as_asgi()),
]
