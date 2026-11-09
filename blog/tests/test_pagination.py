import re

import pytest
from django.contrib.auth.models import User

from blog.models import Pillar, Post

APEX = "https://theroutineparent.com"


def make_pillar(slug="parent-productivity"):
    return Pillar.objects.create(name="Parent Productivity", slug=slug)


def make_posts(count, pillar=None):
    author, _ = User.objects.get_or_create(username="douglas")
    return [
        Post.objects.create(
            title=f"Post {i}",
            body="Body text",
            author=author,
            pillar=pillar,
            status=Post.Status.PUBLISHED,
        )
        for i in range(count)
    ]


def canonical(response):
    match = re.search(r'<link rel="canonical" href="([^"]*)">', response.content.decode())
    return match.group(1)


@pytest.fixture
def homepage_posts(db):
    # 1 featured + 13 listed = 3 pages of 6 on the homepage
    return make_posts(14)


@pytest.fixture
def pillar(db):
    pillar = make_pillar()
    make_posts(13, pillar=pillar)  # 3 pages of 6
    return pillar


# --- ?page=1 redirect ---

@pytest.mark.django_db
def test_homepage_page_one_redirects_permanently(client, homepage_posts):
    response = client.get("/?page=1")
    assert response.status_code == 301
    assert response["Location"] == "/"


@pytest.mark.django_db
def test_page_one_redirect_keeps_other_params(client, homepage_posts):
    response = client.get("/?utm_source=pinterest&page=1&utm_medium=social")
    assert response.status_code == 301
    assert response["Location"] == "/?utm_source=pinterest&utm_medium=social"


@pytest.mark.django_db
def test_pillar_page_one_redirects(client, pillar):
    response = client.get(f"/pillar/{pillar.slug}/?page=1")
    assert response.status_code == 301
    assert response["Location"] == f"/pillar/{pillar.slug}/"


@pytest.mark.django_db
def test_search_page_one_redirect_keeps_query(client, homepage_posts):
    response = client.get("/search/?q=post&page=1")
    assert response.status_code == 301
    assert response["Location"] == "/search/?q=post"


@pytest.mark.django_db
def test_page_two_does_not_redirect(client, homepage_posts):
    assert client.get("/?page=2").status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("page, status", [("abc", 404), ("0", 404), ("99", 404), ("last", 200)])
def test_invalid_and_out_of_range_pages_unchanged(client, homepage_posts, page, status):
    assert client.get(f"/?page={page}").status_code == status


# --- pagination links ---

@pytest.mark.django_db
def test_page_two_links_back_to_clean_homepage(client, homepage_posts):
    html = client.get("/?page=2").content.decode()
    assert '<a href="/">← Previous</a>' in html
    assert '<a href="/">1</a>' in html
    assert "?page=1" not in html


@pytest.mark.django_db
def test_page_three_previous_links_to_page_two(client, homepage_posts):
    html = client.get("/?page=3").content.decode()
    assert '<a href="?page=2">← Previous</a>' in html
    assert "?page=1" not in html


@pytest.mark.django_db
def test_pillar_page_two_links_back_to_clean_pillar_url(client, pillar):
    html = client.get(f"/pillar/{pillar.slug}/?page=2").content.decode()
    assert f'<a href="/pillar/{pillar.slug}/">← Previous</a>' in html
    assert "?page=1" not in html


# --- canonical ---

@pytest.mark.django_db
def test_homepage_canonical_is_apex_root(client, homepage_posts):
    assert canonical(client.get("/")) == f"{APEX}/"


@pytest.mark.django_db
def test_canonical_drops_tracking_params(client, homepage_posts):
    response = client.get("/?utm_source=pinterest&fbclid=abc123")
    assert canonical(response) == f"{APEX}/"


@pytest.mark.django_db
def test_canonical_keeps_page_number_from_two(client, homepage_posts):
    response = client.get("/?page=2&utm_source=pinterest")
    assert canonical(response) == f"{APEX}/?page=2"


@pytest.mark.django_db
def test_pillar_canonical_keeps_page_number(client, pillar):
    response = client.get(f"/pillar/{pillar.slug}/?page=3")
    assert canonical(response) == f"{APEX}/pillar/{pillar.slug}/?page=3"


@pytest.mark.django_db
def test_canonical_uses_apex_whatever_the_host(client, homepage_posts):
    # www is redirected by WWWRedirectMiddleware, so use another live host
    response = client.get("/", HTTP_HOST="theroutineparent.up.railway.app")
    assert canonical(response) == f"{APEX}/"


@pytest.mark.django_db
def test_non_paginated_page_ignores_page_param(client):
    response = client.get("/about/?page=3")
    assert canonical(response) == f"{APEX}/about/"


@pytest.mark.django_db
def test_post_detail_canonical_drops_query(client):
    post = make_posts(1)[0]
    response = client.get(f"{post.get_absolute_url()}?utm_source=newsletter")
    assert canonical(response) == f"{APEX}{post.get_absolute_url()}"


# --- title (unchanged behaviour) ---

@pytest.mark.django_db
def test_page_title_suffix_only_from_page_two(client, homepage_posts):
    assert "– Page" not in client.get("/").content.decode().split("</title>")[0]
    assert "– Page 2" in client.get("/?page=2").content.decode().split("</title>")[0]
