from django.contrib import admin

from blog.models.bookmark import Bookmark
from blog.models.category import Category
from blog.models.comment import Comment
from blog.models.notification import Notification
from blog.models.post import Post
from blog.models.profile import Profile
from blog.models.user import User


admin.site.register(Bookmark)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(User)
