from django.db.models import Count, Q
from django.utils.functional import SimpleLazyObject

from .models import Pillar, Post


def sidebar(request):
    """Pillar list for the editorial sidebar, and the latest posts shown in
    the footer on every page (the sidebar reuses the first four)."""
    return {
        "sidebar_pillars": Pillar.objects.annotate(
            post_count=Count(
                "posts", filter=Q(posts__status=Post.Status.PUBLISHED)
            )
        ),
        # One query, run only when a template first uses it
        "latest_posts": SimpleLazyObject(lambda: list(
            Post.objects.filter(status=Post.Status.PUBLISHED)[:5]
        )),
    }
