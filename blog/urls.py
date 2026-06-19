from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("newsletter/", views.newsletter_signup, name="newsletter_signup"),
    path("free-planner/", views.DownloadPageView.as_view(), name="free_planner"),
    path("download/planner/", views.download_planner, name="download_planner"),
    path("download/chore-chart/", views.download_chore_chart, name="download_chore_chart"),
    path("download/morningchecklist/", views.download_morning_checklist, name="download_morning_checklist"),
    path("download/eveningchecklist/", views.download_evening_checklist, name="download_evening_checklist"),
    path("download/weeklygoals/", views.download_weekly_goals_tracker, name="download_weekly_goals_tracker"),
    path("download/mealplanner/", views.download_meal_planner, name="download_meal_planner"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("pillar/<slug:slug>/", views.PillarPostsView.as_view(), name="pillar_posts"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path('feed/', LatestPostsFeed(), name='feed'),
]