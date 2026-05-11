<?php
require_once __DIR__ . '/config.php';

// Database functions now use file-based storage as fallback (Firebase backend)
// Tokens and bookings are stored in files on the server

function getStoredTokens(int $accountId = 1): ?array {
    $tokensFile = __DIR__ . '/.tokens-account' . $accountId;
    if (!file_exists($tokensFile)) {
        return null;
    }
    try {
        $data = json_decode(file_get_contents($tokensFile), true);
        return $data ?: null;
    } catch (Exception $e) {
        return null;
    }
}

function storeTokens(string $accessToken, string $refreshToken, int $expiresAt, int $accountId = 1): void {
    $tokensFile = __DIR__ . '/.tokens-account' . $accountId;
    $data = json_encode([
        'access_token' => $accessToken,
        'refresh_token' => $refreshToken,
        'expires_at' => $expiresAt,
        'accountId' => $accountId,
    ]);
    file_put_contents($tokensFile, $data);
    chmod($tokensFile, 0600);
}

function logBooking(string $eventId, string $name, string $email, string $start, string $end): void {
    $bookingsFile = __DIR__ . '/.bookings';
    $booking = [
        'outlook_event_id' => $eventId,
        'guest_name' => $name,
        'guest_email' => $email,
        'start_time' => $start,
        'end_time' => $end,
        'created_at' => date('c'),
    ];

    $bookings = [];
    if (file_exists($bookingsFile)) {
        $bookings = json_decode(file_get_contents($bookingsFile), true) ?: [];
    }

    $bookings[] = $booking;
    file_put_contents($bookingsFile, json_encode($bookings, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}
