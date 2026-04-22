# Scheduling Tool — Setup Guide

## Files

| File | Purpose |
|------|---------|
| `config.php` | All your settings — fill this in first |
| `schema.sql` | Run once in your database to create tables |
| `setup.php` | Visit once in browser to authorize Outlook |
| `auth.php` | OAuth callback (called by Microsoft automatically) |
| `slots.php` | API: returns available time slots as JSON |
| `book.php` | API: creates the Outlook meeting |
| `index.html` | The public booking page you share with people |

---

## Step 1 — Azure App Registration

1. Go to [portal.azure.com](https://portal.azure.com) and sign in with your work account.
2. Search **App registrations** → **New registration**.
3. Name: anything (e.g. `My Scheduler`).
4. Supported account types: **Single tenant**.
5. Redirect URI: **Web** → `https://yoursite.com/scheduling/auth.php`
6. Click **Register**.
7. Copy the **Application (client) ID** and **Directory (tenant) ID** from the overview page.
8. Go to **Certificates & secrets** → **New client secret** → copy the **Value**.
9. Go to **API permissions** → **Add a permission** → **Microsoft Graph** → **Delegated** → search `Calendars.ReadWrite` → Add.

---

## Step 2 — Configure `config.php`

Fill in every blank field:

```php
define('AZURE_CLIENT_ID',     'paste-client-id-here');
define('AZURE_CLIENT_SECRET', 'paste-secret-value-here');
define('AZURE_TENANT_ID',     'paste-tenant-id-here');
define('AZURE_REDIRECT_URI',  'https://yoursite.com/scheduling/auth.php');

define('OWNER_NAME',  'Your Name');
define('OWNER_EMAIL', 'you@yourdomain.com');
define('OWNER_TIMEZONE', 'America/Chicago');  // php.net/timezones

define('DB_HOST', 'localhost');
define('DB_NAME', 'your_db');
define('DB_USER', 'your_user');
define('DB_PASS', 'your_password');
```

Adjust availability hours and `MEETING_DURATION` as needed.

---

## Step 3 — Create the Database Tables

Run `schema.sql` in your MySQL database (via phpMyAdmin or CLI):

```bash
mysql -u your_user -p your_db < schema.sql
```

---

## Step 4 — Upload Files

Upload the entire `scheduling/` folder to your web server.

---

## Step 5 — Authorize Outlook (one-time)

Visit `https://yoursite.com/scheduling/setup.php` in your browser.  
Sign in with your Microsoft work account and grant calendar access.  
You'll be redirected back and see a "Connected!" confirmation.

**After this step, delete or password-protect `setup.php`.**

---

## Step 6 — Share Your Booking Page

Send people the link:  `https://yoursite.com/scheduling/`

That's it. The page reads your live Outlook calendar, shows real open slots,
and creates Teams meetings with calendar invites for both parties automatically.

---

## Maintenance

- Tokens auto-refresh silently — no action needed.
- If you ever revoke access in Azure, run `setup.php` again.
- Bookings are logged in the `bookings` table for your records.
