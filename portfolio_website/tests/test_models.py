import datetime

from django import db
from django.test import TestCase

from portfolio_app.models import Post, Portfolio, Tag, Client, Service


class ClientTestCase(TestCase):
    @classmethod
    def setUp(cls):
        Client.objects.create(
            name="Иван",
            company="Рога и Копыта",
            telegram="@ivan_company",
            email="ivan@mail.ru",
            state=Client.State.ACTIVE,
            additional_info="none"
        )
        Client.objects.create(
            name="Петр",
            company="Первый",
            telegram="@peter_company",
            email="peter@mail.ru",
            state=Client.State.ACTIVE,
            additional_info="none"
        )

    def test_get_client_by_email(self):
        """Clients are identified by email"""
        peter = Client.objects.get(email="peter@mail.ru")
        self.assertEqual("Петр", peter.name)
        self.assertEqual(peter.state, Client.State.ACTIVE)

    def test_get_archived_clients__none(self):
        """There are no archived clients"""
        archived_clients = Client.objects.filter(state=Client.State.ARCHIVED)
        self.assertEqual(0, archived_clients.count())

    def test_get_active_clients(self):
        """There are two active clients"""
        archived_clients = Client.objects.filter(state=Client.State.ACTIVE)
        self.assertEqual(2, archived_clients.count())

    def test_archive_client(self):
        """Make one client archived"""
        peter = Client.objects.get(email="peter@mail.ru")
        peter.state = Client.State.ARCHIVED
        peter.save()
        archived_clients = Client.objects.filter(state=Client.State.ARCHIVED)
        self.assertEqual(1, archived_clients.count())

    def test_delete_client(self):
        """Delete client"""
        clients_count = Client.objects.all().count()
        peter = Client.objects.get(email="peter@mail.ru")
        peter.delete()
        self.assertEqual(clients_count - 1, Client.objects.all().count())


class PortfolioTestCase(TestCase):
    @classmethod
    def setUp(cls):
        Portfolio.objects.create(
            site_name="Name",
            site_description="Description",
            about="About"
        )

    def test_make_more_than_one_portfolio__exception(self):
        """Portfolio is singleton"""
        self.assertRaises(db.utils.IntegrityError, Portfolio.objects.create,
                          site_name="Name",
                          site_description="Description",
                          about="About")


class PostTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.post = Post.objects.create(
            datetime=datetime.datetime.now(),
            text="Text",
            key_phrase="Key"
        )

    def test_get_post_by_id(self):
        """Post could be gotten by id"""
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.text, self.post.text)

    def test_get_all_posts(self):
        """There are posts"""
        self.assertEqual(1, Post.objects.all().count())

    def test_delete_post(self):
        """Delete post"""
        post_count = Post.objects.all().count()
        post = Post.objects.get(id=self.post.id)
        post.delete()
        self.assertEqual(post_count - 1, Post.objects.all().count())

    def test_add_tag_to_post__updated_post(self):
        """Add tag to post, increased number of tags in post"""
        tag = Tag.objects.create(name="name", description="description")
        prev_tags_count = Post.objects.get(id=self.post.id).tags.count()
        post = Post.objects.get(id=self.post.id)
        post.tags.add(tag)
        post.save()
        self.assertEqual(prev_tags_count + 1,
                         Post.objects.get(id=self.post.id).tags.count())

    def test_delete_tag_from_post__updated_post(self):
        """Delete tag from post, decreased number of tags in post"""
        post = Post.objects.get(id=self.post.id)
        prev_tags_count = post.tags.count()
        tag = Tag.objects.create(name="name", description="description")
        post.tags.add(tag)
        post.save()
        post.tags.remove(tag)
        self.assertEqual(prev_tags_count,
                         post.tags.count())


class TagTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.tag = Tag.objects.create(
            name="Name",
            description="Description"
        )

    def test_get_tag_by_id(self):
        """Tag could be gotten by id"""
        tag = Tag.objects.get(id=self.tag.id)
        self.assertEqual(tag.name, self.tag.name)

    def test_get_all_tags(self):
        """There are tags"""
        self.assertEqual(1, Tag.objects.all().count())

    def test_delete_tag(self):
        """Delete tag"""
        tag_count = Tag.objects.all().count()
        tag = Tag.objects.get(id=self.tag.id)
        tag.delete()
        self.assertEqual(tag_count - 1, Tag.objects.all().count())







