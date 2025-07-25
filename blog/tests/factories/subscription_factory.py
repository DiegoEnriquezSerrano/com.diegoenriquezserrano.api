import factory

from django.utils import timezone

from blog.models.subscription import Subscription

from .user_factory import UserFactory


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    activated_date = timezone.now()
    active = True
    confirmation_token = factory.Sequence(lambda c: "dummyconfirmationtoken%s" % c)
    confirmation_token_sent_at = timezone.now()
    confirmed = True
    confirmed_at = timezone.now()
    email = factory.LazyAttribute(lambda o: "%s@example.org" % o.name)
    name = factory.Sequence(lambda n: "john%s" % n)
    user = factory.SubFactory(UserFactory)
