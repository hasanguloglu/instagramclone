from django.urls import path
from .views import list_view, detail_view, create_view, like_view, social_view, follow_view, comment_add_view, explore_view, post_share_view, shared_posts_view, profile_edit_view

app_name = "post"

urlpatterns = [
    path('', list_view, name='list'),
    path('create/', create_view, name='create'),
    path('edit/', profile_edit_view, name='edit'),
    path('detail/', detail_view, name='detail'),
    path('<uuid:uuid>/like/', like_view, name='like'),
    path('social/', social_view, name='social'),
    path('explore/', explore_view, name='explore'),
    path('post/<int:post_id>/share/', post_share_view, name='share_post'),
    path('shared_posts/', shared_posts_view, name='shared_posts'),
    path('follow/', follow_view, name='follow'),
    path('<uuid:uuid>/comment_add/', comment_add_view, name='comment_add')
]
