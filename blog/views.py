from django.views.generic import ListView, DetailView, TemplateView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

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


class AboutView(TemplateView):
    template_name = "pages/about.html"

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
        from .models import Pillar
        context["pillar"] = Pillar.objects.get(slug=self.kwargs["slug"])
        return context