from django.contrib import admin
from .models import Pillar, Post, Comment, NewsletterSubscriber


@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ["name", "order", "post_count"]
    prepopulated_fields = {"slug": ("name",)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Posts"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "pillar", "status", "is_featured", "publish", "reading_time"]
    list_filter = ["status", "pillar", "is_featured", "publish"]
    search_fields = ["title", "body", "subtitle"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "-publish"]
    list_editable = ["status", "is_featured"]

    fieldsets = (
        ("Content", {
            "fields": ("title", "subtitle", "slug", "body", "excerpt")
        }),
        ("Organization", {
            "fields": ("pillar", "tags", "featured_image", "featured_image_alt")
        }),
        ("Publishing", {
            "fields": ("author", "status", "is_featured", "publish")
        }),
        ("SEO", {
            "fields": ("meta_description",),
            "classes": ("collapse",)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "created", "active"]
    list_filter = ["active", "created"]
    search_fields = ["name", "email", "body"]
    list_editable = ["active"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "subscribed_at", "is_active"]
    list_filter = ["is_active", "subscribed_at"]
    search_fields = ["email", "name"]