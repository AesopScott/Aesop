<?php
// consent-mailer-v1.1
/**
 * consent-mailer.php — v1.1
 * Sends COPPA parental consent email and handles confirmation link clicks.
 * FTP to: public_html/aesop-academy/consent-mailer.php
 *
 * Requires PHPMailer already in /aesop-academy/ (PHPMailer.php, SMTP.php, Exception.php)
 * Email delivery via Brevo SMTP (free tier — 300 emails/day, reliable inbox delivery)
 */

header('Access-Control-Allow-Origin: https://aesopacademy.org');
header('Access-Control-Allow-Methods: POST, GET');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

require_once __DIR__ . '/PHPMailer.php';
require_once __DIR__ . '/SMTP.php';
require_once __DIR__ . '/Exception.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception as PHPMailerException;

// ─── CONFIG ──────────────────────────────────────────────────────────────────
define('SITE_URL',      'https://aesopacademy.org');
define('FROM_EMAIL',    'no-reply@aesopacademy.org');
define('FROM_NAME',     'AESOP AI Academy');
define('ADMIN_EMAIL',   'scott@aesopacademy.org');
define('TOKEN_DIR',     __DIR__ . '/consent-tokens/');
define('TOKEN_TTL',     60 * 60 * 72); // 72 hours

// Brevo SMTP — free tier (300 emails/day, reliable inbox delivery)
// Get credentials at: app.brevo.com → SMTP & API → SMTP tab
define('SMTP_HOST',     'smtp-relay.brevo.com');
define('SMTP_PORT',     587);
define('SMTP_USER',     'a78a3c001@smtp-brevo.com');   // ← your Brevo account email
define('SMTP_PASS',     'xsmtpsib-187a3c85b2209bdfd76163e0e5347a8f5bbc6ab6bc2cfc0b586b469b442e42cf-0JdKBmCXIqshwesH');      // ← Brevo SMTP key (not your password)
// ─────────────────────────────────────────────────────────────────────────────

// Create token directory if missing
if (!is_dir(TOKEN_DIR)) {
    mkdir(TOKEN_DIR, 0700, true);
}

$method = $_SERVER['REQUEST_METHOD'];

// ── GET: Handle confirmation link click ──────────────────────────────────────
if ($method === 'GET') {
    $token = isset($_GET['token']) ? preg_replace('/[^a-f0-9]/', '', $_GET['token']) : '';

    if (!$token) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'Missing token']);
        exit;
    }

    $file = TOKEN_DIR . $token . '.json';
    if (!file_exists($file)) {
        // Token already used or expired — redirect to expired page
        header('Location: ' . SITE_URL . '/consent-expired.html');
        exit;
    }

    $data = json_decode(file_get_contents($file), true);

    // Check expiry
    if (time() > $data['expires']) {
        unlink($file);
        header('Location: ' . SITE_URL . '/consent-expired.html');
        exit;
    }

    // Mark as verified — write a permanent record
    $record = [
        'childName'   => $data['childName'],
        'parentEmail' => $data['parentEmail'],
        'parentName'  => $data['parentName'],
        'verifiedAt'  => date('c'),
        'ip'          => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
    ];

    // Save verified record
    $recordFile = TOKEN_DIR . 'verified_' . $token . '.json';
    file_put_contents($recordFile, json_encode($record, JSON_PRETTY_PRINT));

    // Delete the pending token
    unlink($file);

    // Notify admin
    sendAdminNotification($record);

    // Redirect to success page with child name in query
    $childParam = urlencode($data['childName']);
    header('Location: ' . SITE_URL . '/consent-confirmed.html?child=' . $childParam);
    exit;
}

// ── POST: Send consent email ─────────────────────────────────────────────────
if ($method === 'POST') {
    $raw = file_get_contents('php://input');
    $body = json_decode($raw, true);

    $parentName  = trim($body['parentName']  ?? '');
    $parentEmail = trim($body['parentEmail'] ?? '');
    $childName   = trim($body['childName']   ?? '');

    if (!$parentName || !$parentEmail || !$childName || !filter_var($parentEmail, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'Missing or invalid fields']);
        exit;
    }

    // Generate token
    $token   = bin2hex(random_bytes(24));
    $expires = time() + TOKEN_TTL;

    // Store pending token
    $pending = [
        'token'       => $token,
        'parentName'  => $parentName,
        'parentEmail' => $parentEmail,
        'childName'   => $childName,
        'created'     => date('c'),
        'expires'     => $expires,
    ];
    file_put_contents(TOKEN_DIR . $token . '.json', json_encode($pending, JSON_PRETTY_PRINT));

    $confirmUrl = SITE_URL . '/consent-mailer.php?token=' . $token;

    // Build email
    $mail = new PHPMailer(true);
    try {
        $mail->isSMTP();
        $mail->Host       = SMTP_HOST;
        $mail->SMTPAuth   = true;
        $mail->Username   = SMTP_USER;
        $mail->Password   = SMTP_PASS;
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
        $mail->Port       = SMTP_PORT;
        $mail->setFrom(FROM_EMAIL, FROM_NAME);
        $mail->addAddress($parentEmail, $parentName);
        $mail->addReplyTo(ADMIN_EMAIL, FROM_NAME);
        $mail->isHTML(true);
        $mail->Subject = 'Action Required: Consent for ' . $childName . ' to use AESOP AI Academy';
        $mail->Body    = buildConsentEmail($parentName, $childName, $confirmUrl);
        $mail->AltBody = buildConsentEmailText($parentName, $childName, $confirmUrl);
        $mail->send();

        echo json_encode(['ok' => true]);
    } catch (PHPMailerException $e) {
        error_log('consent-mailer error: ' . $e->getMessage());
        http_response_code(500);
        echo json_encode(['ok' => false, 'error' => 'Email failed to send']);
    }
    exit;
}

http_response_code(405);
echo json_encode(['ok' => false, 'error' => 'Method not allowed']);
exit;

// ─── EMAIL TEMPLATES ─────────────────────────────────────────────────────────

function buildConsentEmail($parentName, $childName, $confirmUrl) {
    return <<<HTML
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><style>
  body { font-family: Georgia, serif; color: #1a1a2e; background: #faf8f4; margin: 0; padding: 0; }
  .wrap { max-width: 560px; margin: 40px auto; background: white; border: 1px solid #e2d9cc; border-radius: 8px; overflow: hidden; }
  .header { background: #1a1a2e; padding: 28px 32px; }
  .header h1 { color: #c9a05a; font-size: 20px; margin: 0; }
  .header p  { color: rgba(255,255,255,0.6); font-size: 13px; margin: 4px 0 0; }
  .body { padding: 32px; }
  .body p { font-size: 15px; line-height: 1.7; margin-bottom: 16px; }
  .btn { display: inline-block; background: #1a1a2e; color: white; text-decoration: none; padding: 14px 28px; border-radius: 6px; font-family: sans-serif; font-size: 15px; font-weight: 600; margin: 8px 0 20px; }
  .info-box { background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 6px; padding: 16px; font-size: 13px; color: #0c4a6e; line-height: 1.6; margin-bottom: 20px; }
  .info-box ul { padding-left: 16px; margin: 8px 0 0; }
  .info-box li { margin-bottom: 4px; }
  .footer { background: #f5f5f0; padding: 20px 32px; font-size: 12px; color: #718096; border-top: 1px solid #e2d9cc; }
  .footer a { color: #c9a05a; }
  .url-note { font-size: 12px; color: #718096; word-break: break-all; }
</style></head>
<body>
<div class="wrap">
  <div class="header">
    <h1>AESOP AI Academy</h1>
    <p>Parental Consent Request — aesopacademy.org</p>
  </div>
  <div class="body">
    <p>Hi {$parentName},</p>
    <p><strong>{$childName}</strong> would like to create a free account on <strong>AESOP AI Academy</strong>, an AI literacy curriculum designed for learners of all ages.</p>
    <p>Because {$childName} is under 13, we need your permission before they can sign up. This is required by U.S. law (COPPA).</p>

    <div class="info-box">
      <strong>What your child will learn:</strong>
      <ul>
        <li>What artificial intelligence is and how it works</li>
        <li>How to use AI safely and responsibly</li>
        <li>AI ethics, bias, and real-world case studies</li>
        <li>Storytelling and creative projects using AI tools</li>
      </ul>
    </div>

    <div class="info-box">
      <strong>What we collect &amp; how we use it:</strong>
      <ul>
        <li>Name and email address (for account login only)</li>
        <li>Course progress (to remember where they left off)</li>
        <li>We <strong>never</strong> sell data, show ads, or share data with third parties for marketing</li>
        <li>You can request data deletion at any time: <a href="mailto:scott@aesopacademy.org">scott@aesopacademy.org</a></li>
      </ul>
    </div>

    <p>If you approve, click the button below. This link expires in <strong>72 hours</strong>.</p>

    <a href="{$confirmUrl}" class="btn">✓ I Approve — Let {$childName} Join</a>

    <p class="url-note">Or copy this link into your browser:<br>{$confirmUrl}</p>

    <p>If you did not request this or don't recognize this request, simply ignore this email. No account will be created.</p>

    <p>Questions? Email us at <a href="mailto:scott@aesopacademy.org">scott@aesopacademy.org</a></p>
  </div>
  <div class="footer">
    AESOP AI Academy &mdash; aesopacademy.org<br>
    <a href="https://aesopacademy.org/privacy.html">Privacy Notice</a> &nbsp;|&nbsp;
    <a href="https://aesopacademy.org/parent-portal.html">Parent Portal</a>
  </div>
</div>
</body>
</html>
HTML;
}

function buildConsentEmailText($parentName, $childName, $confirmUrl) {
    return <<<TEXT
Hi {$parentName},

{$childName} would like to join AESOP AI Academy, a free AI literacy curriculum.

Because they are under 13, we need your permission (required by COPPA).

WHAT WE COLLECT: Name, email, course progress. We never sell data or show ads.

TO APPROVE, visit this link (expires in 72 hours):
{$confirmUrl}

If you did not request this, ignore this email. No account will be created.

Questions: scott@aesopacademy.org
AESOP AI Academy — aesopacademy.org
Privacy Notice: https://aesopacademy.org/privacy.html
TEXT;
}

function sendAdminNotification($record) {
    $mail = new PHPMailer(true);
    try {
        $mail->isSMTP();
        $mail->Host       = SMTP_HOST;
        $mail->SMTPAuth   = true;
        $mail->Username   = SMTP_USER;
        $mail->Password   = SMTP_PASS;
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
        $mail->Port       = SMTP_PORT;
        $mail->setFrom(FROM_EMAIL, FROM_NAME);
        $mail->addAddress(ADMIN_EMAIL);
        $mail->Subject = '[AESOP] New parental consent verified — ' . $record['childName'];
        $mail->Body    = "New COPPA consent verified.\n\nChild: {$record['childName']}\nParent: {$record['parentName']} <{$record['parentEmail']}>\nVerified: {$record['verifiedAt']}\nIP: {$record['ip']}";
        $mail->send();
    } catch (PHPMailerException $e) {
        error_log('consent admin notify error: ' . $e->getMessage());
    }
}
