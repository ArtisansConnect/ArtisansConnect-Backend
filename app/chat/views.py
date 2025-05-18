from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializers import MessageSerializer
from core.models import Message



class MessageView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sender_id = self.request.query_params.get('sender_id')
        receiver_id = self.request.query_params.get('receiver_id')
        return Message.objects.filter(sender_id=sender_id, receiver_id=receiver_id)