from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from .models import Post, Pillar, NewsletterSubscriber


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


class PillarPostsView(ListView):
    model = Post
    template_name = "blog/pillar_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            pillar__slug=self.kwargs["slug"]
        ).select_related("pillar", "author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pillar"] = Pillar.objects.get(slug=self.kwargs["slug"])
        return context


class SearchView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

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
        email = request.POST.get("email", "").strip()
        if email:
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.info(request, "You're already subscribed!")
            else:
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Thanks for subscribing!")
    return redirect("blog:post_list")