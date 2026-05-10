<?php
require_once dirname(__DIR__) . '/secrets.php';

// Azure App Registration
// Client and tenant IDs are identifiers; the client secret is loaded from
// environment or secrets.local.php through aesop_secret().
define('AZURE_CLIENT_ID',     aesop_secret('AESOP_AZURE_CLIENT_ID', '9362894e-cca3-48d5-99f6-b135c6090cb4'));
define('AZURE_CLIENT_SECRET', aesop_require_secret('AESOP_AZURE_CLIENT_SECRET'));
define('AZURE_TENANT_ID',     aesop_secret('AESOP_AZURE_TENANT_ID', 'e6af4d4f-7ea3-4182-9d21-b6697a4abaf3'));

// The redirect URI registered in Azure must match exactly.
define('AZURE_REDIRECT_URI',  aesop_secret('AESOP_AZURE_REDIRECT_URI', 'https://aesopacademy.org/scheduling/auth.php'));

// Owner details
define('OWNER_NAME',  aesop_secret('AESOP_OWNER_NAME', 'Scott'));
define('OWNER_EMAIL', aesop_secret('AESOP_OWNER_EMAIL', 'scott@aesopacademy.org'));

// Shown on the booking page
define('BOOKING_PAGE_TITLE',  aesop_secret('AESOP_BOOKING_PAGE_TITLE', 'Schedule a Meeting'));
define('BOOKING_PAGE_BLURB',  aesop_secret('AESOP_BOOKING_PAGE_BLURB', 'Pick a time that works for you and I\'ll send you a calendar invite.'));

// Availability
define('MEETING_DURATION',      (int)aesop_secret('AESOP_MEETING_DURATION', 30));
define('BUFFER_MINUTES',        (int)aesop_secret('AESOP_BUFFER_MINUTES', 5));
define('BOOKING_DAYS_AHEAD',    (int)aesop_secret('AESOP_BOOKING_DAYS_AHEAD', 14));
define('MIN_NOTICE_HOURS',      (int)aesop_secret('AESOP_MIN_NOTICE_HOURS', 4));
define('BUSINESS_HOURS_START',  (int)aesop_secret('AESOP_BUSINESS_HOURS_START', 9));
define('BUSINESS_HOURS_END',    (int)aesop_secret('AESOP_BUSINESS_HOURS_END', 17));
define('OWNER_TIMEZONE',        aesop_secret('AESOP_OWNER_TIMEZONE', 'America/Denver'));
define('BUSINESS_DAYS',         serialize([1, 2, 3, 4, 5]));

// Secondary calendar and Teams meeting integration
define('SECOND_CALENDAR_ICS',   aesop_require_secret('AESOP_SECOND_CALENDAR_ICS'));
define('CREATE_TEAMS_MEETING',  filter_var(aesop_secret('AESOP_CREATE_TEAMS_MEETING', 'true'), FILTER_VALIDATE_BOOLEAN));

// Database
define('DB_HOST', aesop_secret('AESOP_DB_HOST', 'localhost'));
define('DB_NAME', aesop_require_secret('AESOP_DB_NAME'));
define('DB_USER', aesop_require_secret('AESOP_DB_USER'));
define('DB_PASS', aesop_require_secret('AESOP_DB_PASS'));
