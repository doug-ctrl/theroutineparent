# The Routine Parent — Technical Documentation

**theroutineparent.com**
A productivity and personal growth blog for modern parents.

Last updated: April 2, 2026

---

## 1. Project Overview

The Routine Parent is a full-stack blog platform built with Django and deployed on Railway. The blog features four content pillars (Parent Productivity, Raising Independent Kids, Personal Growth for Parents, Real Life Systems), a rich text editor, search, newsletter signups with free downloadable templates, comments, social sharing, contact form, dark mode, affiliate marketing integration, and Google Analytics integration.

**Live URL:** https://www.theroutineparent.com
**GitHub Repository:** https://github.com/doug-ctrl/theroutineparent (private)
**Admin Panel:** https://www.theroutineparent.com/admin/

---

## 2. Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.11 | Core programming language |
| Framework | Django 5.2 | Full-stack web framework |
| Database | PostgreSQL | Production database (Railway) |
| Database (local) | SQLite | Local development database |
| Rich Text Editor | CKEditor 5 | Blog post formatting (bold, headings, lists, links, source editing) |
| Tagging | django-taggit | Post tagging system |
| Image Handling | Pillow | Image processing for featured images |
| Static Files | WhiteNoise | Serves static files in production |
| Media Storage | Cloudflare R2 | Stores PDF downloads and media files in production |
| Object Storage Client | boto3 + django-storages | S3-compatible interface for Cloudflare R2 |
| WSGI Server | Gunicorn | Production web server |
| Database URL | dj-database-url | Parses DATABASE_URL for PostgreSQL connection |
| HTTP Client | requests | Used for serving PDF downloads from R2 |
| Environment Variables | python-dotenv | Manages secrets (SECRET_KEY, DEBUG) |
| Package Manager | uv (local), pip (production) | Python dependency management |
| IDE | PyCharm | Development environment |
| Version Control | Git & GitHub (private repo) | Source code management |
| AI Development | Claude Code | Custom slash commands for development workflow |
| Hosting | Railway | Production server (auto-deploy from GitHub) |
| Domain Registrar | Namecheap | Custom domain (theroutineparent.com) |
| SSL Certificate | Let's Encrypt | HTTPS encryption (auto-renewed via Railway) |
| Analytics | Google Analytics 4 | Visitor tracking and insights |
| Search Console | Google Search Console | SEO monitoring and sitemap management |
| Affiliate Platform | Amazon Associates | Affiliate links (UK: theroutinepar-21, US: theroutinepar-20) |
| Affiliate Platform | Impact.com | Affiliate network (application in progress) |
| Logo Design | Canva | Brand logo creation |
| PDF Generation | ReportLab | Downloadable template creation |

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
│   ├── sitemaps.py         # Sitemap configuration for Google
│   ├── admin.py            # Admin panel configuration
│   ├── apps.py             # App configuration
│   ├── forms.py            # Comment and Contact forms
│   ├── models.py           # Data models (Pillar, Post, Comment, NewsletterSubscriber, ContactMessage)
│   ├── urls.py             # Blog URL routing
│   └── views.py            # View logic (list, detail, search, newsletter, comments, contact, downloads)
├── config/                 # Django project configuration
│   ├── settings.py         # All Django settings
│   ├── urls.py             # Root URL routing (includes sitemap, ckeditor5)
│   └── wsgi.py             # WSGI entry point for production
├── static/
│   ├── css/                # Stylesheets (currently inline in base.html)
│   ├── images/             # Logo, favicon, apple-touch-icon
│   └── js/                 # JavaScript (currently inline in base.html)
├── staticfiles/            # Collected static files for production
├── templates/
│   ├── base.html           # Base template (nav, footer, all CSS, dark mode JS)
│   ├── blog/
│   │   ├── pillar_posts.html    # Posts filtered by content pillar
│   │   ├── post_detail.html     # Individual post page
│   │   ├── post_list.html       # Homepage with all posts
│   │   └── search_results.html  # Search results page
│   ├── pages/
│   │   ├── about.html           # About page
│   │   ├── contact.html         # Contact form page
│   │   └── download.html        # Free templates download page
│   └── partials/                # Reusable template components (future use)
├── media/
│   └── downloads/          # Local copies of PDF templates (production served from R2)
│       ├── weekly_family_planner.pdf
│       └── kids_chore_chart.pdf
├── .env                    # Environment variables (SECRET_KEY, DEBUG) — NOT in Git
├── .gitignore              # Files excluded from version control
├── CLAUDE.md               # Claude Code project knowledge file
├── TECHNICAL_DOCS.md       # This technical documentation
├── railway.toml            # Railway deployment configuration
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
| excerpt | TextField(500) | Auto-generated plain text summary (HTML stripped) |
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
- `save()` — Auto-generates slug and excerpt (strips HTML tags and &nbsp;) if not provided

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
| email | EmailField (unique) | Subscriber's email (normalized to lowercase) |
| name | CharField(100) | Optional name |
| subscribed_at | DateTimeField | Auto-set on creation |
| is_active | BooleanField | Subscription status |

### ContactMessage
Messages submitted via the contact form.

| Field | Type | Description |
|---|---|---|
| name | CharField(100) | Sender's name |
| email | EmailField | Sender's email |
| subject | CharField(200) | Message subject |
| message | TextField | Message content |
| created | DateTimeField | Auto-set on creation |
| is_read | BooleanField | Read status (editable in admin) |

---

## 5. URL Routing

### Root URLs (config/urls.py)
| URL | View | Description |
|---|---|---|
| /admin/ | Django Admin | Admin panel |
| /ckeditor5/ | CKEditor 5 | Rich text editor URLs |
| /sitemap.xml | Django Sitemaps | XML sitemap for Google |
| / | Blog URLs (include) | All blog routes |

### Blog URLs (blog/urls.py)
| URL | View | Name | Description |
|---|---|---|---|
| / | PostListView | post_list | Homepage with all posts |
| /search/ | SearchView | search | Search results |
| /newsletter/ | newsletter_signup | newsletter_signup | Newsletter form handler |
| /free-planner/ | DownloadPageView | free_planner | Free templates download page |
| /download/planner/ | download_planner | download_planner | PDF download (Weekly Planner) from R2 |
| /download/chore-chart/ | download_chore_chart | download_chore_chart | PDF download (Chore Chart) from R2 |
| /post/\<slug\>/ | PostDetailView | post_detail | Individual post |
| /pillar/\<slug\>/ | PillarPostsView | pillar_posts | Posts by pillar |
| /about/ | AboutView | about | About page |
| /contact/ | ContactView | contact | Contact form |

---

## 6. Features

### Implemented
- **Homepage** — Displays all published posts with excerpts, pillar badges, reading time, and pagination (6 posts per page)
- **Post Detail Page** — Full post with rich text formatting, tags, social share buttons, related posts, and comments
- **Content Pillars** — Four category pages with filtered posts and pagination (6 per page)
- **Search** — Full-text search across post titles and body content with pagination (10 per page)
- **Newsletter Signup** — Email collection form on the homepage promoting free templates; redirects to download page on subscription; email validation and lowercase normalization; duplicate detection
- **Free Downloadable Templates** — Two PDF templates (Weekly Family Planner, Kids' Chore Chart) available at /free-planner/ after newsletter signup; served from Cloudflare R2
- **Tip Boxes** — Styled callout boxes in post content using `.tip-box` CSS class; added via CKEditor Source view using `<div class="tip-box">...</div>`
- **Comments** — Reader comments with name, email, and moderation via admin panel
- **Contact Page** — Contact form with name, email, subject, and message; messages stored in database and manageable via admin panel with read/unread status
- **Social Sharing** — Share buttons for Twitter, Facebook, LinkedIn, and WhatsApp
- **Related Posts** — Shows up to 3 posts from the same pillar at the bottom of each post
- **Rich Text Editor** — CKEditor 5 in admin panel with bold, italic, headings, lists, links, block quotes, and Source editing (HTML) enabled
- **Mobile Responsive** — Hamburger menu navigation on screens under 768px
- **Dark Mode** — Toggle button (moon/sun icon) in navigation bar; full dark theme with deep navy colours; preference saved to cookie for persistence across pages and sessions
- **About Page** — Static information page
- **Google Analytics** — GA4 tracking with Measurement ID G-TFQPTC1VVE; linked to Google Search Console
- **Google Search Console** — Sitemap submitted; search performance monitoring; linked to Google Analytics
- **Sitemap** — Auto-generated XML sitemap at /sitemap.xml covering posts, pillars, and static pages
- **Affiliate Marketing** — Amazon Associates accounts active (UK, US, EU); Impact.com application in progress for Skylight Calendar
- **Favicon** — Custom clock icon matching the blog logo
- **Logo** — Custom designed logo in navigation bar
- **Production Security** — All `manage.py check --deploy` tests passing with zero issues

### Not Yet Implemented
- Email sending for newsletter subscribers (Mailchimp or ConvertKit)
- RSS feed for syndication
- Open Graph and Twitter card meta tags for social media previews
- Comment moderation enhancements (honeypot field, approval before display)
- Move CSS from inline to external stylesheet
- Amazon Associates affiliate links added to existing posts
- Affiliate disclosure added to all posts with links

---

## 7. Monetisation

### Affiliate Marketing
- **Amazon Associates UK:** theroutinepar-21 (associates.amazon.co.uk)
- **Amazon Associates US:** theroutinepar-20 (affiliate-program.amazon.com)
- **Amazon Associates Spain:** theroutinep05-21
- **Amazon Associates France:** theroutinep02-21
- **Amazon Associates Germany:** theroutinep06-21
- **Amazon Associates Italy:** theroutinep0c-21
- **Impact.com:** Publisher application in progress (for Skylight Calendar affiliate programme)
- **Strategy:** Recommend products genuinely used in posts; include affiliate disclosure at bottom of posts
- **Disclosure text:** "This post contains affiliate links. If you purchase through them, I may earn a small commission at no extra cost to you. I only recommend products I genuinely use and believe in."

### Free Downloads (Lead Magnets)
- **Weekly Family Planner** — A4 printable PDF with 7-day grid, must-do list, dinner plan, kids' check-in, don't forget section, notes & wins
- **Kids' Weekly Chore Chart** — A4 printable PDF with 10 chore rows, daily checkboxes, star tracker, weekly reward section
- **Storage:** Both PDFs stored on Cloudflare R2 at `theroutineparent-media` bucket
- **Public URL:** https://pub-53c2d8846d17472f9a9fc9195eba2c02.r2.dev/downloads/
- **Delivery:** Subscribers redirected to /free-planner/ page after newsletter signup; downloads served via Django views that fetch from R2
- **Purpose:** Grow email list for future monetisation (paid template bundles, sponsored content)

### Future Monetisation Plans
- Paid template bundles (e.g. "Family Organisation Pack")
- Digital downloads via Gumroad or Payhip
- Sponsored posts (once traffic reaches 5,000–10,000 monthly page views)
- Display ads via Mediavine (requires 50,000 monthly sessions)

### Monetisation Milestones
- **Now:** Affiliate links in content + free downloads to grow email list
- **500+ subscribers:** Launch paid template bundle
- **5,000+ monthly views:** Approach brands for sponsored posts
- **50,000+ monthly sessions:** Apply for Mediavine display ads

---

## 8. Hosting & Deployment

### Production Environment
- **Platform:** Railway (EU server — europe-west4)
- **Project name:** accurate-perfection
- **URL:** https://www.theroutineparent.com
- **Railway URL:** https://theroutineparent-production.up.railway.app
- **Python Version:** 3.11
- **Web Server:** Gunicorn

### Railway Services
| Service | Type | Details |
|---|---|---|
| theroutineparent | Web service | Django app, auto-deployed from GitHub |
| Postgres | Database | PostgreSQL, persistent volume (postgres-volume) |

### Railway Environment Variables
| Variable | Description |
|---|---|
| SECRET_KEY | Django secret key |
| DEBUG | False in production |
| DATABASE_URL | PostgreSQL connection string (internal Railway URL) |
| R2_ACCESS_KEY_ID | Cloudflare R2 access key |
| R2_SECRET_ACCESS_KEY | Cloudflare R2 secret key |
| R2_BUCKET_NAME | theroutineparent-media |
| R2_ENDPOINT_URL | https://8d74b21c045d7759a6e1b63c81da8de0.r2.cloudflarestorage.com |
| R2_PUBLIC_URL | pub-53c2d8846d17472f9a9fc9195eba2c02.r2.dev |

### Railway Deployment Configuration (railway.toml)
```toml
[deploy]
startCommand = "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn --bind 0.0.0.0:$PORT config.wsgi:application"
```

### SSL Certificate
- **Type:** Auto-renewed Let's Encrypt certificate
- **Managed by:** Railway

### Cloudflare R2 Media Storage
- **Account:** fastlinkvideo@gmail.com
- **Bucket:** theroutineparent-media (Western Europe)
- **Public Development URL:** https://pub-53c2d8846d17472f9a9fc9195eba2c02.r2.dev
- **S3 Endpoint:** https://8d74b21c045d7759a6e1b63c81da8de0.r2.cloudflarestorage.com
- **API Token:** theroutineparent-r2 (Object Read & Write, all buckets)
- **Contents:** downloads/weekly_family_planner.pdf, downloads/kids_chore_chart.pdf

---

## 9. Domain & DNS Configuration

### Domain
- **Registrar:** Namecheap
- **Domain:** theroutineparent.com
- **Primary URL:** https://www.theroutineparent.com

### DNS Records (Namecheap Advanced DNS)
| Type | Host | Value |
|---|---|---|
| CNAME | www | kiy3qxv5.up.railway.app |
| URL Redirect (301) | @ | https://www.theroutineparent.com |
| TXT | _railway-verify.www | railway-verify=de11a04aa98f08165891c583a8222e722d8b3d270c3742c578df0fe69ea47675 |

---

## 10. Security

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
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Required for Railway
```

### Environment Variables
Secrets are stored in `.env` files locally (excluded from Git via .gitignore) and as Railway environment variables in production:
- `SECRET_KEY` — Django secret key (unique per environment)
- `DEBUG` — True locally, False in production
- `DATABASE_URL` — PostgreSQL connection string (Railway only)
- R2 credentials (Railway only)

### Built-in Django Protections
- CSRF protection on all forms
- SQL injection prevention via ORM
- XSS protection via template auto-escaping
- Clickjacking protection via X-Frame-Options middleware
- Password hashing for admin accounts
- Email validation on newsletter signup and contact form

### GitHub Repository
- **Visibility:** Private
- **Authentication:** Personal Access Token with `repo` scope
- **Credential storage:** `git config credential.helper store` on Mac

---

## 11. Analytics & SEO

### Google Analytics 4
- **Property:** The Routine Parent
- **Measurement ID:** G-TFQPTC1VVE
- **Stream URL:** https://www.theroutineparent.com
- **Dashboard:** https://analytics.google.com
- **Linked to:** Google Search Console

### Google Search Console
- **Property:** https://www.theroutineparent.com (URL prefix)
- **Verified via:** Google Analytics
- **Sitemap:** Submitted at /sitemap.xml (resubmitted April 2, 2026 after Railway migration)
- **Dashboard:** https://search.google.com/search-console
- **Indexing status:** 3 pages indexed, 9 pending (as of April 2, 2026)

### Sitemap
- **URL:** https://www.theroutineparent.com/sitemap.xml
- **Includes:** All published posts, all pillar pages, homepage, and about page
- **Auto-generated:** Via Django's `django.contrib.sitemaps` framework

### Tracked Metrics
- Page views and unique visitors
- Traffic sources (organic, direct, social, referral)
- Popular posts and pages
- User location and device type
- Session duration and engagement
- Scroll depth and outbound clicks
- Search queries and landing pages (via Search Console link)

---

## 12. Development Workflow

### Local Development
1. Open project in PyCharm
2. Make code changes
3. Test locally: `uv run python manage.py runserver`
4. Visit http://127.0.0.1:8000 to verify

### Deployment Process (Railway — Auto-deploy)
1. Commit and push:
```bash
git add .
git commit -m "description of changes"
git push
```
Railway automatically detects the push and redeploys. No manual steps required.

2. If you need to run management commands against the Railway database:
```bash
DATABASE_URL="postgresql://postgres:<password>@interchange.proxy.rlwy.net:45064/railway" uv run python manage.py <command>
```
Note: Use the `DATABASE_PUBLIC_URL` from Railway's Postgres service variables for the connection string.

### Railway CLI
The Railway CLI is installed and linked to the project:
```bash
railway login
railway link  # Select: accurate-perfection > production > theroutineparent
railway run uv run python manage.py <command>  # Run commands in Railway environment
```

### Content Publishing
1. Draft a post using Claude Code: `/draft Topic Name`
2. Optimize for SEO: `/seo Topic Name`
3. Visit https://www.theroutineparent.com/admin/
4. Create new post, paste content, set pillar, tags, meta description
5. Format subheadings as Heading 2 in CKEditor
6. Add tip boxes using Source view: `<div class="tip-box">Tip text here.</div>`
7. Set status to Published and save

---

## 13. Claude Code Integration

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

## 14. Published Content

### Blog Posts (8 total)
| # | Title | Pillar | Slug | Published |
|---|---|---|---|---|
| 1 | Why Productivity Looks Different When You're a Parent | Parent Productivity | why-productivity-looks-different-when-youre-a-parent | Mar 13, 2026 |
| 2 | 7 Habits That Help Me Stay Present With My Kids | Personal Growth for Parents | 7-habits-that-help-me-stay-present-with-my-kids | Mar 15, 2026 |
| 3 | The Weekly Planning System That Keeps Our Family Organized | Real Life Systems | the-weekly-planning-system-that-keeps-our-family-organized | Mar 18, 2026 |
| 4 | Teaching Kids Responsibility: What Works for Our Family | Raising Independent Kids | teaching-kids-responsibility-what-works-for-our-family | Mar 23, 2026 |
| 5 | My Morning Routine Before the Kids Wake Up | Parent Productivity | morning-routine-before-the-kids-wake-up | Mar 24, 2026 |
| 6 | The Family Calendar System We Actually Use | Real Life Systems | the-family-calendar-system-we-actually-use | Mar 27, 2026 |
| 7 | Activities That Help Kids Become More Independent | Raising Independent Kids | activities-that-help-kids-become-more-independent | Mar 31, 2026 |

### Family Context
- **Daughter:** Cataleya, age 9
- **Son:** Enzo, age 6
- Both are referenced naturally throughout blog posts for authenticity

### Remaining Post Ideas
1. How I Balance Personal Growth With Parenting
2. What Six Years of Parenting Has Taught Me
3. The 30-Minute Reset Routine for Busy Parents
4. Why Parents Need Personal Goals Too
5. Simple Evening Routines for Calm School Nights

---

## 15. Dependencies

### Production Dependencies
| Package | Version | Purpose |
|---|---|---|
| django | 5.2.12 | Web framework |
| django-taggit | 6.1.0 | Post tagging |
| django-ckeditor-5 | 0.2.20 | Rich text editor |
| pillow | 12.1.1 | Image processing |
| python-dotenv | — | Environment variable management |
| whitenoise | 6.12.0 | Static file serving in production |
| gunicorn | 25.3.0 | Production WSGI server |
| psycopg2-binary | 2.9.11 | PostgreSQL adapter |
| dj-database-url | — | Database URL parsing |
| django-storages | — | S3-compatible media storage backend |
| boto3 | — | AWS/R2 S3 client |
| requests | — | HTTP client for PDF downloads from R2 |

### Development Dependencies
| Package | Version | Purpose |
|---|---|---|
| pytest | 9.0.2 | Testing framework |
| pytest-django | 4.12.0 | Django testing integration |

---

## 16. Future Roadmap

### Features
- Email integration for newsletter subscribers (Mailchimp or ConvertKit)
- RSS feed for syndication
- Open Graph and Twitter card meta tags for social media previews
- Comment moderation enhancements (honeypot field, approval before display)
- Move CSS from inline to external stylesheet
- Custom domain for Cloudflare R2 bucket (replace public dev URL)

### Content & Growth
- Continue publishing weekly blog posts (5 remaining ideas)
- Add Amazon Associates affiliate links to all existing posts
- Add affiliate disclosure to all posts with links
- Create additional downloadable templates (morning routine checklist, meal planning sheet, evening routine checklist)
- Bundle templates into paid product once 3–4 templates exist
- Complete Impact.com publisher application for Skylight Calendar affiliate link

### Monetisation Milestones
- **Now:** Affiliate links in content + free downloads to grow email list
- **500+ subscribers:** Launch paid template bundle
- **5,000+ monthly views:** Approach brands for sponsored posts
- **50,000+ monthly sessions:** Apply for Mediavine display ads
