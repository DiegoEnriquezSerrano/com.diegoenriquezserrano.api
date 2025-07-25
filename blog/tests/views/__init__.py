from .bookmark_views_test import (
    AuthenticatedBookmarkTests as AuthenticatedBookmarkTests,
)

from .category_views_test import (
    CategoryTests as CategoryTests,
    AuthenticatedCategoryTests as AuthenticatedCategoryTests,
)

from .comment_views_test import AuthenticatedCommentTests as AuthenticatedCommentTests
from .confirmation_views_test import ConfirmationViewTests as ConfirmationViewTests

from .notification_views_test import (
    AuthenticatedNotificationTests as AuthenticatedNotificationTests,
)

from .post_views_test import (
    AuthenticatedPostTests as AuthenticatedPostTests,
    PostTests as PostTests,
)

from .profile_views_test import AuthenticatedProfileTests as AuthenticatedProfileTests
from .register_views_test import UserRegistrationTests as UserRegistrationTests

from .subscription_views_test import (
    AuthenticatedSubscriptionTests as AuthenticatedSubscriptionTests,
    SubscriptionTests as SubscriptionTests,
)

from .token_views_test import (
    BlogTokenObtainPairViewTests as BlogTokenObtainPairViewTests,
)

from .user_views_test import UserTests as UserTests

from .user_subscription_views_test import (
    AuthenticatedUserSubscriptionTests as AuthenticatedUserSubscriptionTests,
)
