from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field


class Pillar(models.Model):
    """
    Content pillars for ModernMuse:
    - Parent Productivity
    - Raising Independent Kids
    - Personal Growth for Parents
    - Real Life Systems
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(
        blank=True,
        help_text="Brief description of this content pillar"
    )
    icon = models.CharField(
        max_length=50, blank=True,
        help_text="Optional icon class or emoji for display"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:pillar_posts", args=[self.slug])


class Post(models.Model):
    """A RoutineParent blog post."""

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        REVIEW = "RV", "Ready for Review"
        PUBLISHED = "PB", "Published"

    # Core content
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    subtitle = models.CharField(
        max_length=300, blank=True,
        help_text="Optional subtitle shown below the title"
    )
    body = CKEditor5Field(config_name="default")
    excerpt = models.TextField(
        max_length=500, blank=True,
        help_text="Short summary for post cards and SEO (auto-generated if blank)"
    )

    # Organization
    pillar = models.ForeignKey(
        Pillar, on_delete=models.SET_NULL,
        null=True, related_name="posts",
        help_text="Which content pillar does this post belong to?"
    )
    tags = TaggableManager(blank=True)

    # Featured image
    featured_image = models.ImageField(
        upload_to="posts/%Y/%m/", blank=True,
        help_text="Main image for the post"
    )
    featured_image_alt = models.CharField(
        max_length=250, blank=True,
        help_text="Alt text for the featured image (accessibility)"
    )

    # Metadata
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this post on the homepage"
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # SEO
    meta_description = models.CharField(
        max_length=160, blank=True,
        help_text="SEO meta description (160 chars max)"
    )

    class Meta:
        ordering = ["-publish"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.body:
            import re
            clean_body = re.sub(r'<[^>]+>', '', self.body)
            clean_body = clean_body.replace('&nbsp;', ' ').strip()
            self.excerpt = clean_body[:497] + "..." if len(clean_body) > 500 else clean_body
        super().save(*args, **kwargs)

    @property
    def reading_time(self):
        """Estimate reading time in minutes."""
        word_count = len(self.body.split())
        return max(1, round(word_count / 200))


class Comment(models.Model):
    """A reader comment on a blog post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


class NewsletterSubscriber(models.Model):
    """Email subscribers for the ModernMuse newsletter."""

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.subject} — {self.name} ({self.created:%d %b %Y})"