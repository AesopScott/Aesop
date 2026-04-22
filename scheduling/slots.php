<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/graph.php';

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

if (!getValidAccessToken()) {
    http_response_code(503);
    echo json_encode(['error' => 'Calendar not connected. Run setup.php first.']);
    exit;
}

$ownerTz      = new DateTimeZone(OWNER_TIMEZONE);
$utc          = new DateTimeZone('UTC');
$businessDays = unserialize(BUSINESS_DAYS);
$minNotice    = MIN_NOTICE_HOURS * 3600;

$now   = new DateTime('now', $ownerTz);
$start = clone $now;
$start->modify('+' . MIN_NOTICE_HOURS . ' hours');
// Round up to next slot boundary
$slotSecs  = MEETING_DURATION * 60;
$remainder = $start->getTimestamp() % $slotSecs;
if ($remainder) {
    $start->modify('+' . ($slotSecs - $remainder) . ' seconds');
}

$end = new DateTime('now', $ownerTz);
$end->modify('+' . BOOKING_DAYS_AHEAD . ' days');
$end->setTime(23, 59, 59);

$startUtc = (clone $start)->setTimezone($utc)->format('Y-m-d\TH:i:s');
$endUtc   = (clone $end)->setTimezone($utc)->format('Y-m-d\TH:i:s');

function fetchBusyBlocks(array $scheduleResp): array {
    $blocks = [];
    foreach ($scheduleResp['value'][0]['scheduleItems'] ?? [] as $item) {
        if (in_array($item['status'], ['busy', 'oof', 'tentative'], true)) {
            $blocks[] = [
                'start' => (new DateTime($item['start']['dateTime'], new DateTimeZone($item['start']['timeZone'])))->getTimestamp(),
                'end'   => (new DateTime($item['end']['dateTime'],   new DateTimeZone($item['end']['timeZone'])))->getTimestamp(),
            ];
        }
    }
    return $blocks;
}

// Account 1 — primary Outlook calendar
$resp1 = graphPost('/me/calendar/getSchedule', [
    'schedules'                => [OWNER_EMAIL],
    'startTime'                => ['dateTime' => $startUtc, 'timeZone' => 'UTC'],
    'endTime'                  => ['dateTime' => $endUtc,   'timeZone' => 'UTC'],
    'availabilityViewInterval' => MEETING_DURATION,
], 1);
$busyBlocks = fetchBusyBlocks($resp1);

// Account 2 — secondary calendar (if connected)
if (getValidAccessToken(2)) {
    $resp2 = graphPost('/me/calendar/getSchedule', [
        'schedules'                => ['me'],
        'startTime'                => ['dateTime' => $startUtc, 'timeZone' => 'UTC'],
        'endTime'                  => ['dateTime' => $endUtc,   'timeZone' => 'UTC'],
        'availabilityViewInterval' => MEETING_DURATION,
    ], 2);
    $busyBlocks = array_merge($busyBlocks, fetchBusyBlocks($resp2));
}

// Walk day by day and generate slots
$slots  = [];
$cursor = clone $start;
$cursor->setTimezone($ownerTz);

while ($cursor <= $end) {
    $dow = (int)$cursor->format('N'); // 1=Mon…7=Sun
    if (in_array($dow, $businessDays, true)) {
        $dayStart = clone $cursor;
        $dayStart->setTime(BUSINESS_HOURS_START, 0, 0);
        $dayEnd   = clone $cursor;
        $dayEnd->setTime(BUSINESS_HOURS_END, 0, 0);

        // Don't go back in time
        if ($dayStart < $start) {
            $dayStart = clone $start;
            // re-align to slot boundary
            $rem = $dayStart->getTimestamp() % $slotSecs;
            if ($rem) $dayStart->modify('+' . ($slotSecs - $rem) . ' seconds');
        }

        $slotStart = clone $dayStart;
        while (true) {
            $slotEnd = clone $slotStart;
            $slotEnd->modify('+' . MEETING_DURATION . ' minutes');
            if ($slotEnd > $dayEnd) break;

            $sTs = $slotStart->getTimestamp();
            $eTs = $slotEnd->getTimestamp();
            $buffer = BUFFER_MINUTES * 60;

            $free = true;
            foreach ($busyBlocks as $b) {
                if ($sTs < ($b['end'] + $buffer) && $eTs > ($b['start'] - $buffer)) {
                    $free = false;
                    break;
                }
            }

            if ($free) {
                $slots[] = [
                    'start' => $slotStart->format('c'),   // ISO 8601 in owner tz
                    'utc'   => (clone $slotStart)->setTimezone($utc)->format('c'),
                    'ts'    => $sTs,
                ];
            }

            $slotStart->modify('+' . MEETING_DURATION . ' minutes');
        }
    }

    $cursor->modify('+1 day');
    $cursor->setTime(0, 0, 0);
}

echo json_encode(['slots' => $slots, 'duration' => MEETING_DURATION]);
