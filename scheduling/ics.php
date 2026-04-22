<?php
/**
 * Fetches an ICS calendar feed and returns busy time blocks
 * as [{start: timestamp, end: timestamp}, …] within the given range.
 */
function fetchIcsBusyBlocks(string $url, int $rangeStart, int $rangeEnd): array {
    $ctx = stream_context_create(['http' => [
        'timeout'       => 10,
        'ignore_errors' => true,
        'header'        => 'User-Agent: SchedulerBot/1.0',
    ]]);
    $raw = @file_get_contents($url, false, $ctx);
    if (!$raw) return [];

    // Unfold ICS lines (CRLF + whitespace = continuation)
    $raw = preg_replace("/\r\n[ \t]/", '', $raw);
    $raw = str_replace("\r\n", "\n", $raw);

    $blocks = [];
    preg_match_all('/BEGIN:VEVENT\n(.*?)END:VEVENT/s', $raw, $events);

    foreach ($events[1] as $evt) {
        $status = icsProp($evt, 'STATUS');
        if ($status === 'CANCELLED') continue;

        $dtstart = icsDate($evt, 'DTSTART');
        $dtend   = icsDate($evt, 'DTEND');
        if (!$dtstart || !$dtend) continue;

        $rrule = icsProp($evt, 'RRULE');
        if ($rrule) {
            $duration = $dtend - $dtstart;
            $occurrences = expandRRule($dtstart, $duration, $rrule, $rangeStart, $rangeEnd, $evt);
            $blocks = array_merge($blocks, $occurrences);
        } else {
            if ($dtend > $rangeStart && $dtstart < $rangeEnd) {
                $blocks[] = ['start' => $dtstart, 'end' => $dtend];
            }
        }
    }

    return $blocks;
}

// Get a property value from a VEVENT block (handles TZID params)
function icsProp(string $evt, string $name): string {
    if (preg_match('/^' . $name . '[;:][^\n]*?:?([^\n:]+)$/m', $evt, $m)) {
        // Handle "NAME;PARAM=val:value" and "NAME:value"
        if (preg_match('/^' . $name . '(?:;[^:]+)?:(.+)$/m', $evt, $m2)) {
            return trim($m2[1]);
        }
    }
    return '';
}

// Parse a DTSTART/DTEND line into a Unix timestamp
function icsDate(string $evt, string $name): ?int {
    if (!preg_match('/^' . $name . '(;[^:]+)?:(.+)$/m', $evt, $m)) return null;

    $params = $m[1] ?? '';
    $val    = trim($m[2]);

    // All-day date: YYYYMMDD
    if (preg_match('/^\d{8}$/', $val)) {
        return mktime(0, 0, 0, (int)substr($val,4,2), (int)substr($val,6,2), (int)substr($val,0,4));
    }

    // UTC: ends with Z
    if (str_ends_with($val, 'Z')) {
        $val = rtrim($val, 'Z');
        return gmmktime(
            (int)substr($val,9,2), (int)substr($val,11,2), (int)substr($val,13,2),
            (int)substr($val,4,2), (int)substr($val,6,2), (int)substr($val,0,4)
        );
    }

    // Has TZID
    if (preg_match('/TZID=([^;:]+)/', $params, $tz)) {
        try {
            $dt = new DateTime($val, new DateTimeZone($tz[1]));
            return $dt->getTimestamp();
        } catch (Exception $e) {}
    }

    // Fallback: treat as UTC
    return gmmktime(
        (int)substr($val,9,2), (int)substr($val,11,2), (int)substr($val,13,2),
        (int)substr($val,4,2), (int)substr($val,6,2), (int)substr($val,0,4)
    );
}

// Expand recurring events into individual occurrences within range
function expandRRule(int $dtstart, int $duration, string $rrule, int $rangeStart, int $rangeEnd, string $evt): array {
    $blocks = [];

    // Parse RRULE parts
    $parts = [];
    foreach (explode(';', $rrule) as $part) {
        [$k, $v] = explode('=', $part, 2) + ['', ''];
        $parts[strtoupper($k)] = strtoupper($v);
    }

    $freq  = $parts['FREQ']  ?? '';
    $until = isset($parts['UNTIL']) ? icsDateStr($parts['UNTIL']) : null;
    $count = isset($parts['COUNT']) ? (int)$parts['COUNT'] : 999;
    $interval = max(1, (int)($parts['INTERVAL'] ?? 1));

    // EXDATE — excluded dates
    $exdates = [];
    if (preg_match('/^EXDATE(?:;[^:]+)?:(.+)$/m', $evt, $exm)) {
        foreach (explode(',', trim($exm[1])) as $ex) {
            $ts = icsDateStr(trim($ex));
            if ($ts) $exdates[$ts] = true;
        }
    }

    $limit = min($until ?? $rangeEnd, $rangeEnd);
    $cur   = $dtstart;
    $n     = 0;

    // Days of week map for BYDAY
    $dowMap = ['SU'=>0,'MO'=>1,'TU'=>2,'WE'=>3,'TH'=>4,'FR'=>5,'SA'=>6];
    $byday  = [];
    if (!empty($parts['BYDAY'])) {
        foreach (explode(',', $parts['BYDAY']) as $day) {
            $day = preg_replace('/[+-]?\d+/', '', $day); // strip ordinals
            if (isset($dowMap[$day])) $byday[] = $dowMap[$day];
        }
    }

    while ($cur <= $limit && $n < $count) {
        if ($cur >= $rangeStart && !isset($exdates[$cur])) {
            // For weekly freq with BYDAY, check day matches
            $dow = (int)date('w', $cur); // 0=Sun
            if (empty($byday) || in_array($dow, $byday, true)) {
                $blocks[] = ['start' => $cur, 'end' => $cur + $duration];
                $n++;
            }
        }

        // Advance to next occurrence
        switch ($freq) {
            case 'DAILY':
                $cur = strtotime("+$interval day", $cur);
                break;
            case 'WEEKLY':
                if (!empty($byday)) {
                    // Walk day by day until we hit an allowed day of the next week
                    $cur = strtotime('+1 day', $cur);
                    // Jump ahead by interval weeks when we've gone through all days in this week
                    // Simple approach: just step 1 day at a time
                } else {
                    $cur = strtotime("+$interval week", $cur);
                }
                break;
            case 'MONTHLY':
                $cur = strtotime("+$interval month", $cur);
                break;
            case 'YEARLY':
                $cur = strtotime("+$interval year", $cur);
                break;
            default:
                break 2;
        }
        if ($cur === false) break;
    }

    return $blocks;
}

function icsDateStr(string $val): ?int {
    $val = trim($val);
    if (preg_match('/^\d{8}$/', $val)) {
        return mktime(0,0,0,(int)substr($val,4,2),(int)substr($val,6,2),(int)substr($val,0,4));
    }
    if (str_ends_with($val, 'Z')) {
        $val = rtrim($val, 'Z');
        return gmmktime(
            (int)substr($val,9,2),(int)substr($val,11,2),(int)substr($val,13,2),
            (int)substr($val,4,2),(int)substr($val,6,2),(int)substr($val,0,4)
        );
    }
    return null;
}
