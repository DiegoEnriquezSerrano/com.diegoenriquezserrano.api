import factory

from blog.models.notification import Notification

from .user_factory import UserFactory
from .post_factory import PostFactory


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    type = "like"
    read = False
    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
