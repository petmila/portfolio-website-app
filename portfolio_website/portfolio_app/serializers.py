from rest_framework import serializers
from portfolio_app import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['datetime', 'text', 'key_phrase', 'tags']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['name', 'description']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ['name', 'company', 'telegram', 'email', 'additional_info']


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Portfolio
        fields = ['site_name', 'site_description', 'about', 'service_list']