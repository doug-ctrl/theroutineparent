import re
from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from blog.models import Pillar, Post

APEX = "https://theroutineparent.com"


def make_pillar(name="Real Life Systems", slug="real-life-systems"):
    return Pillar.objects.create(name=name, slug=slug)


def make_post(title, days_ago, pillar=None, status=Post.Status.PUBLISHED):
    author, _ = User.objects.get_or_create(username="douglas")
    return Post.objects.create(
        title=title,
        body="Body text",
        author=author,
        pillar=pillar,
        status=status,
        publish=timezone.now() - timedelta(days=days_ago),
    )


def make_pillar_posts(pillar, count):
    """Newest first: index 0 is the newest post."""
    return [make_post(f"{pillar.name} {i}", days_ago=i, pillar=pillar) for i in range(count)]


def links_between(html, start_marker, end_marker):
    """(href, anchor text) pairs between two markers in the page."""
    start = html.index(start_marker)
    block = html[start:html.index(end_marker, start)]
    return re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', block)


def related_links(html):
    links = links_between(html, 'class="related-posts"', "<!-- Comments")
    return [(href, text) for href, text in links if text != "Read more →"]


def footer_links(html):
    return links_between(html, 'class="footer-latest"', "</nav>")


# --- Post.next_in_pillar ---

@pytest.mark.django_db
def test_next_in_pillar_takes_next_older_posts():
    a, b, c, d, e = make_pillar_posts(make_pillar(), 5)
    assert a.next_in_pillar() == [b, c, d]
    assert b.next_in_pillar() == [c, d, e]


@pytest.mark.django_db
def test_next_in_pillar_wraps_round_to_newest():
    a, b, c, d, e = make_pillar_posts(make_pillar(), 5)
    assert d.next_in_pillar() == [e, a, b]
    assert e.next_in_pillar() == [a, b, c]


@pytest.mark.django_db
def test_every_post_in_pillar_gets_inbound_links():
    posts = make_pillar_posts(make_pillar(), 8)
    linked = {p.pk for post in posts for p in post.next_in_pillar()}
    assert linked == {p.pk for p in posts}


@pytest.mark.django_db
def test_next_in_pillar_with_small_pillar_never_repeats_or_includes_self():
    a, b, c = make_pillar_posts(make_pillar(), 3)
    assert c.next_in_pillar() == [a, b]
    assert make_post("Solo", 0, pillar=make_pillar("Solo", "solo")).next_in_pillar() == []


@pytest.mark.django_db
def test_next_in_pillar_skips_drafts_and_other_pillars():
    pillar = make_pillar()
    a, b = make_pillar_posts(pillar, 2)
    make_post("Draft", 0.5, pillar=pillar, status=Post.Status.DRAFT)
    make_post("Elsewhere", 0.5, pillar=make_pillar("Other", "other"))
    assert a.next_in_pillar() == [b]


@pytest.mark.django_db
def test_next_in_pillar_handles_same_publish_time():
    pillar = make_pillar()
    same = timezone.now()
    posts = [make_post(f"Tie {i}", 0, pillar=pillar) for i in range(4)]
    Post.objects.filter(pk__in=[p.pk for p in posts]).update(publish=same)
    posts = [Post.objects.get(pk=p.pk) for p in posts]
    linked = {p.pk for post in posts for p in post.next_in_pillar()}
    assert linked == {p.pk for p in posts}


@pytest.mark.django_db
def test_post_without_pillar_has_no_related_posts():
    assert make_post("No pillar", 0).next_in_pillar() == []


# --- "More from <pillar>" on post detail ---

@pytest.mark.django_db
def test_post_detail_shows_more_from_pillar_with_apex_links(client):
    pillar = make_pillar()
    a, b, c, d, e = make_pillar_posts(pillar, 5)
    html = client.get(e.get_absolute_url()).content.decode()
    assert "More from Real Life Systems" in html
    assert related_links(html) == [
        (f"{APEX}{p.get_absolute_url()}", p.title) for p in (a, b, c)
    ]


@pytest.mark.django_db
def test_post_without_pillar_has_no_more_from_block(client):
    post = make_post("No pillar", 0)
    assert 'class="related-posts"' not in client.get(post.get_absolute_url()).content.decode()


# --- "Latest Posts" footer ---

@pytest.mark.django_db
@pytest.mark.parametrize("path", ["/", "/about/", "/contact/", "/free-planner/", "/search/?q=x"])
def test_footer_lists_five_newest_posts_on_every_page(client, path):
    posts = [make_post(f"Post {i}", days_ago=i) for i in range(7)]
    make_post("Unpublished", 0, status=Post.Status.DRAFT)
    html = client.get(path).content.decode()
    assert footer_links(html) == [
        (f"{APEX}{p.get_absolute_url()}", p.title) for p in posts[:5]
    ]


@pytest.mark.django_db
def test_footer_on_post_detail_page(client):
    posts = [make_post(f"Post {i}", days_ago=i) for i in range(6)]
    html = client.get(posts[5].get_absolute_url()).content.decode()
    assert [t for _, t in footer_links(html)] == [p.title for p in posts[:5]]


@pytest.mark.django_db
def test_no_footer_block_when_no_posts(client):
    assert 'class="footer-latest"' not in client.get("/about/").content.decode()


@pytest.mark.django_db
def test_sidebar_still_shows_four_recent_posts(client):
    posts = [make_post(f"Post {i}", days_ago=i) for i in range(7)]
    html = client.get("/").content.decode()
    sidebar = links_between(html, 'class="sidebar-recent"', 'class="sidebar-box sidebar-newsletter"')
    assert [text for _, text in sidebar] == [p.title for p in posts[:4]]


# --- no N+1: query count doesn't grow with the number of posts ---

def count_queries(client, url):
    with CaptureQueriesContext(connection) as ctx:
        assert client.get(url).status_code == 200
    return len(ctx.captured_queries)


@pytest.mark.django_db
def test_post_detail_query_count_is_constant(client):
    pillar = make_pillar()
    posts = make_pillar_posts(pillar, 4)
    few = count_queries(client, posts[-1].get_absolute_url())
    make_pillar_posts(make_pillar("Busy", "busy"), 20)
    for i in range(20):
        make_post(f"Extra {i}", days_ago=0.1 + i / 100, pillar=pillar)
    assert count_queries(client, posts[-1].get_absolute_url()) == few


@pytest.mark.django_db
def test_footer_query_count_is_constant(client):
    make_post("Only post", 0)
    one_post = count_queries(client, "/about/")
    for i in range(10):
        make_post(f"Post {i}", days_ago=i + 1)
    assert count_queries(client, "/about/") == one_post
