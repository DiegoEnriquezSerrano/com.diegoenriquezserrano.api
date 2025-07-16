from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views as blog_views

app_name = "blog"

urlpatterns = [
    ##
    ##
    ## User paths
    path(
        "user/profile/<username>",
        blog_views.ProfileView.as_view(),
        name="profile_detail",
    ),
    path("user/register", blog_views.RegisterView.as_view(), name="register_path"),
    path(
        "user/token",
        blog_views.BlogTokenObtainPairView.as_view(),
        name="login_path",
    ),
    ##
    ##
    ## Post paths
    path("posts", blog_views.PostListCreateAPIView.as_view(), name="posts_path"),
    path(
        "posts/bookmark",
        blog_views.BookmarkCreateAPIView.as_view(),
        name="create_or_delete_bookmark_path",
    ),
    path(
        "posts/comment",
        blog_views.CommentCreateAPIView.as_view(),
        name="create_comment_path",
    ),
    path(
        "posts/like",
        blog_views.PostLikeCreateAPIView.as_view(),
        name="create_or_delete_like_path",
    ),
    path(
        "posts/<username>",
        blog_views.PostListByUserAPIView.as_view(),
        name="posts_by_user_path",
    ),
    path(
        "posts/<username>/<slug>",
        blog_views.PostRetrieveAPIView.as_view(),
        name="post_detail_path",
    ),
    path(
        "dashboard/posts/<post_id>",
        blog_views.DashboardPostRetrieveUpdateDestroyAPIView.as_view(),
        name="post_update_path",
    ),
    ##
    ##
    ## Category paths
    path(
        "categories",
        blog_views.CategoryListCreateAPIView.as_view(),
        name="categories_path",
    ),
    path(
        "categories/<username>",
        blog_views.CategoryListByUserAPIView.as_view(),
        name="categories_by_user_path",
    ),
    path(
        "categories/<username>/<slug>",
        blog_views.CategoryRetrieveAPIView.as_view(),
        name="category_detail_path",
    ),
    path(
        "categories/<username>/<slug>/posts",
        blog_views.CategoryPostsListAPIView.as_view(),
        name="category_posts_path",
    ),
    ##
    ##
    ## Dashboard paths
    path(
        "dashboard/bookmarks",
        blog_views.DashboardBookmarkListsAPIView.as_view(),
        name="dashboard_bookmarks_path",
    ),
    path(
        "dashboard/categories",
        blog_views.DashboardCategoryListsAPIView.as_view(),
        name="dashboard_categories_path",
    ),
    path(
        "dashboard/categories/<slug>",
        blog_views.DashboardCategoriesRetrieveUpdateDestroyAPIView.as_view(),
        name="dashboard_categories_path",
    ),
    path(
        "dashboard/comments",
        blog_views.DashboardCommentListsAPIView.as_view(),
        name="dashboard_comments_path",
    ),
    path(
        "dashboard/comments/<id>",
        blog_views.DashboardCommentsRetrieveDestroyAPIView.as_view(),
        name="dashboard_retrieve_destroy_comment_path",
    ),
    path(
        "dashboard/stats",
        blog_views.AuthorStatsAPIView.as_view(),
        name="dashboard_stats_path",
    ),
    path(
        "dashboard/posts",
        blog_views.DashboardPostListsAPIView.as_view(),
        name="dashboard_posts_path",
    ),
    path(
        "dashboard/notifications/<notification_id>",
        blog_views.NotificationUpdateAPIView.as_view(),
    ),
    path(
        "dashboard/notifications",
        blog_views.NotificationListAPIView.as_view(),
        name="dashboard_notifications_path",
    ),
]
