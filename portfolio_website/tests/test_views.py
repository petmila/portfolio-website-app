import datetime

from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse

from portfolio_app.views import PostListView, ActiveClientListView, ArchivedClientListView, PortfolioDetailView, \
    TagListView, ServiceListView


class TestPostListViews(TestCase):
    @classmethod
    def setUp(cls):
        """
        Set up the request and call into the view
        """
        cls.view = PostListView()

    def test_post_view_page_loads(self):
        """
        Verify the page loads for this view
        """
        self.request = RequestFactory().get(reverse('posts'))
        self.view.setup(self.request)
        response = PostListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_post_post_view__forbidden(self):
        """
        Verify the page loads for this view
        """
        data = {"datetime": datetime.datetime.now(),
                "text": "Text",
                "key_phrase": "Key"}
        self.request = RequestFactory().post(reverse('posts'), data=data)
        self.view.setup(self.request)
        response = PostListView.as_view()(self.request)
        self.assertEqual(response.status_code, 403)


class TestClientListViews(TestCase):
    @classmethod
    def setUp(cls):
        """
        Set up the request and call into the view
        """
        cls.active_request = RequestFactory().get(reverse('active-clients'))
        cls.active_view = ActiveClientListView()
        cls.active_view.setup(cls.active_request)

        cls.archived_request = RequestFactory().get(reverse('archived-clients'))
        cls.archived_view = ArchivedClientListView()
        cls.archived_view.setup(cls.archived_request)

    def test_active_view_page_loads(self):
        """
        Verify the view returns an HTTP 200 if the user is logged in.
        """
        self.active_request.user = User.objects.create(username='test', is_active=True, email='a@b.com')
        self.active_view.setup(self.active_request)
        response = ActiveClientListView.as_view()(self.active_request)
        self.assertEqual(response.status_code, 200)

    def test_archived_view_page_loads(self):
        """
        Verify the view returns an HTTP 200 if the user is logged in.
        """
        self.archived_request.user = User.objects.create(username='test', is_active=True, email='a@b.com')
        self.archived_view.setup(self.archived_request)
        response = ArchivedClientListView.as_view()(self.archived_request)
        self.assertEqual(response.status_code, 200)

    def test_active_view_page__forbidden(self):
        """
        Verify the view returns an HTTP 403 if the user is anonymous.
        """
        self.active_request.user = AnonymousUser()
        self.active_view.setup(self.active_request)
        response = ActiveClientListView.as_view()(self.active_request)
        self.assertEqual(response.status_code, 403)

    def test_archived_view_page__forbidden(self):
        """
        Verify the view returns an HTTP 403 if the user is anonymous.
        """
        self.archived_request.user = AnonymousUser()
        self.archived_view.setup(self.archived_request)
        response = ArchivedClientListView.as_view()(self.archived_request)
        self.assertEqual(response.status_code, 403)


class TestTagsListViews(TestCase):
    @classmethod
    def setUp(cls):
        """
        Set up the request and call into the view
        """
        cls.view = TagListView()

    def test_tags_view_page_loads(self):
        """
        Verify the page loads for this view
        """
        self.request = RequestFactory().get(reverse('tags'))
        self.view.setup(self.request)
        response = TagListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_post_tag_view__forbidden(self):
        """
        Verify the page loads for this view
        """
        data = {"datetime": datetime.datetime.now(),
                "text": "Text",
                "key_phrase": "Key"}
        self.request = RequestFactory().post(reverse('tags'), data=data)
        self.view.setup(self.request)
        response = TagListView.as_view()(self.request)
        self.assertEqual(response.status_code, 403)


class TestServicesListViews(TestCase):
    @classmethod
    def setUp(cls):
        """
        Set up the request and call into the view
        """
        cls.view = ServiceListView()

    def test_services_view_page_loads(self):
        """
        Verify the page loads for this view
        """
        self.request = RequestFactory().get(reverse('services'))
        self.view.setup(self.request)
        response = ServiceListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_post_service_view__forbidden(self):
        """
        Verify the page loads for this view
        """
        data = {"datetime": datetime.datetime.now(),
                "text": "Text",
                "key_phrase": "Key"}
        self.request = RequestFactory().post(reverse('services'), data=data)
        self.view.setup(self.request)
        response = ServiceListView.as_view()(self.request)
        self.assertEqual(response.status_code, 403)
