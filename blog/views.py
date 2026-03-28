from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Post, Pillar, Comment, NewsletterSubscriber
from .forms import CommentForm
from django.http import FileResponse
from django.conf import settings
import os


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).select_related("pillar", "author")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).select_related("pillar", "author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(active=True)
        context["comment_form"] = CommentForm()
        context["related_posts"] = Post.objects.filter(
            status=Post.Status.PUBLISHED,
            pillar=self.object.pillar
        ).exclude(id=self.object.id).select_related("pillar", "author")[:3]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                post=self.object,
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                body=form.cleaned_data["body"],
            )
            messages.success(request, "Your comment has been posted!")
            return redirect(self.object.get_absolute_url())
        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(context)


class PillarPostsView(ListView):
    model = Post
    template_name = "blog/pillar_posts.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            pillar__slug=self.kwargs["slug"]
        ).select_related("pillar", "author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pillar"] = get_object_or_404(Pillar, slug=self.kwargs["slug"])
        return context


class SearchView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query),
                status=Post.Status.PUBLISHED
            ).select_related("pillar", "author")
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"


def newsletter_signup(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        if email:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Please enter a valid email address.")
                return redirect("blog:free_planner")
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.info(request, "You're already subscribed!")
            else:
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Thanks for subscribing!")
    return redirect("blog:free_planner")

class DownloadPageView(TemplateView):
    template_name = "pages/download.html"

def download_planner(request):
    file_path = os.path.join(settings.MEDIA_ROOT, "downloads", "weekly_family_planner.pdf")
    return FileResponse(open(file_path, "rb"), content_type="application/pdf", as_attachment=True, filename="Weekly_Family_Planner_The_Routine_Parent.pdf")