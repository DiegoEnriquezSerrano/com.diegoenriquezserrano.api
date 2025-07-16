import factory

from blog.models.category import Category

from .user_factory import UserFactory

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    user = factory.SubFactory(UserFactory)
