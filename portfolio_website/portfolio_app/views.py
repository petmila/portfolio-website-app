import requests
import json
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
import datetime

from rest_framework.response import Response

import local_settings
from . import models
from . import serializers


class PostListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = models.Post.objects.order_by('datetime').all()
    serializer_class = serializers.PostSerializer
    paginate_by = 1

    def create(self, request, *args, **kwargs):
        request.data['datetime'] = datetime.datetime.now()
        serializer = serializers.PostSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError:
            return Response({"errors": (serializer.errors,)},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(request.data, status=status.HTTP_200_OK)
    # template_name = 'portfolio_app/post_list.html'


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


class TagListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Tag.objects.all()
    # lookup_field = 'name'
    serializer_class = serializers.TagSerializer


class ClientCreateView(generics.CreateAPIView):
    serializer_class = serializers.ClientSerializer

    def create(self, request, *args, **kwargs):
        request.data['state'] = models.Client.State.ACTIVE
        serializer = serializers.ClientSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError:
            return Response({"errors": (serializer.errors,)},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            send_client_update(request.data)
            return Response(request.data, status=status.HTTP_200_OK)


class ClientListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.all()


class ActiveClientListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.filter(state=models.Client.State.ACTIVE)


class ArchivedClientListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.filter(state=models.Client.State.ARCHIVED)


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Client.objects.all()
    lookup_field = 'email'
    serializer_class = serializers.ClientSerializer


class PortfolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Portfolio.objects.all()
    serializer_class = serializers.PortfolioSerializer


class ServiceListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


def index(request):
    """
    View function for home page of site.
    """
    posts = models.Post.objects.order_by('datetime').all()
    portfolio = models.Portfolio.objects.first()
    service_list = models.Service.objects.all()

    context = {
        'post_list': posts,
        'portfolio': portfolio,
        'services': service_list,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def send_client_update(client_data):
    data_ = f'Новый клиент зарегистрировался!\n Имя: {client_data["name"]}\n Компания: {client_data["company"]}\n Telegram: {client_data["telegram"]}\n Email: {client_data["email"]}\n Дополнительная информация: {client_data["additional_info"]}\n'
    keyboard = json.dumps({'inline_keyboard': [[{"text": "Архивировать", "callback_data": "archive"}, {"text": "Пропустить", "callback_data": "skip"}]]})
    data = {'chat_id': local_settings.CHAT_ID, 'text': data_, 'parse_mode': "HTML", 'reply_markup': keyboard}
    requests.post(url="https://api.telegram.org/bot" + local_settings.API_KEY + "/sendMessage", data=data)
