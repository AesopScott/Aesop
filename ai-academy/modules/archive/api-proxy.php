<?php
/**
 * AESOP AI Academy — Anthropic API Proxy
 * ----------------------------------------
 * Deploy to: public_html/mobile/ai-academy/ai-curriculum/api-proxy.php
 *
 * 1. Replace YOUR_API_KEY_HERE with your actual Anthropic API key.
 * 2. Update ALLOWED_ORIGINS to include your live domain.
 * 3. Upload via FTP/cPanel File Manager.
 */

define('ANTHROPIC_API_KEY', 'YOUR_API_KEY_HERE');
define('ANTHROPIC_API_URL', 'https://api.anthropic.com/v1/messages');
define('MODEL',             'claude-sonnet-4-20250514');
define('MAX_TOKENS_CAP',    1024);

// ── CORS ──────────────────────────────────────────────────────
$allowed_origins = [
    'https://playagame.ai',
    'https://www.playagame.ai',
    'http://localhost',
    'http://127.0.0.1',
];
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $allowed_origins, true)) {
    header("Access-Control-Allow-Origin: $origin");
} else {
    header('Access-Control-Allow-Origin: https://playagame.ai');
}
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

// ── PARSE REQUEST ─────────────────────────────────────────────
$raw  = file_get_contents('php://input');
$body = json_decode($raw, true);
if (!$body || !is_array($body)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON body']);
    exit;
}

$messages      = $body['messages']      ?? [];
$system_prompt = $body['system_prompt'] ?? '';
$max_tokens    = min((int)($body['max_tokens'] ?? MAX_TOKENS_CAP), MAX_TOKENS_CAP);

if (empty($messages) || !is_array($messages)) {
    http_response_code(400);
    echo json_encode(['error' => 'messages array required']);
    exit;
}

// ── SANITIZE MESSAGES ─────────────────────────────────────────
// Keep only role/content pairs with valid roles; truncate huge messages
$clean_messages = [];
foreach ($messages as $msg) {
    $role    = $msg['role']    ?? '';
    $content = $msg['content'] ?? '';
    if (!in_array($role, ['user', 'assistant'], true)) continue;
    if (!is_string($content)) continue;
    // Hard cap per message — prevents prompt injection via oversized input
    if (strlen($content) > 8000) {
        $content = mb_substr($content, 0, 8000) . "\n[message truncated]";
    }
    $clean_messages[] = ['role' => $role, 'content' => $content];
}

if (empty($clean_messages)) {
    http_response_code(400);
    echo json_encode(['error' => 'No valid messages after sanitization']);
    exit;
}

// ── BUILD ANTHROPIC REQUEST ───────────────────────────────────
$payload = [
    'model'      => MODEL,
    'max_tokens' => $max_tokens,
    'messages'   => $clean_messages,
];

// Only add system if non-empty; Anthropic rejects empty system strings
if (!empty(trim($system_prompt))) {
    // Truncate system prompt too — prevents injection via that field
    $payload['system'] = mb_substr(trim($system_prompt), 0, 4000);
}

// ── CALL ANTHROPIC ────────────────────────────────────────────
$ch = curl_init(ANTHROPIC_API_URL);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => json_encode($payload),
    CURLOPT_HTTPHEADER     => [
        'Content-Type: application/json',
        'x-api-key: ' . ANTHROPIC_API_KEY,
        'anthropic-version: 2023-06-01',
    ],
    CURLOPT_TIMEOUT        => 60,
    CURLOPT_CONNECTTIMEOUT => 10,
]);

$response    = curl_exec($ch);
$http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curl_error  = curl_error($ch);
curl_close($ch);

if ($curl_error) {
    http_response_code(502);
    echo json_encode(['error' => 'Upstream connection failed: ' . $curl_error]);
    exit;
}

// ── FORWARD RESPONSE ─────────────────────────────────────────
http_response_code($http_status);
echo $response;
