# Blog API

A Django REST API for publishing blog posts with rich text content, categories, and featured images. Deployed on Namecheap Stellar Plus using MySQL-compatible hosting.

## Features

- Public, read-only post endpoints
- Post details retrieved by slug
- Category filtering
- Pagination: 10 posts per page
- Draft and published statuses
- Django admin for managing posts and categories
- TinyMCE rich text editor
- Featured image uploads and alternative text
- CORS support for React integration

Only published posts appear in the public API. Content management happens through Django admin.

## Tech Stack

- Python 3.12
- Django 5.2
- Django REST Framework
- MySQL Connector/Python
- SQLite for local development
- TinyMCE
- Pillow
- WhiteNoise
- django-cors-headers
- python-dotenv

## Live URLs (for testing)

| Resource | URL |
|----------|-----|
| Posts | https://api.yusufbusoyriy.com.ng/api/posts/ |
| Categories | https://api.yusufbusoyriy.com.ng/api/categories/ |
| Admin | https://api.yusufbusoyriy.com.ng/admin/ |

## API Endpoints

All public endpoints accept `GET`, `HEAD`, and `OPTIONS`. Authentication is not required to read published content.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts/` | List published posts |
| GET | `/api/posts/?page=2` | Retrieve another page |
| GET | `/api/posts/?category=technology` | Filter by category slug |
| GET | `/api/posts/<slug>/` | Retrieve a published post |
| GET | `/api/categories/` | List categories |

A missing or draft post returns `404` through the post detail endpoint.

### Post List Response

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "My First Blog Post",
      "slug": "my-first-blog-post",
      "excerpt": "An introduction to the blog.",
      "content": "<p>This is the full article.</p>",
      "image": "https://api.yusufbusoyriy.com.ng/media/posts/2026/10/cover.jpg",
      "image_alt": "A laptop on a desk",
      "author": "admin",
      "category": {
        "id": 1,
        "name": "Technology",
        "slug": "technology"
      },
      "created_at": "2026-10-01T03:00:00Z",
      "updated_at": "2026-10-01T03:30:00Z"
    }
  ]
}
```

The detail endpoint returns a single post object without the pagination wrapper. The categories endpoint returns an array of category objects.

## Project Structure

```text
.
├── blog/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── passenger_wsgi.py
├── requirements.txt
└── .gitignore
```

The `.env`, local database, collected static files, and uploaded media are excluded from version control.

## Local Setup

### 1. Clone the Repository

Replace the placeholders with your repository details:

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` beside `manage.py`:

```dotenv
DJANGO_SECRET_KEY="your-local-secret-key"
DJANGO_DEBUG=True
USE_SQLITE=True

DB_NAME=unused
DB_USER=unused
DB_PASSWORD=unused
DB_HOST=localhost
```

Generate a secret key with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

The database placeholders are needed because the settings load the MySQL configuration before applying the SQLite override.

### 5. Create Database Tables and an Admin Account

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Start the Server

```bash
python manage.py runserver
```

Visit:

- API: http://127.0.0.1:8000/api/posts/
- Admin: http://127.0.0.1:8000/admin/

## Publishing Posts

1. Sign in to Django admin.
2. Create a category if needed.
3. Add a post with a title and unique slug.
4. Write a plain text excerpt.
5. Write the article using the rich text editor.
6. Select an author and optional category.
7. Upload an optional featured image and describe it in `image_alt`.
8. Set the status to **Published** and save.

Use complete external link addresses, such as `https://example.com`, in the editor.

## React Integration

Fetch the published post list:

```javascript
const response = await fetch(
  "https://api.yusufbusoyriy.com.ng/api/posts/"
);

if (!response.ok) {
  throw new Error(`Request failed: ${response.status}`);
}

const data = await response.json();
const posts = data.results;
```

Fetch a single article:

```javascript
const response = await fetch(
  `https://api.yusufbusoyriy.com.ng/api/posts/${encodeURIComponent(slug)}/`
);

if (!response.ok) {
  throw new Error(`Request failed: ${response.status}`);
}

const post = await response.json();
```

The `content` field contains HTML. Sanitize it before rendering in React:

```jsx
import DOMPurify from "dompurify";

<div
  dangerouslySetInnerHTML={{
    __html: DOMPurify.sanitize(post.content),
  }}
/>
```

Button links created in the editor use the `blog-button` class. Apply the corresponding styles in your frontend.

### CORS

Allowed local frontend origins are configured in Django:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

Add your deployed frontend origin when publishing the React app. Include the scheme and port where applicable, without a trailing slash.

## Namecheap Deployment

The application uses cPanel's **Setup Python App**, Python 3.12, and Passenger.

### Production Environment

Create a private `.env` in the application root:

```dotenv
DJANGO_SECRET_KEY="your-production-secret-key"
DJANGO_DEBUG=False
USE_SQLITE=False

DB_NAME="cpanel-prefix_database"
DB_USER="cpanel-prefix_user"
DB_PASSWORD="your-database-password"
DB_HOST=localhost

DJANGO_MEDIA_ROOT="/home/<cpanel-user>/<api-document-root>/media"
```

Assign the database user to the database with the required privileges.

The database backend is:

```python
"ENGINE": "mysql.connector.django"
```

MySQL Connector/Python is used because the hosting environment blocked compilation of `mysqlclient`.

### Deploy or Update

Upload the application files, including committed migration files. Keep the production `.env` on the server.

Activate the virtual environment using the command shown in **Setup Python App**, then enter the application directory.

Run:

```bash
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```

For the first deployment, create an admin account:

```bash
python manage.py createsuperuser
```

Restart the application through **Setup Python App**.

Generate migrations locally and commit them before deploying model changes.

## Static Files and Uploaded Images

- **Static files:** Collected with `collectstatic` and served through WhiteNoise.
- **Uploaded images:** Stored under `DJANGO_MEDIA_ROOT` and served by the hosting web server.
- **Local images:** Served by Django while `DEBUG=True`.

The production media directory sits inside the API domain's document root so `/media/` URLs resolve publicly. WhiteNoise does not handle uploaded media.

## Verification

After deployment, check that:

- `/api/posts/` returns `200 OK`.
- Published posts appear and drafts remain hidden.
- A post opens through its slug endpoint.
- Category filtering and pagination work.
- Admin styling and the rich text editor load.
- Uploaded image URLs open publicly.
- The React frontend can fetch the API.

## Backups and Configuration

Keep `.env` out of Git and use separate local and production secret keys.

Back up both the production database and media directory. The database stores article content and image references; the media directory stores the actual uploaded images.

Keep production `DEBUG=False`, configure the correct `ALLOWED_HOSTS`, and use HTTPS.