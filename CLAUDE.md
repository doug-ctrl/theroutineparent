# ModernMuse — Django Blog

A productivity and personal growth blog for modern parents.

## Quick Commands
- Install deps: `uv sync`
- Run dev server: `uv run python manage.py runserver`
- Run tests: `uv run pytest`
- Run single test: `uv run pytest blog/tests/test_models.py -v`
- Make migrations: `uv run python manage.py makemigrations`
- Apply migrations: `uv run python manage.py migrate`
- Create superuser: `uv run python manage.py createsuperuser`
- Django shell: `uv run python manage.py shell`

## Tech Stack
- Python 3.12+ / Django 5.x
- django-taggit (post tagging)
- django-ckeditor-5 (rich text editor)
- SQLite (local database)
- uv (package manager)
- pytest + pytest-django (testing)

## Project Structure
- `config/` — Django project settings and root URL config
- `blog/` — Main blog app (posts, pillars, comments, newsletter)
- `accounts/` — User registration and profiles
- `templates/` — HTML templates (Django template language)
- `templates/base.html` — Base template all pages extend
- `templates/blog/` — Blog templates (post_list, post_detail, pillar_posts)
- `templates/pages/` — Static pages (about, contact)
- `templates/partials/` — Reusable components (post_card, sidebar, newsletter_form)
- `static/css/` — Stylesheets
- `static/js/` — JavaScript
- `static/images/` — Site images and icons
- `media/` — Uploaded content (post images)

## Content Pillars
The blog has 4 content pillars (Pillar model):
1. Parent Productivity — time management, planning, routines
2. Raising Independent Kids — responsibility, curiosity, structure
3. Personal Growth for Parents — learning, identity, goals
4. Real Life Systems — calendars, chores, family organization

## Brand Voice
ModernMuse content should feel: honest, reflective, encouraging,
practical, and relatable. Real-life experiences, not idealized advice.
Written from the perspective of a parent with two kids (ages 6 and 9).

## Code Style
- Use class-based views (ListView, DetailView, CreateView)
- Models must have __str__ and get_absolute_url methods
- Templates extend base.html using {% extends %} and {% block %}
- Keep views thin — logic goes in model methods or services
- Use Django forms for all user input
- All images must have alt text for accessibility

## Naming Conventions
- Models: PascalCase singular (Post, Pillar, Comment)
- URLs: kebab-case (post-detail, pillar-posts)
- Templates: snake_case (post_list.html, post_detail.html)

## Testing
- pytest-django with @pytest.mark.django_db
- Test models, views, and forms
- Use factory functions for test data