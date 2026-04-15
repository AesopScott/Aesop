<?php
// report-mailer.php v1.1 — AESOP AI Academy Issue Report Mailer
// Uses PHPMailer + GoDaddy SMTP (scott@aesopacademy.org mailbox is on GoDaddy)
// Deploy to: public_html/aesop-academy/report-mailer.php
//
// ── BEFORE DEPLOYING ─────────────────────────────────────────────────────────
// 1. Upload PHPMailer (3 files) to public_html/aesop-academy/phpmailer/
//      - Exception.php
//      - PHPMailer.php
//      - SMTP.php
//    Download from: https://github.com/PHPMailer/PHPMailer/tree/master/src
//    (click each file → Raw → Save As)
//
// 2. Fill in SMTP_PASSWORD below with your GoDaddy email password
// 3. FTP this file to public_html/aesop-academy/report-mailer.php
// ─────────────────────────────────────────────────────────────────────────────

require_once __DIR__ . '/secrets.php';

// ── CREDENTIALS — edit these ──────────────────────────────────────────────────
define('SMTP_HOST',     'smtpout.secureserver.net'); // GoDaddy outgoing SMTP
define('SMTP_PORT',     465);                         // SSL port
define('SMTP_USER',     'scott@aesopacademy.org');
define('SMTP_PASSWORD', aesop_secret('AESOP_REPORT_SMTP_PASSWORD', ''));
define('MAIL_TO',       'scott@aesopacademy.org');
define('MAIL_FROM',     'scott@aesopacademy.org');
// ─────────────────────────────────────────────────────────────────────────────

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: https://aesopacademy.org');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method not allowed']);
    exit;
}

if (SMTP_PASSWORD === '') {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Server is missing AESOP_REPORT_SMTP_PASSWORD']);
    exit;
}

// Load PHPMailer
$pmDir = __DIR__ . '/phpmailer/';
if (!file_exists($pmDir . 'PHPMailer.php')) {
    error_log('report-mailer: PHPMailer not found at ' . $pmDir);
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Mailer not configured — PHPMailer missing']);
    exit;
}
require $pmDir . 'Exception.php';
require $pmDir . 'PHPMailer.php';
require $pmDir . 'SMTP.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

// Parse body
$raw  = file_get_contents('php://input');
$data = json_decode($raw, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Invalid JSON']);
    exit;
}

function clean($val) {
    return htmlspecialchars(strip_tags(trim((string)$val)), ENT_QUOTES, 'UTF-8');
}

$issueType    = clean($data['issueType']    ?? 'not specified');
$affectedPage = clean($data['affectedPage'] ?? 'not specified');
$tier         = clean($data['tier']         ?? '');
$description  = clean($data['description']  ?? '');
$pageUrl      = clean($data['pageUrl']      ?? '');
$severity     = strtoupper(clean($data['severity'] ?? 'MEDIUM'));
$email        = clean($data['email']        ?? '');
$submittedAt  = clean($data['submittedAt']  ?? date('c'));
$userAgent    = clean($data['userAgent']    ?? '');

if (empty($description)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Description required']);
    exit;
}

$severityEmoji = [
    'LOW'      => 'LOW',
    'MEDIUM'   => 'MEDIUM',
    'HIGH'     => 'HIGH',
    'CRITICAL' => 'CRITICAL',
][$severity] ?? $severity;

$isUrgent = in_array($severity, ['HIGH', 'CRITICAL']);
$subjectPrefix = $isUrgent ? '[URGENT] ' : '';
$subject = $subjectPrefix . 'AESOP Issue Report — ' . $severityEmoji . ' — ' . $issueType;

$body  = "AESOP AI ACADEMY -- ISSUE REPORT\n";
$body .= str_repeat('=', 50) . "\n\n";
$body .= "Submitted:     {$submittedAt}\n";
$body .= "Severity:      {$severityEmoji}\n";
$body .= "Issue Type:    {$issueType}\n";
$body .= "Affected Page: {$affectedPage}\n";
if ($tier)    $body .= "Tier:          {$tier}\n";
if ($pageUrl) $body .= "Page URL:      {$pageUrl}\n";
if ($email)   $body .= "Reporter:      {$email}\n";
$body .= "\nDESCRIPTION\n" . str_repeat('-', 40) . "\n";
$body .= wordwrap($description, 72, "\n", true) . "\n\n";
$body .= str_repeat('-', 40) . "\n";
$body .= "User Agent: {$userAgent}\n";
$body .= "\n-- aesopacademy.org/report-mailer.php v1.1\n";

$mail = new PHPMailer(true);
try {
    $mail->isSMTP();
    $mail->Host       = SMTP_HOST;
    $mail->SMTPAuth   = true;
    $mail->Username   = SMTP_USER;
    $mail->Password   = SMTP_PASSWORD;
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
    $mail->Port       = SMTP_PORT;

    $mail->setFrom(MAIL_FROM, 'AESOP Issue Reporter');
    $mail->addAddress(MAIL_TO, 'Scott - AESOP Academy');
    if ($email) $mail->addReplyTo($email, 'Reporter');

    $mail->Subject = $subject;
    $mail->Body    = $body;
    $mail->isHTML(false);
    if ($isUrgent) $mail->Priority = 1;

    $mail->send();
    echo json_encode(['ok' => true]);

} catch (Exception $e) {
    error_log('report-mailer: PHPMailer error -- ' . $mail->ErrorInfo);
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Mail send failed: ' . $mail->ErrorInfo]);
}
