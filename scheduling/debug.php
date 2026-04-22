<?php
// TEMPORARY DEBUG — delete this file after troubleshooting
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/ics.php';

header('Content-Type: text/plain');

$ctx = stream_context_create(['http' => ['timeout' => 10, 'header' => 'User-Agent: SchedulerBot/1.0']]);
$raw = @file_get_contents(SECOND_CALENDAR_ICS, false, $ctx);

if (!$raw) {
    die("FAILED TO FETCH ICS URL");
}

// Unfold and normalize
$raw = preg_replace("/\r\n[ \t]/", '', $raw);
$raw = str_replace("\r\n", "\n", $raw);

echo "=== ALL EVENTS IN ICS FILE ===\n";
echo "Total file size: " . strlen($raw) . " bytes\n\n";

preg_match_all('/BEGIN:VEVENT\n(.*?)END:VEVENT/s', $raw, $events);
echo "Total VEVENTs found: " . count($events[1]) . "\n\n";

foreach ($events[1] as $i => $evt) {
    $summary = icsProp($evt, 'SUMMARY');
    $dtstart = icsDate($evt, 'DTSTART');
    $dtend   = icsDate($evt, 'DTEND');
    $rrule   = icsProp($evt, 'RRULE');
    $status  = icsProp($evt, 'STATUS');

    echo ($i+1) . ". " . ($summary ?: '(no title)') . "\n";
    echo "   Status:  " . ($status ?: 'CONFIRMED') . "\n";
    echo "   Start:   " . ($dtstart ? date('Y-m-d H:i T', $dtstart) : 'PARSE FAIL') . "\n";
    echo "   End:     " . ($dtend   ? date('Y-m-d H:i T', $dtend)   : 'PARSE FAIL') . "\n";
    if ($rrule) echo "   RRULE:   $rrule\n";
    echo "\n";
}

echo "\n=== Raw ICS (first 6000 chars) ===\n";
echo substr($raw, 0, 6000);
