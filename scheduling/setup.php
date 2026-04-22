<?php
/**
 * Visit this page ONCE to connect your Outlook calendar.
 * After authorizing, delete or password-protect this file.
 */
require_once __DIR__ . '/config.php';

$params = http_build_query([
    'client_id'     => AZURE_CLIENT_ID,
    'response_type' => 'code',
    'redirect_uri'  => AZURE_REDIRECT_URI,
    'scope'         => 'Calendars.ReadWrite offline_access',
    'response_mode' => 'query',
    'prompt'        => 'consent',
]);

header('Location: https://login.microsoftonline.com/' . AZURE_TENANT_ID . '/oauth2/v2.0/authorize?' . $params);
exit;
