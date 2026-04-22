<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);
ini_set('pcre.backtrack_limit', 10000000);
ini_set('memory_limit', '256M');

require_once __DIR__ . '/config.php';

header('Content-Type: text/plain');

$ctx = stream_context_create(['http' => ['timeout' => 15, 'header' => 'User-Agent: SchedulerBot/1.0']]);
$raw = @file_get_contents(SECOND_CALENDAR_ICS, false, $ctx);
if (!$raw) die("FAILED TO FETCH ICS URL");

echo "File size: " . strlen($raw) . " bytes\n\n";

// Parse line by line
$raw   = str_replace("\r\n", "\n", $raw);
$raw   = preg_replace("/\n[ \t]/", '', $raw); // unfold
$lines = explode("\n", $raw);

$inEvent  = false;
$event    = [];
$events   = [];

foreach ($lines as $line) {
    if ($line === 'BEGIN:VEVENT') {
        $inEvent = true;
        $event   = [];
    } elseif ($line === 'END:VEVENT') {
        $inEvent = false;
        $events[] = $event;
    } elseif ($inEvent) {
        $pos = strpos($line, ':');
        if ($pos !== false) {
            $key = strtoupper(substr($line, 0, $pos));
            $val = substr($line, $pos + 1);
            $event[$key] = $val;
            // Also store with params stripped for easier lookup
            $bareKey = explode(';', $key)[0];
            if ($bareKey !== $key) $event[$bareKey . '__LINE'] = $line;
        }
    }
}

echo "Total events parsed: " . count($events) . "\n\n";

// Show DTSTART sample formats
echo "=== SAMPLE DTSTART FORMATS (first 10) ===\n";
$shown = 0;
foreach ($events as $e) {
    foreach ($e as $k => $v) {
        if (strpos($k, 'DTSTART') === 0) {
            echo "$k:$v\n";
            $shown++;
            break;
        }
    }
    if ($shown >= 10) break;
}

echo "\n=== 2026 EVENTS ===\n";
$count2026 = 0;
$countPast = 0;
$countFail = 0;

foreach ($events as $e) {
    $dtRaw = null;
    foreach ($e as $k => $v) {
        if (strpos($k, 'DTSTART') === 0) { $dtRaw = $v; break; }
    }

    if (!$dtRaw) { $countFail++; continue; }

    // Quick year check without full parsing
    $year = (int)substr(preg_replace('/.*:/', '', $dtRaw), 0, 4);

    $summary = $e['SUMMARY'] ?? '(no title)';
    $rrule   = $e['RRULE']   ?? '';
    $status  = $e['STATUS']  ?? '';

    if ($status === 'CANCELLED') continue;

    if ($year === 2026) {
        $count2026++;
        $dtStr = preg_replace('/.*:/', '', $dtRaw);
        echo "$dtStr | $summary";
        if ($rrule) echo " [RECUR]";
        echo "\n";
    } elseif ($year < 2026) {
        $countPast++;
    }
}

echo "\n=== SUMMARY ===\n";
echo "Past events:   $countPast\n";
echo "2026 events:   $count2026\n";
echo "No DTSTART:    $countFail\n";
