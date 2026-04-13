# The Routine Parent — Django Blog

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
The Routine Parent content should feel: honest, reflective, encouraging,
practical, and relatable. Real-life experiences, not idealized advice.
Written from the perspective of a parent with two kids (ages 6 and 9).
Kids' names: Cataleya (daughter, 9) and Enzo (son, 6). Use their names
naturally in posts rather than "my daughter" or "my son" throughout.

## Published Posts (avoid repeating openings, phrases, or structures)
1. Why Productivity Looks Different When You're a Parent — intro/welcome post, conceptual
2. 7 Habits That Help Me Stay Present With My Kids — opens with Cataleya catching Douglas distracted
3. The Weekly Planning System That Keeps Our Family Organized — opens with Tuesday night kitchen chaos
4. Teaching Kids Responsibility: What Works for Our Family — opens with Enzo leaving lunch box at school
5. My Morning Routine Before the Kids Wake Up — opens with 5:45 AM alarm negotiation
6. The Family Calendar System We Actually Use — opens with dropping Enzo at football on wrong day
7. Activities That Help Kids Become More Independent — opens with reflection on nine years of parenting
8. How I Balance Personal Growth With Parenting — opens with 9:47 PM Tuesday night kitchen scene

### Avoid reusing these patterns
- Opening with a specific time of day (e.g. "It was 9:47 PM") — used in post 8
- Opening with a child doing something at bedtime — used in post 8
- Opening with a forgotten or misplaced item — used in posts 3 and 4
- Opening with a parenting mistake or wrong-day scenario — used in post 6
- "Spoiler:" in the title — used in post 8
- "The chaos doesn't end" or similar phrasing — used in post 8
- Ending with a callback to the opening scene — used in posts 5 and 8
- Starting with "For years I thought..." — used in post 1

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
