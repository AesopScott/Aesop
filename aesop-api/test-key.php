<?php
/**
 * Temporary key diagnostic — DELETE THIS FILE after testing.
 * Visit: https://aesopacademy.org/aesop-api/test-key.php
 */
require_once dirname(__DIR__) . '/secrets.php';

header('Content-Type: text/plain');

$key = aesop_secret('AESOP_ANTHROPIC_API_KEY', '');

echo "Key loaded: " . (strlen($key) > 0 ? "YES (" . strlen($key) . " chars)" : "NO — empty") . "\n";
echo "Starts with: " . substr($key, 0, 12) . "...\n";
echo "Ends with: ..." . substr($key, -4) . "\n\n";

// Test call to Anthropic
$ch = curl_init('https://api.anthropic.com/v1/messages');
curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => json_encode([
        'model'      => 'claude-haiku-4-5-20241022',
        'max_tokens' => 10,
        'messages'   => [['role' => 'user', 'content' => 'Say hi']],
    ]),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 15,
    CURLOPT_HTTPHEADER     => [
        'Content-Type: application/json',
        'x-api-key: ' . $key,
        'anthropic-version: 2023-06-01',
    ],
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlErr  = curl_error($ch);
curl_close($ch);

echo "HTTP status: $httpCode\n";
if ($curlErr) echo "Curl error: $curlErr\n";
echo "Response: $response\n";
