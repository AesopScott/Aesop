<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/db.php';

function getValidAccessToken(): ?string {
    $tokens = getStoredTokens();
    if (!$tokens) return null;

    // Refresh 5 minutes before expiry
    if (time() >= $tokens['expires_at'] - 300) {
        $data = httpPost(
            'https://login.microsoftonline.com/' . AZURE_TENANT_ID . '/oauth2/v2.0/token',
            [
                'client_id'     => AZURE_CLIENT_ID,
                'client_secret' => AZURE_CLIENT_SECRET,
                'refresh_token' => $tokens['refresh_token'],
                'grant_type'    => 'refresh_token',
                'scope'         => 'Calendars.ReadWrite offline_access',
            ]
        );
        if (!isset($data['access_token'])) return null;
        $newRefresh = $data['refresh_token'] ?? $tokens['refresh_token'];
        storeTokens($data['access_token'], $newRefresh, time() + (int)$data['expires_in']);
        return $data['access_token'];
    }

    return $tokens['access_token'];
}

function graphGet(string $endpoint): array {
    $token = getValidAccessToken();
    return httpRequest('GET', 'https://graph.microsoft.com/v1.0' . $endpoint, null, $token);
}

function graphPost(string $endpoint, array $body): array {
    $token = getValidAccessToken();
    return httpRequest('POST', 'https://graph.microsoft.com/v1.0' . $endpoint, $body, $token);
}

function httpPost(string $url, array $fields): array {
    $ctx = stream_context_create([
        'http' => [
            'method'  => 'POST',
            'header'  => 'Content-Type: application/x-www-form-urlencoded',
            'content' => http_build_query($fields),
            'ignore_errors' => true,
        ],
    ]);
    return json_decode(file_get_contents($url, false, $ctx) ?: '{}', true) ?? [];
}

function httpRequest(string $method, string $url, ?array $body, string $token): array {
    $headers = "Authorization: Bearer $token\r\nContent-Type: application/json\r\nAccept: application/json";
    $opts    = ['method' => $method, 'header' => $headers, 'ignore_errors' => true];
    if ($body !== null) {
        $opts['content'] = json_encode($body);
    }
    $ctx      = stream_context_create(['http' => $opts]);
    $response = file_get_contents($url, false, $ctx);
    return json_decode($response ?: '{}', true) ?? [];
}
