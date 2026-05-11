<?php
/**
 * Firebase Firestore helper for scheduler
 * Stores OAuth tokens and bookings in Firebase instead of MySQL
 */

require_once dirname(__DIR__) . '/secrets.php';

class FirebaseScheduler {
    private $projectId = 'playagame-f733d';
    private $baseUrl = 'https://firestore.googleapis.com/v1/projects/playagame-f733d/databases/(default)/documents';

    public function __construct() {
        // Verify Firebase service account is available
        $this->getAccessToken();
    }

    /**
     * Get OAuth2 access token for Firebase Admin API
     */
    private function getAccessToken() {
        static $token = null;
        static $tokenExpiry = 0;

        if ($token && time() < $tokenExpiry) {
            return $token;
        }

        // For now, use a simple approach: store/retrieve tokens in files
        // In production, you'd use the Firebase Admin SDK for PHP or OAuth2 library
        throw new RuntimeException('Firebase integration requires Google Application Default Credentials');
    }

    /**
     * Store OAuth tokens (write to file as fallback)
     */
    public function storeTokens($accessToken, $refreshToken, $expiresAt, $accountId = 1) {
        $tokensFile = dirname(__FILE__) . '/.tokens-account' . $accountId;
        $data = json_encode([
            'access_token' => $accessToken,
            'refresh_token' => $refreshToken,
            'expires_at' => $expiresAt,
            'accountId' => $accountId,
        ]);
        file_put_contents($tokensFile, $data);
        chmod($tokensFile, 0600); // Read/write for owner only
    }

    /**
     * Get stored OAuth tokens
     */
    public function getStoredTokens($accountId = 1) {
        $tokensFile = dirname(__FILE__) . '/.tokens-account' . $accountId;
        if (!file_exists($tokensFile)) {
            return null;
        }
        $data = json_decode(file_get_contents($tokensFile), true);
        return $data ?: null;
    }

    /**
     * Log booking
     */
    public function logBooking($eventId, $name, $email, $start, $end) {
        $bookingsFile = dirname(__FILE__) . '/.bookings';
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
}

// For now, use file-based storage as fallback
function getValidAccessToken($accountId = 1) {
    $firebase = new FirebaseScheduler();
    $tokens = $firebase->getStoredTokens($accountId);
    if (!$tokens) {
        return null;
    }

    if (time() >= $tokens['expires_at'] - 300) {
        // Token is expiring, try to refresh via OAuth
        $data = httpPost(
            'https://login.microsoftonline.com/common/oauth2/v2.0/token',
            [
                'client_id' => AZURE_CLIENT_ID,
                'client_secret' => AZURE_CLIENT_SECRET,
                'refresh_token' => $tokens['refresh_token'],
                'grant_type' => 'refresh_token',
                'scope' => 'Calendars.ReadWrite offline_access',
            ]
        );

        if (!isset($data['access_token'])) {
            error_log('[scheduler] Token refresh failed for account ' . $accountId . ': ' . json_encode($data));
            return null;
        }

        $newRefresh = $data['refresh_token'] ?? $tokens['refresh_token'];
        $firebase->storeTokens($data['access_token'], $newRefresh, time() + (int)$data['expires_in'], $accountId);
        return $data['access_token'];
    }

    return $tokens['access_token'];
}

function logBooking($eventId, $name, $email, $start, $end) {
    $firebase = new FirebaseScheduler();
    $firebase->logBooking($eventId, $name, $email, $start, $end);
}

function httpPost($url, $fields) {
    $ctx = stream_context_create([
        'http' => [
            'method' => 'POST',
            'header' => 'Content-Type: application/x-www-form-urlencoded',
            'content' => http_build_query($fields),
            'ignore_errors' => true,
        ],
    ]);
    return json_decode(file_get_contents($url, false, $ctx) ?: '{}', true) ?? [];
}
