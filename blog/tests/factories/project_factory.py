import factory

from django.utils import timezone

from blog.models.project import Project

from .user_factory import UserFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    body = factory.Faker("paragraph", nb_sentences=6)
    cover_image_url = factory.Faker("url")
    description = factory.Faker("paragraph", nb_sentences=3)
    finished_at = None
    started_at = timezone.now()
    status = "ongoing"
    title = factory.Faker("sentence", nb_words=4)
    url = factory.Faker("url")
    user = factory.SubFactory(UserFactory)
