# The Routine Parent — Technical Documentation

**theroutineparent.com**
A productivity and personal growth blog for modern parents.

Last updated: March 2026

---

## 1. Project Overview

The Routine Parent is a full-stack blog platform built with Django and deployed on PythonAnywhere. The blog features four content pillars (Parent Productivity, Raising Independent Kids, Personal Growth for Parents, Real Life Systems), a rich text editor, search, newsletter signups, comments, social sharing, and Google Analytics integration.

**Live URL:** https://www.theroutineparent.com
**GitHub Repository:** https://github.com/doug-ctrl/theroutineparent
**Admin Panel:** https://www.theroutineparent.com/admin/

---

## 2. Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.11 | Core programming language |
| Framework | Django 5.2 | Full-stack web framework |
| Database | SQLite | Local and production database |
| Rich Text Editor | CKEditor 5 | Blog post formatting (bold, headings, lists, links) |
| Tagging | django-taggit | Post tagging system |
| Image Handling | Pillow | Image processing for featured images |
| Static Files | WhiteNoise | Serves static files in production |
| Environment Variables | python-dotenv | Manages secrets (SECRET_KEY, DEBUG) |
| Package Manager | uv (local), pip (production) | Python dependency management |
| IDE | PyCharm | Development environment |
| Version Control | Git & GitHub | Source code management |
| AI Development | Claude Code | Custom slash commands for development workflow |
| Hosting | PythonAnywhere (EU) | Production server |
| Domain Registrar | Namecheap | Custom domain (theroutineparent.com) |
| SSL Certificate | Let's Encrypt | HTTPS encryption (auto-renewed) |
| Analytics | Google Analytics 4 | Visitor tracking and insights |
| Logo Design | Canva | Brand logo creation |

---

## 3. Project Structure

```
theroutineparent/
├── .claude/
│   └── commands/           # Claude Code custom slash commands
│       ├── draft.md        # Blog post drafting
│       ├── explain.md      # Code explanation
│       ├── feature.md      # Feature building
│       ├── review.md       # Code review
│       ├── seo.md          # SEO optimization
│       ├── template.md     # Template creation
│       └── test.md         # Test writing
├── accounts/               # User accounts app (future use)
├── blog/                   # Main blog application
│   ├── migrations/         # Database migrations
│   ├── admin.py            # Admin panel configuration
│   ├── apps.py             # App configuration
│   ├── forms.py            # Comment form
│   ├── models.py           # Data models (Pillar, Post, Comment, NewsletterSubscriber)
│   ├── urls.py             # Blog URL routing
│   └── views.py            # View logic (list, detail, search, newsletter, comments)
├── config/                 # Django project configuration
│   ├── settings.py         # All Django settings
│   ├── urls.py             # Root URL routing
│   └── wsgi.py             # WSGI entry point for production
├── static/
│   ├── css/                # Stylesheets (currently inline in base.html)
│   ├── images/             # Logo, favicon
│   └── js/                 # JavaScript (currently inline in base.html)
├── staticfiles/            # Collected static files for production
├── templates/
│   ├── base.html           # Base template (nav, footer, styles)
│   ├── blog/
│   │   ├── pillar_posts.html    # Posts filtered by content pillar
│   │   ├── post_detail.html     # Individual post page
│   │   ├── post_list.html       # Homepage with all posts
│   │   └── search_results.html  # Search results page
│   ├── pages/
│   │   └── about.html           # About page
│   └── partials/                # Reusable template components (future use)
├── media/                  # User-uploaded content
├── .env                    # Environment variables (SECRET_KEY, DEBUG) — NOT in Git
├── .gitignore              # Files excluded from version control
├── CLAUDE.md               # Claude Code project knowledge file
├── manage.py               # Django management script
├── pyproject.toml          # Project metadata and dependencies
└── uv.lock                 # Dependency lock file
```

---

## 4. Data Models

### Pillar
Represents the four content categories of the blog.

| Field | Type | Description |
|---|---|---|
| name | CharField(100) | Pillar name (e.g. "Parent Productivity") |
| slug | SlugField(100) | URL-friendly identifier |
| description | TextField | Brief description of the pillar |
| icon | CharField(50) | Optional icon or emoji |
| order | PositiveIntegerField | Display order |

### Post
The core blog post model.

| Field | Type | Description |
|---|---|---|
| title | CharField(250) | Post title |
| slug | SlugField(250) | URL-friendly identifier (auto-generated) |
| subtitle | CharField(300) | Optional subtitle |
| body | CKEditor5Field | Rich text post content |
| excerpt | TextField(500) | Auto-generated plain text summary |
| pillar | ForeignKey(Pillar) | Content pillar category |
| tags | TaggableManager | Post tags via django-taggit |
| featured_image | ImageField | Optional main image |
| featured_image_alt | CharField(250) | Image alt text for accessibility |
| author | ForeignKey(User) | Post author |
| status | CharField (Draft/Review/Published) | Publication status |
| is_featured | BooleanField | Featured on homepage flag |
| publish | DateTimeField | Publication date |
| created | DateTimeField | Auto-set on creation |
| updated | DateTimeField | Auto-set on save |
| meta_description | CharField(160) | SEO meta description |

**Custom methods:**
- `reading_time` — Estimates read time based on word count (200 words/minute)
- `save()` — Auto-generates slug and excerpt (strips HTML) if not provided

### Comment
Reader comments on posts.

| Field | Type | Description |
|---|---|---|
| post | ForeignKey(Post) | Associated post |
| name | CharField(80) | Commenter's name |
| email | EmailField | Commenter's email (not displayed) |
| body | TextField | Comment content |
| created | DateTimeField | Auto-set on creation |
| active | BooleanField | Moderation flag |

### NewsletterSubscriber
Email subscribers for the blog newsletter.

| Field | Type | Description |
|---|---|---|
| email | EmailField (unique) | Subscriber's email |
| name | CharField(100) | Optional name |
| subscribed_at | DateTimeField | Auto-set on creation |
| is_active | BooleanField | Subscription status |

---

## 5. Features

### Implemented
- **Homepage** — Displays all published posts with excerpts, pillar badges, reading time, and pagination (6 posts per page)
- **Post Detail Page** — Full post with rich text formatting, tags, social share buttons, related posts, and comments
- **Content Pillars** — Four category pages with filtered posts
- **Search** — Full-text search across post titles and body content
- **Newsletter Signup** — Email collection form on the homepage with duplicate detection
- **Comments** — Reader comments with name, email, and moderation via admin panel
- **Social Sharing** — Share buttons for Twitter, Facebook, LinkedIn, and WhatsApp
- **Related Posts** — Shows up to 3 posts from the same pillar at the bottom of each post
- **Rich Text Editor** — CKEditor 5 in admin panel with bold, italic, headings, lists, links, block quotes
- **Mobile Responsive** — Hamburger menu navigation on screens under 768px
- **About Page** — Static information page
- **Google Analytics** — GA4 tracking with Measurement ID G-TFQPTC1VVE
- **Favicon** — Custom clock icon matching the blog logo
- **Logo** — Custom designed logo in navigation bar

### Not Yet Implemented
- Email sending for newsletter subscribers
- RSS feed
- Sitemap and SEO meta tags in templates
- Contact page
- Dark mode
- Comment moderation notifications
- Social media preview images (Open Graph tags)

---

## 6. Hosting & Deployment

### Production Environment
- **Platform:** PythonAnywhere (EU server)
- **Account:** theroutineparent
- **URL:** https://www.theroutineparent.com
- **Python Version:** 3.11
- **Web App Type:** Manual configuration (WSGI)

### Server Paths
| Item | Path |
|---|---|
| Source code | /home/theroutineparent/theroutineparent |
| Virtual environment | /home/theroutineparent/theroutineparent/.venv |
| WSGI config | /var/www/theroutineparent_eu_pythonanywhere_com_wsgi.py |
| Static files | /home/theroutineparent/theroutineparent/staticfiles |
| Media files | /home/theroutineparent/theroutineparent/media |
| Database | /home/theroutineparent/theroutineparent/db.sqlite3 |
| Environment file | /home/theroutineparent/theroutineparent/.env |

### Static File Configuration
| URL | Directory |
|---|---|
| /static/ | /home/theroutineparent/theroutineparent/staticfiles |
| /media/ | /home/theroutineparent/theroutineparent/media |

### WSGI Configuration
```python
import os
import sys

path = '/home/theroutineparent/theroutineparent'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### SSL Certificate
- **Type:** Auto-renewed Let's Encrypt certificate
- **Managed by:** PythonAnywhere

---

## 7. Domain & DNS Configuration

### Domain
- **Registrar:** Namecheap
- **Domain:** theroutineparent.com
- **Primary URL:** https://www.theroutineparent.com

### DNS Records (Namecheap Advanced DNS)
| Type | Host | Value |
|---|---|---|
| CNAME | www | webapp-54762.eu.pythonanywhere.com. |
| URL Redirect (301) | @ | https://www.theroutineparent.com |

The CNAME record points the www subdomain to PythonAnywhere's server. The URL redirect ensures visitors who type theroutineparent.com (without www) are redirected to the secure www version.

---

## 8. Security

### Production Security Settings (active when DEBUG=False)
```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Security Check
Running `python manage.py check --deploy` on production returns: **System check identified no issues (0 silenced).**

### Environment Variables
Secrets are stored in `.env` files (excluded from Git via .gitignore):
- `SECRET_KEY` — Django secret key (unique per environment)
- `DEBUG` — True locally, False in production

### Built-in Django Protections
- CSRF protection on all forms
- SQL injection prevention via ORM
- XSS protection via template auto-escaping
- Clickjacking protection via X-Frame-Options middleware
- Password hashing for admin accounts

---

## 9. Analytics

### Google Analytics 4
- **Property:** The Routine Parent
- **Measurement ID:** G-TFQPTC1VVE
- **Stream URL:** https://www.theroutineparent.com
- **Dashboard:** https://analytics.google.com

### Tracked Metrics
- Page views and unique visitors
- Traffic sources (organic, direct, social, referral)
- Popular posts and pages
- User location and device type
- Session duration and engagement
- Scroll depth and outbound clicks

---

## 10. Development Workflow

### Local Development
1. Open project in PyCharm
2. Make code changes
3. Test locally: `uv run python manage.py runserver`
4. Visit http://127.0.0.1:8000 to verify

### Deployment Process
1. Commit and push:
```bash
git add .
git commit -m "description of changes"
git push
```

2. On PythonAnywhere Bash console:
```bash
cd theroutineparent
git stash        # If local settings.py changes exist
git pull
```

3. If models changed:
```bash
source .venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

4. If static files changed:
```bash
source .venv/bin/activate
python manage.py collectstatic --noinput
```

5. Click **Reload** on PythonAnywhere Web tab

### Content Publishing
1. Draft a post using Claude Code: `/draft Topic Name`
2. Optimize for SEO: `/seo Topic Name`
3. Visit https://www.theroutineparent.com/admin/
4. Create new post, paste content, set pillar, tags, meta description
5. Format subheadings as Heading 2 in CKEditor
6. Set status to Published and save

---

## 11. Claude Code Integration

### CLAUDE.md
The project root contains a `CLAUDE.md` file that teaches Claude Code about the project's tech stack, structure, conventions, content pillars, and brand voice. Claude reads this automatically at the start of every session.

### Custom Slash Commands (.claude/commands/)
| Command | File | Purpose |
|---|---|---|
| /draft | draft.md | Drafts blog posts in The Routine Parent's voice |
| /seo | seo.md | SEO optimization for titles, meta descriptions, keywords |
| /review | review.md | Code review for Django best practices and security |
| /test | test.md | Writes pytest tests for models, views, and forms |
| /feature | feature.md | Builds complete features end to end |
| /template | template.md | Creates or updates HTML templates |
| /explain | explain.md | Explains code or concepts for beginners |

---

## 12. Dependencies

### Production Dependencies
| Package | Version | Purpose |
|---|---|---|
| django | 5.2.12 | Web framework |
| django-taggit | 6.1.0 | Post tagging |
| django-ckeditor-5 | 0.2.20 | Rich text editor |
| pillow | 12.1.1 | Image processing |
| python-dotenv | — | Environment variable management |
| whitenoise | — | Static file serving in production |

### Development Dependencies
| Package | Version | Purpose |
|---|---|---|
| pytest | 9.0.2 | Testing framework |
| pytest-django | 4.12.0 | Django testing integration |

---

## 13. Future Roadmap

- Email integration for newsletter subscribers (Mailchimp or ConvertKit)
- RSS feed for syndication
- Sitemap and enhanced SEO meta tags
- Contact page with form
- Dark mode toggle
- Open Graph and Twitter card meta tags for social media previews
- Comment moderation email notifications
- Google Search Console integration
- Move CSS from inline to external stylesheet
- Consider PostgreSQL migration for production scalability
