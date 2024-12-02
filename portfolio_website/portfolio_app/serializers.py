from rest_framework import serializers
from portfolio_app import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['id', 'datetime', 'text', 'key_phrase', 'tags']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'name', 'description']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ['id', 'name', 'state', 'company', 'telegram', 'email', 'additional_info']


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Portfolio
        fields = ['site_name', 'site_description', 'about', 'service_list']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ['id', 'value']
