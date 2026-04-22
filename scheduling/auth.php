<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/db.php';
require_once __DIR__ . '/graph.php';

if (!isset($_GET['code'])) {
    http_response_code(400);
    die('Missing authorization code.');
}

$data = httpPost(
    'https://login.microsoftonline.com/' . AZURE_TENANT_ID . '/oauth2/v2.0/token',
    [
        'client_id'     => AZURE_CLIENT_ID,
        'client_secret' => AZURE_CLIENT_SECRET,
        'code'          => $_GET['code'],
        'redirect_uri'  => AZURE_REDIRECT_URI,
        'grant_type'    => 'authorization_code',
        'scope'         => 'Calendars.ReadWrite offline_access',
    ]
);

if (!isset($data['access_token'])) {
    $msg = htmlspecialchars($data['error_description'] ?? $data['error'] ?? 'Unknown error');
    die("Authorization failed: $msg");
}

storeTokens($data['access_token'], $data['refresh_token'], time() + (int)$data['expires_in']);

?><!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Connected!</title>
<style>
  body { font-family: system-ui, sans-serif; display: flex; align-items: center; justify-content: center;
         min-height: 100vh; margin: 0; background: #f0fdf4; }
  .card { background: #fff; border-radius: 12px; padding: 2.5rem 3rem; text-align: center;
          box-shadow: 0 4px 20px rgba(0,0,0,.08); max-width: 420px; }
  h1 { color: #16a34a; margin: 0 0 .5rem; }
  p  { color: #555; line-height: 1.6; }
  a  { display: inline-block; margin-top: 1.25rem; padding: .6rem 1.4rem;
       background: #2563eb; color: #fff; border-radius: 8px; text-decoration: none; font-weight: 500; }
</style>
</head>
<body>
<div class="card">
  <h1>&#10003; Connected!</h1>
  <p>Your Outlook calendar is now linked.<br>
     Your booking page is live and ready to share.</p>
  <p><strong>Important:</strong> delete or protect <code>setup.php</code> and <code>auth.php</code> now.</p>
  <a href="index.html">View booking page &rarr;</a>
</div>
</body>
</html>
