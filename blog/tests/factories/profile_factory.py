import factory

from blog.models.profile import Profile

from .user_factory import UserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    bio = factory.Faker("paragraph", nb_sentences=2)
    user = factory.SubFactory(UserFactory)
