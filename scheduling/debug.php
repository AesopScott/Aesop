<?php
// TEMPORARY DEBUG — delete this file after troubleshooting
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/ics.php';

header('Content-Type: text/plain');

$rangeStart = mktime(0,0,0, date('n'), date('j'), date('Y'));
$rangeEnd   = $rangeStart + (BOOKING_DAYS_AHEAD * 86400);

echo "=== ICS Busy Blocks from Second Calendar ===\n";
echo "Range: " . date('Y-m-d H:i T', $rangeStart) . " to " . date('Y-m-d H:i T', $rangeEnd) . "\n\n";

$blocks = fetchIcsBusyBlocks(SECOND_CALENDAR_ICS, $rangeStart, $rangeEnd);

if (empty($blocks)) {
    echo "NO BLOCKS FOUND — ICS fetch may have failed or returned no events in range.\n";
} else {
    usort($blocks, fn($a,$b) => $a['start'] <=> $b['start']);
    foreach ($blocks as $b) {
        echo date('D M j g:ia T', $b['start']) . "  →  " . date('g:ia', $b['end']) . "\n";
    }
}

echo "\n=== Raw ICS snippet (first 3000 chars) ===\n";
$ctx = stream_context_create(['http' => ['timeout' => 10, 'header' => 'User-Agent: SchedulerBot/1.0']]);
$raw = @file_get_contents(SECOND_CALENDAR_ICS, false, $ctx);
echo $raw ? substr($raw, 0, 3000) : "FAILED TO FETCH ICS URL";
