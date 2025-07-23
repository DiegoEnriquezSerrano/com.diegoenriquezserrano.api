from .authenticated.author_views import AuthorStatsAPIView as AuthorStatsAPIView
from .register_views import RegisterView as RegisterView
from .token_views import BlogTokenObtainPairView as BlogTokenObtainPairView
from .user_views import ProfileView as ProfileView

from .authenticated.profile_views import (
    DashboardProfileRetrieveUpdateAPIView as DashboardProfileRetrieveUpdateAPIView,
)

from .authenticated.bookmark_views import (
    BookmarkCreateAPIView as BookmarkCreateAPIView,
    DashboardBookmarkListsAPIView as DashboardBookmarkListsAPIView,
)

from .authenticated.category_views import (
    DashboardCategoriesRetrieveUpdateDestroyAPIView as DashboardCategoriesRetrieveUpdateDestroyAPIView,
    DashboardCategoryListsAPIView as DashboardCategoryListsAPIView,
)

from .authenticated.comment_views import (
    CommentCreateAPIView as CommentCreateAPIView,
    DashboardCommentListsAPIView as DashboardCommentListsAPIView,
    DashboardCommentsRetrieveDestroyAPIView as DashboardCommentsRetrieveDestroyAPIView,
)

from .authenticated.notification_views import (
    NotificationListAPIView as NotificationListAPIView,
    NotificationUpdateAPIView as NotificationUpdateAPIView,
)

from .authenticated.post_views import (
    PostLikeCreateAPIView as PostLikeCreateAPIView,
    DashboardPostListsAPIView as DashboardPostListsAPIView,
    DashboardPostRetrieveUpdateDestroyAPIView as DashboardPostRetrieveUpdateDestroyAPIView,
)

from .authenticated.subscription_views import (
    DashboardSubscriptionListsAPIView as DashboardSubscriptionListsAPIView,
)

from .authenticated.user_subscription_views import (
    DashboardUserSubscriptionListsAPIView as DashboardUserSubscriptionListsAPIView,
    DashboardUserSubscriptionCreateAPIView as DashboardUserSubscriptionCreateAPIView,
    DashboardUserSubscriptionRetrieveUpdateAPIView as DashboardUserSubscriptionRetrieveUpdateAPIView,
)

from .category_views import (
    CategoryListByUserAPIView as CategoryListByUserAPIView,
    CategoryListCreateAPIView as CategoryListCreateAPIView,
    CategoryPostsListAPIView as CategoryPostsListAPIView,
    CategoryRetrieveAPIView as CategoryRetrieveAPIView,
)

from .post_views import (
    PostListCreateAPIView as PostListCreateAPIView,
    PostRetrieveAPIView as PostRetrieveAPIView,
    PostListByUserAPIView as PostListByUserAPIView,
)

from .subscription_views import SubscriptionCreateAPIView as SubscriptionCreateAPIView
