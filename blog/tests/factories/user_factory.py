import factory

from django.utils import timezone

from blog.models.user import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    confirmation_token = factory.Sequence(lambda c: "dummyconfirmationtoken%s" % c)
    confirmation_token_sent_at = timezone.now()
    confirmed = True
    confirmed_at = timezone.now()
    email = factory.LazyAttribute(lambda o: "%s@example.org" % o.username)
    username = factory.Sequence(lambda n: "john%s" % n)
