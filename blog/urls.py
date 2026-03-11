from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("pillar/<slug:slug>/", views.PillarPostsView.as_view(), name="pillar_posts"),
    path("about/", views.AboutView.as_view(), name="about"),
]