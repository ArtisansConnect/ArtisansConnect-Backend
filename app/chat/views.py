from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializers import MessageSerializer
from core.models import Message



class MessageView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer