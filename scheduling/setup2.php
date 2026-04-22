<?php
/**
 * Visit this page ONCE to connect the second calendar.
 * Uses 'common' endpoint so any Microsoft account can authorize.
 * Delete or password-protect this file after use.
 */
require_once __DIR__ . '/config.php';

$params = http_build_query([
    'client_id'     => AZURE_CLIENT_ID,
    'response_type' => 'code',
    'redirect_uri'  => AZURE_REDIRECT_URI,
    'scope'         => 'Calendars.Read offline_access',
    'response_mode' => 'query',
    'prompt'        => 'consent',
    'state'         => '2',   // tells auth.php to store as account #2
]);

header('Location: https://login.microsoftonline.com/common/oauth2/v2.0/authorize?' . $params);
exit;
