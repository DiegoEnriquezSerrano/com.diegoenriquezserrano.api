from .factories import (
    BookmarkFactory as BookmarkFactory,
    CategoryFactory as CategoryFactory,
    CommentFactory as CommentFactory,
    NotificationFactory as NotificationFactory,
    PostFactory as PostFactory,
    ProfileFactory as ProfileFactory,
    UserFactory as UserFactory,
)

from .models import (
    BookmarkModelTests as BookmarkModelTests,
    CategoryModelTests as CategoryModelTests,
    CommentModelTests as CommentModelTests,
    PostModelTests as PostModelTests,
    UserModelTests as UserModelTests,
)

from .serializers import (
    CategorySerializerTest as CategorySerializerTest,
    ProfileSerializerTest as ProfileSerializerTest,
)

from .views import (
    AuthenticatedBookmarkTests as AuthenticatedBookmarkTests,
    AuthenticatedCategoryTests as AuthenticatedCategoryTests,
    AuthenticatedCommentTests as AuthenticatedCommentTests,
    AuthenticatedNotificationTests as AuthenticatedNotificationTests,
    AuthenticatedPostTests as AuthenticatedPostTests,
    BlogTokenObtainPairViewTests as BlogTokenObtainPairViewTests,
    CategoryTests as CategoryTests,
    UserRegistrationTests as UserRegistrationTests,
    UserTests as UserTests,
)
