<?php
// ─── Azure App Registration ───────────────────────────────────────────────────
define('AZURE_CLIENT_ID',     '9362894e-cca3-48d5-99f6-b135c6090cb4');
define('AZURE_CLIENT_SECRET', 'k4L8Q~1riXm~MpTrOEa2KLOQlbS.ZIo6vkiu5dzO');
define('AZURE_TENANT_ID',     'e6af4d4f-7ea3-4182-9d21-b6697a4abaf3');

// The redirect URI you registered in Azure (must match exactly)
define('AZURE_REDIRECT_URI',  'https://aesopacademy.org/scheduling/auth.php');

// ─── Your Details ─────────────────────────────────────────────────────────────
define('OWNER_NAME',  'Scott');
define('OWNER_EMAIL', 'scott@aesopacademy.org');

// Shown on the booking page
define('BOOKING_PAGE_TITLE',  'Schedule a Meeting');
define('BOOKING_PAGE_BLURB',  'Pick a time that works for you and I\'ll send you a calendar invite.');

// ─── Availability ─────────────────────────────────────────────────────────────
define('MEETING_DURATION',      30);          // minutes per slot
define('BUFFER_MINUTES',         5);          // gap between meetings
define('BOOKING_DAYS_AHEAD',    14);          // how far ahead visitors can book
define('MIN_NOTICE_HOURS',       4);          // earliest same/next-day booking

// Business hours (24h, your local timezone)
define('BUSINESS_HOURS_START',   9);          // 9 AM
define('BUSINESS_HOURS_END',    17);          // 5 PM
define('OWNER_TIMEZONE', 'America/Denver');   // your timezone (MDT)

// Days available: 1=Mon … 7=Sun
define('BUSINESS_DAYS', serialize([1, 2, 3, 4, 5]));

// ─── Teams Meeting ────────────────────────────────────────────────────────────
define('CREATE_TEAMS_MEETING', true);         // set false if you don't use Teams

// ─── Database ─────────────────────────────────────────────────────────────────
define('DB_HOST', 'localhost');
define('DB_NAME', 'hivetec1_scheduler');
define('DB_USER', 'hivetec1_aesop_sched');
define('DB_PASS', 'DG35zrE@FSHyn#zG');
