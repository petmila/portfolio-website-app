from django.utils.translation import gettext_lazy as _
from django.db import models
from djsingleton.models import SingletonModel


class Service(models.Model):
    value = models.CharField(verbose_name="Value", max_length=255, null=True, blank=True)


class Portfolio(SingletonModel):
    site_name = models.CharField(verbose_name="SiteName", max_length=255, null=True, blank=True)
    site_description = models.CharField(verbose_name="SiteDescription", max_length=255, null=True, blank=True)
    about = models.TextField(verbose_name="About")
    service_list = models.ManyToManyField(Service, blank=True)


class Tag(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100, unique=True)
    description = models.TextField(verbose_name="Description")


class Post(models.Model):
    datetime = models.DateTimeField(unique=True)
    text = models.TextField(verbose_name="Text")
    key_phrase = models.CharField(verbose_name="KeyPhrase", max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)


class Client(models.Model):
    class State(models.TextChoices):
        ACTIVE = 'AC', _('Active')
        ARCHIVED = 'AR', _('Archived')

    name = models.CharField(verbose_name="Name", max_length=100)
    company = models.CharField(verbose_name="Company", max_length=100)
    telegram = models.CharField(verbose_name="Telegram", max_length=100)
    email = models.EmailField(verbose_name="Email", unique=True)
    additional_info = models.TextField(verbose_name="Info")
    state = models.CharField(verbose_name="State", max_length=10,
                             choices=State, default=State.ACTIVE)
