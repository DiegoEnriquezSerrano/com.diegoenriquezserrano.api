import factory

from blog.models.comment import Comment

from .user_factory import UserFactory
from .post_factory import PostFactory


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    body = factory.Faker("paragraph", nb_sentences=2)
    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
