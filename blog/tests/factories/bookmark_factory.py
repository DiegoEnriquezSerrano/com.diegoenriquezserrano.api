import factory

from blog.models.bookmark import Bookmark

from .user_factory import UserFactory
from .post_factory import PostFactory


class BookmarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bookmark

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
