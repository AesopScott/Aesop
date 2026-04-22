<?php
// TEMPORARY DEBUG — delete this file after troubleshooting
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/ics.php';

header('Content-Type: text/plain');

$ctx = stream_context_create(['http' => ['timeout' => 15, 'header' => 'User-Agent: SchedulerBot/1.0']]);
$raw = @file_get_contents(SECOND_CALENDAR_ICS, false, $ctx);
if (!$raw) die("FAILED TO FETCH ICS URL");

$raw = preg_replace("/\r\n[ \t]/", '', $raw);
$raw = str_replace("\r\n", "\n", $raw);

preg_match_all('/BEGIN:VEVENT\n(.*?)END:VEVENT/s', $raw, $events);

$year2026   = [];
$parseFails = [];
$pastCount  = 0;

foreach ($events[1] as $i => $evt) {
    $dtstart = icsDate($evt, 'DTSTART');
    $dtend   = icsDate($evt, 'DTEND');
    $summary = icsProp($evt, 'SUMMARY');
    $rrule   = icsProp($evt, 'RRULE');
    $status  = icsProp($evt, 'STATUS');

    if ($status === 'CANCELLED') continue;

    if ($dtstart === null) {
        $parseFails[] = $summary ?: "(no title)";
        continue;
    }

    if (date('Y', $dtstart) === '2026') {
        $year2026[] = compact('summary','dtstart','dtend','rrule');
    } elseif ($dtstart < mktime(0,0,0,4,22,2026)) {
        $pastCount++;
    }
}

echo "=== SUMMARY ===\n";
echo "Total events: " . count($events[1]) . "\n";
echo "Past events (before Apr 22 2026): $pastCount\n";
echo "Events with 2026 start dates: " . count($year2026) . "\n";
echo "Parse failures: " . count($parseFails) . "\n\n";

if ($parseFails) {
    echo "=== PARSE FAILURES ===\n";
    foreach ($parseFails as $f) echo "  - $f\n";
    echo "\n";
}

echo "=== 2026 EVENTS ===\n";
usort($year2026, fn($a,$b) => $a['dtstart'] <=> $b['dtstart']);
foreach ($year2026 as $e) {
    echo date('D M j H:i T', $e['dtstart']) . " → " . ($e['dtend'] ? date('H:i', $e['dtend']) : '?');
    echo "  |  " . ($e['summary'] ?: '(no title)');
    if ($e['rrule']) echo "  [RECURRING: " . $e['rrule'] . "]";
    echo "\n";
}

echo "\n=== SAMPLE DTSTART LINES (first 20 events) ===\n";
preg_match_all('/DTSTART[^\n]+/m', $raw, $dtstarts);
foreach (array_slice($dtstarts[0], 0, 20) as $line) {
    echo $line . "\n";
}
