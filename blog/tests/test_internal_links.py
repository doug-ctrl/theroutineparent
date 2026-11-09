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


# --- Post.next_in_pillar ---

@pytest.mark.django_db
def test_next_two_older_posts_plus_pillar_newest():
    a, b, c, d, e, f = make_pillar_posts(make_pillar(), 6)
    assert b.next_in_pillar() == [c, d, a]
    assert c.next_in_pillar() == [d, e, a]


@pytest.mark.django_db
def test_newest_post_gets_next_three_older():
    a, b, c, d, e = make_pillar_posts(make_pillar(), 5)
    assert a.next_in_pillar() == [b, c, d]


@pytest.mark.django_db
def test_wraps_round_past_newest_without_repeating_it():
    a, b, c, d, e = make_pillar_posts(make_pillar(), 5)
    # D runs out after E; the wrap would hit A (already the third link), so B fills the slot
    assert d.next_in_pillar() == [e, b, a]
    assert e.next_in_pillar() == [b, c, a]


@pytest.mark.django_db
@pytest.mark.parametrize("size", range(1, 9))
def test_links_are_unique_exclude_self_and_include_newest(size):
    posts = make_pillar_posts(make_pillar(), size)
    newest = posts[0]
    for post in posts:
        related = post.next_in_pillar()
        assert post not in related
        assert len({p.pk for p in related}) == len(related) == min(3, size - 1)
        if post != newest:
            assert related[-1] == newest


@pytest.mark.django_db
def test_every_post_in_pillar_gets_inbound_links():
    posts = make_pillar_posts(make_pillar(), 8)
    linked = {p.pk for post in posts for p in post.next_in_pillar()}
    assert linked == {p.pk for p in posts}


@pytest.mark.django_db
def test_pillar_with_fewer_than_four_posts():
    a, b, c = make_pillar_posts(make_pillar(), 3)
    assert a.next_in_pillar() == [b, c]
    assert b.next_in_pillar() == [c, a]
    assert c.next_in_pillar() == [b, a]


@pytest.mark.django_db
def test_pillar_with_one_post_has_no_links():
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
        (f"{APEX}{p.get_absolute_url()}", p.title) for p in (b, c, a)
    ]


@pytest.mark.django_db
def test_pillar_with_one_post_hides_more_from_block(client):
    post = make_post("Solo", 0, pillar=make_pillar("Solo", "solo"))
    html = client.get(post.get_absolute_url()).content.decode()
    assert 'class="related-posts"' not in html
    assert "More from Solo" not in html


@pytest.mark.django_db
def test_post_without_pillar_has_no_more_from_block(client):
    post = make_post("No pillar", 0)
    assert 'class="related-posts"' not in client.get(post.get_absolute_url()).content.decode()


# --- sidebar "Recent Posts" ---

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
def test_pages_without_sidebar_do_not_query_posts(client):
    for i in range(5):
        make_post(f"Post {i}", days_ago=i)
    with CaptureQueriesContext(connection) as ctx:
        assert client.get("/about/").status_code == 200
    assert not any('"blog_post"' in q["sql"] for q in ctx.captured_queries)
