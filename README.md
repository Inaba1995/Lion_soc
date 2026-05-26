# MiniSocial — Simple Social Network on Django

A minimal but functional social network built with Django: posts, likes, comments, follows, private messages, and notifications.

## Features

- **Auth** — register, login, logout
- **Posts** — create, delete, attach images
- **Feed** — posts from users you follow
- **Likes** — AJAX toggle without page reload
- **Comments** — inline under each post
- **Follows** — follow/unfollow users
- **Profiles** — user page with stats
- **Notifications** — likes, comments, follows, messages
- **Private Messages** — conversations between users
- **Search** — search posts and users
- **Admin Panel** — full CRUD for all models

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000

## Project Structure

```
minisocial/
├── config/           # Settings, URLs, WSGI
├── social/           # Core app: posts, likes, comments, follows
├── notifications/    # In-app notifications
├── messaging/        # Private messages
├── templates/        # Base template
└── manage.py
```

## Models

| Model | Fields |
|---|---|
| Post | user, text (1000), image, timestamps |
| Like | user, post (unique_together) |
| Comment | user, post, text (500), timestamp |
| Follow | follower, following (unique_together) |
| Notification | recipient, sender, type, text, link, is_read |
| Conversation | participants (M2M) |
| Message | conversation, sender, text, is_read, timestamp |
