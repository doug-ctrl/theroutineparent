from django.db.models import Count, Q

from .models import Pillar, Post


def sidebar(request):
    """Pillar list and recent posts shown in the editorial sidebar."""
    return {
        "sidebar_pillars": Pillar.objects.annotate(
            post_count=Count(
                "posts", filter=Q(posts__status=Post.Status.PUBLISHED)
            )
        ),
        "sidebar_recent_posts": Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).select_related("pillar")[:4],
    }
