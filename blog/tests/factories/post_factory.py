import factory

from blog.models.post import Post

from .user_factory import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    body = factory.Faker("paragraph", nb_sentences=6)
    cover_image_url = factory.Faker("url")
    description = factory.Faker("paragraph", nb_sentences=3)
    excerpt = factory.Faker("paragraph", nb_sentences=3)
    title = factory.Faker("sentence", nb_words=4)
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.categories.add(*extracted)
