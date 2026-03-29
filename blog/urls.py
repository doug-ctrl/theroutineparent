from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("newsletter/", views.newsletter_signup, name="newsletter_signup"),
    path("free-planner/", views.DownloadPageView.as_view(), name="free_planner"),
    path("download/planner/", views.download_planner, name="download_planner"),
    path("download/chore-chart/", views.download_chore_chart, name="download_chore_chart"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("pillar/<slug:slug>/", views.PillarPostsView.as_view(), name="pillar_posts"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]