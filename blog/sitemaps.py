from django.contrib.sitemaps import Sitemap
from .models import Post, Pillar


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated


class PillarSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Pillar.objects.all()

    def lastmod(self, obj):
        latest_post = obj.posts.filter(
            status=Post.Status.PUBLISHED
        ).order_by("-updated").first()
        if latest_post:
            return latest_post.updated
        return None


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ["blog:post_list", "blog:about"]

    def location(self, item):
        from django.urls import reverse
        return reverse(item)