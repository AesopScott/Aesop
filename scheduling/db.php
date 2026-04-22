<?php
require_once __DIR__ . '/config.php';

function getDB(): PDO {
    static $pdo = null;
    if (!$pdo) {
        $pdo = new PDO(
            'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4',
            DB_USER,
            DB_PASS,
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]
        );
    }
    return $pdo;
}

function getStoredTokens(int $accountId = 1): ?array {
    try {
        $stmt = getDB()->prepare('SELECT * FROM oauth_tokens WHERE id = ?');
        $stmt->execute([$accountId]);
        $row = $stmt->fetch();
        return $row ?: null;
    } catch (Exception $e) {
        return null;
    }
}

function storeTokens(string $accessToken, string $refreshToken, int $expiresAt, int $accountId = 1): void {
    $db   = getDB();
    $stmt = $db->prepare(
        'INSERT INTO oauth_tokens (id, access_token, refresh_token, expires_at)
         VALUES (:id, :a, :r, :e)
         ON DUPLICATE KEY UPDATE access_token = :a, refresh_token = :r, expires_at = :e'
    );
    $stmt->execute([':id' => $accountId, ':a' => $accessToken, ':r' => $refreshToken, ':e' => $expiresAt]);
}

function logBooking(string $eventId, string $name, string $email, string $start, string $end): void {
    $stmt = getDB()->prepare(
        'INSERT INTO bookings (outlook_event_id, guest_name, guest_email, start_time, end_time)
         VALUES (?, ?, ?, ?, ?)'
    );
    $stmt->execute([$eventId, $name, $email, $start, $end]);
}
