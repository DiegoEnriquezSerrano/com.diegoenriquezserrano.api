from .authenticated.author_views import AuthorStatsAPIView as AuthorStatsAPIView
from .confirmation_views import ConfirmationView as ConfirmationView
from .register_views import RegisterView as RegisterView
from .token_views import BlogTokenObtainPairView as BlogTokenObtainPairView
from .user_views import ProfileView as ProfileView
from .captcha_views import ChallengeImageView as ChallengeImageView

from .authenticated.profile_views import (
    DashboardProfileRetrieveUpdateAPIView as DashboardProfileRetrieveUpdateAPIView,
)

from .authenticated.bookmark_views import (
    BookmarkCreateAPIView as BookmarkCreateAPIView,
    DashboardBookmarkListsAPIView as DashboardBookmarkListsAPIView,
)

from .authenticated.category_views import (
    DashboardCategoriesRetrieveUpdateDestroyAPIView as DashboardCategoriesRetrieveUpdateDestroyAPIView,
    DashboardCategoryListCreateAPIView as DashboardCategoryListCreateAPIView,
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
    DashboardPostListCreateAPIView as DashboardPostListCreateAPIView,
    DashboardPostRetrieveUpdateDestroyAPIView as DashboardPostRetrieveUpdateDestroyAPIView,
    PostLikeCreateAPIView as PostLikeCreateAPIView,
    DashboardCategoryPostListAPIView as DashboardCategoryPostListAPIView,
)

from .authenticated.project_views import (
    DashboardProjectListCreateAPIView as DashboardProjectListCreateAPIView,
    DashboardProjectRetrieveUpdateDestroyAPIView as DashboardProjectRetrieveUpdateDestroyAPIView,
)

from .authenticated.subscription_views import (
    DashboardSubscriptionListsAPIView as DashboardSubscriptionListsAPIView,
)

from .authenticated.user_subscription_views import (
    DashboardUserSubscriptionCreateAPIView as DashboardUserSubscriptionCreateAPIView,
    DashboardUserSubscriptionListsAPIView as DashboardUserSubscriptionListsAPIView,
    DashboardUserSubscriptionRetrieveUpdateAPIView as DashboardUserSubscriptionRetrieveUpdateAPIView,
)

from .category_views import (
    CategoryListByUserAPIView as CategoryListByUserAPIView,
    CategoryListAPIView as CategoryListAPIView,
    CategoryPostsListAPIView as CategoryPostsListAPIView,
    CategoryRetrieveAPIView as CategoryRetrieveAPIView,
)

from .post_views import (
    PostListByUserAPIView as PostListByUserAPIView,
    PostListAPIView as PostListAPIView,
    PostRetrieveAPIView as PostRetrieveAPIView,
)

from .project_views import (
    ProjectListAPIView as ProjectListAPIView,
    ProjectListByUsernameAPIView as ProjectListByUsernameAPIView,
    ProjectRetrieveAPIView as ProjectRetrieveAPIView,
)

from .subscription_views import (
    SubscriptionConfirmationUpdateAPIView as SubscriptionConfirmationUpdateAPIView,
    SubscriptionCreateAPIView as SubscriptionCreateAPIView,
)
