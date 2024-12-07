import datetime

from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse

from portfolio_app.views import PostListView, ActiveClientListView, ArchivedClientListView, TagListView
from portfolio_app.models import Post, Client, Tag


class TestPostListViews(TestCase):
    @classmethod
    def setUp(cls):
        cls.post = Post.objects.create(
            datetime=datetime.datetime.now(),
            text="Text",
            key_phrase="Key"
        )

        """
        Set up the request and call into the view
        """
        cls.view = PostListView()

    def test_queryset(self):
        """
        Verify that post is included in the posts-view
        """
        queryset = self.view.get_queryset()
        self.assertIn(self.post, queryset)


class TestClientListViews(TestCase):
    @classmethod
    def setUp(cls):
        cls.active_client = Client.objects.create(
            name="Иван",
            company="Рога и Копыта",
            telegram="@ivan_company",
            email="ivan@mail.ru",
            state=Client.State.ACTIVE,
            additional_info="none"
        )
        cls.archived_client = Client.objects.create(
            name="Петр",
            company="Первый",
            telegram="@peter_company",
            email="peter@mail.ru",
            state=Client.State.ARCHIVED,
            additional_info="none"
        )

        """
        Set up the request and call into the view
        """
        cls.active_view = ActiveClientListView()
        cls.archived_view = ArchivedClientListView()

    def test_active_queryset(self):
        """
        Verify that only active clients are included in the active-clients-view
        """
        queryset = self.active_view.get_queryset()
        self.assertIn(self.active_client, queryset)
        self.assertNotIn(self.archived_client, queryset)

    def test_archived_queryset(self):
        """
        Verify that only archived clients are included in the archived-clients-view
        """
        queryset = self.archived_view.get_queryset()
        self.assertIn(self.archived_client, queryset)
        self.assertNotIn(self.active_client, queryset)


class TestTagListViews(TestCase):
    @classmethod
    def setUp(cls):
        cls.tag = Tag.objects.create(
            name="Name",
            description="Description"
        )

        """
        Set up the request and call into the view
        """
        cls.view = TagListView()

    def test_queryset(self):
        """
        Verify that tag is included in the tags-view
        """
        queryset = self.view.get_queryset()
        self.assertIn(self.tag, queryset)
