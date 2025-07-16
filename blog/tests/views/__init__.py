from .comment_views_test import AuthenticatedCommentTests as AuthenticatedCommentTests
from .register_views_test import UserRegistrationTests as UserRegistrationTests
from .user_views_test import UserTests as UserTests

from .bookmark_views_test import (
    AuthenticatedBookmarkTests as AuthenticatedBookmarkTests,
)

from .category_views_test import (
    CategoryTests as CategoryTests,
    AuthenticatedCategoryTests as AuthenticatedCategoryTests,
)

from .notification_views_test import (
    AuthenticatedNotificationTests as AuthenticatedNotificationTests,
)

from .post_views_test import (
    AuthenticatedPostTests as AuthenticatedPostTests,
    PostTests as PostTests,
)

from .token_views_test import (
    BlogTokenObtainPairViewTests as BlogTokenObtainPairViewTests,
)
