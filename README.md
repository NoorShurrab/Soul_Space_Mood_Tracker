# SoulSpace 

A mood tracking web application with micro-journaling and personal analytics. SoulSpace helps users build a gentler relationship with their feelings through daily check-ins, mood history, and personalized email reminders.

---

## Features

- **User Authentication** — Register, login, logout, and password reset via email
- **Daily Mood Check-in** — Choose from 8 moods with optional notes and tags
- **Personal Dashboard** — Mood calendar, streaks, average score, and most felt mood
- **Mood History** — Search and filter past logs with mood scores and tags
- **Email Reminders** — Motivational emails based on your last logged mood
- **REST API** — JSON endpoints for mood data and email reminders
- **AJAX** — Dynamic interactions without full page reloads

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django (Python) |
| Database | MySQL |
| Frontend | Tailwind CSS |
| Password Security | bcrypt (custom hasher) |
| Email | Gmail SMTP |
| Dynamic | AJAX (Fetch API) |

---


## API Endpoints

### GET `/api/moods/`
```json
{
    "logs": [
        {
            "date": "2026-06-22",
            "mood": "Happy",
            "mood_score": 4,
            "note": "Great day!"
        }
    ]
}
```

### POST `/api/send-reminder/`
```json
{
    "message": "Reminder sent successfully!"
}
```

---

## Mood Score Scale

| Mood | Score |
|------|-------|
| Amazing | 5 ⭐⭐⭐⭐⭐ |
| Happy | 4 ⭐⭐⭐⭐ |
| Relaxed | 3 ⭐⭐⭐ |
| Okay | 3 ⭐⭐⭐ |
| Tired | 2 ⭐⭐ |
| Sad | 2 ⭐⭐ |
| Anxious | 1 ⭐ |
| Angry | 1 ⭐ |

---

## Security

- bcrypt password hashing with custom Django hasher
- CSRF protection on all forms
- Session-based authentication
- Custom password reset with secure random tokens

---

## Challenges & Solutions

### 1. Custom bcrypt Hasher
**Problem:** Django's default bcrypt hasher wasn't compatible with our password verification flow.  
**Solution:** Built a custom `BcryptPasswordHasher` with proper `encode()` and `verify()` methods.

### 2. Password Reset with Custom User Model
**Problem:** Django's built-in password reset only works with `auth.User`.  
**Solution:** Built a custom reset flow using Python's `secrets` module with database cache tokens.

---

## Pages

| Page | URL |
|------|-----|
| Register | `/` |
| Login | `/login` |
| Dashboard | `/mood/dashboard/` |
| Check-in | `/mood/check-in/` |
| History | `/mood/history/` |
| About | `/mood/about/` |
| Password Reset | `/password_reset/` |

---

*Built with 💜 — SoulSpace, a gentle place to feel.*
