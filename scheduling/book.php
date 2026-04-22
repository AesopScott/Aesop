<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/db.php';
require_once __DIR__ . '/graph.php';

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$name  = trim($input['name']  ?? '');
$email = trim($input['email'] ?? '');
$ts    = (int)($input['ts']   ?? 0);
$note  = trim($input['note']  ?? '');

if (!$name || !$ts) {
    http_response_code(400);
    echo json_encode(['error' => 'Name and time are required.']);
    exit;
}

$email = filter_var($email, FILTER_VALIDATE_EMAIL);
if (!$email) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid email address.']);
    exit;
}

$utc      = new DateTimeZone('UTC');
$ownerTz  = new DateTimeZone(OWNER_TIMEZONE);
$slotStart = new DateTime('@' . $ts, $utc);
$slotEnd   = clone $slotStart;
$slotEnd->modify('+' . MEETING_DURATION . ' minutes');

// Verify the slot is still in the future with minimum notice
if ($ts < time() + MIN_NOTICE_HOURS * 3600) {
    http_response_code(409);
    echo json_encode(['error' => 'That time slot is no longer available.']);
    exit;
}

$body  = "Hi $name,\n\nLooking forward to connecting!\n\n";
$body .= $note ? "Your note: $note\n\n" : '';
$body .= "— " . OWNER_NAME;

$event = [
    'subject' => 'Meeting with ' . $name,
    'body'    => ['contentType' => 'text', 'content' => $body],
    'start'   => ['dateTime' => $slotStart->format('Y-m-d\TH:i:s'), 'timeZone' => 'UTC'],
    'end'     => ['dateTime' => $slotEnd->format('Y-m-d\TH:i:s'),   'timeZone' => 'UTC'],
    'attendees' => [[
        'emailAddress' => ['address' => $email, 'name' => $name],
        'type'         => 'required',
    ]],
    'allowNewTimeProposals' => false,
];

if (CREATE_TEAMS_MEETING) {
    $event['isOnlineMeeting']        = true;
    $event['onlineMeetingProvider']  = 'teamsForBusiness';
}

$result = graphPost('/me/events', $event);

if (!isset($result['id'])) {
    $detail = $result['error']['message'] ?? 'Unknown Graph API error';
    http_response_code(502);
    echo json_encode(['error' => "Could not create meeting: $detail"]);
    exit;
}

logBooking(
    $result['id'],
    $name,
    $email,
    $slotStart->setTimezone($ownerTz)->format('Y-m-d H:i:s'),
    $slotEnd->setTimezone($ownerTz)->format('Y-m-d H:i:s')
);

$joinUrl = $result['onlineMeeting']['joinUrl'] ?? null;
$friendly = (new DateTime('@' . $ts))->setTimezone($ownerTz)->format('l, F j \a\t g:ia T');

echo json_encode([
    'success'  => true,
    'time'     => $friendly,
    'joinUrl'  => $joinUrl,
]);
