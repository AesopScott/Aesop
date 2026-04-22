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
            $duration    = $dtend - $dtstart;
            $occurrences = expandRRule($dtstart, $duration, $rrule, $rangeStart, $rangeEnd, $evt);
            $blocks      = array_merge($blocks, $occurrences);
        } else {
            if ($dtend > $rangeStart && $dtstart < $rangeEnd) {
                $blocks[] = ['start' => $dtstart, 'end' => $dtend];
            }
        }
    }

    return $blocks;
}

// Map Windows timezone names (used by Outlook ICS) to IANA names
function windowsToIana(string $tz): string {
    static $map = [
        'Afghanistan Standard Time'       => 'Asia/Kabul',
        'Alaskan Standard Time'           => 'America/Anchorage',
        'Arab Standard Time'              => 'Asia/Riyadh',
        'Arabian Standard Time'           => 'Asia/Dubai',
        'Arabic Standard Time'            => 'Asia/Baghdad',
        'Atlantic Standard Time'          => 'America/Halifax',
        'AUS Eastern Standard Time'       => 'Australia/Sydney',
        'Canada Central Standard Time'    => 'America/Regina',
        'Cen. Australia Standard Time'    => 'Australia/Adelaide',
        'Central America Standard Time'   => 'America/Guatemala',
        'Central Asia Standard Time'      => 'Asia/Almaty',
        'Central Europe Standard Time'    => 'Europe/Budapest',
        'Central European Standard Time'  => 'Europe/Warsaw',
        'Central Pacific Standard Time'   => 'Pacific/Guadalcanal',
        'Central Standard Time'           => 'America/Chicago',
        'Central Standard Time (Mexico)'  => 'America/Mexico_City',
        'China Standard Time'             => 'Asia/Shanghai',
        'E. Africa Standard Time'         => 'Africa/Nairobi',
        'E. Australia Standard Time'      => 'Australia/Brisbane',
        'E. Europe Standard Time'         => 'Asia/Nicosia',
        'E. South America Standard Time'  => 'America/Sao_Paulo',
        'Eastern Standard Time'           => 'America/New_York',
        'Eastern Standard Time (Mexico)'  => 'America/Cancun',
        'Egypt Standard Time'             => 'Africa/Cairo',
        'Fiji Standard Time'              => 'Pacific/Fiji',
        'FLE Standard Time'               => 'Europe/Helsinki',
        'GMT Standard Time'               => 'Europe/London',
        'Greenland Standard Time'         => 'America/Godthab',
        'Greenwich Standard Time'         => 'Atlantic/Reykjavik',
        'GTB Standard Time'               => 'Europe/Bucharest',
        'Hawaii-Aleutian Standard Time'   => 'Pacific/Honolulu',
        'Hawaii Standard Time'            => 'Pacific/Honolulu',
        'India Standard Time'             => 'Asia/Calcutta',
        'Israel Standard Time'            => 'Asia/Jerusalem',
        'Jordan Standard Time'            => 'Asia/Amman',
        'Korea Standard Time'             => 'Asia/Seoul',
        'Middle East Standard Time'       => 'Asia/Beirut',
        'Mountain Standard Time'          => 'America/Denver',
        'Mountain Standard Time (Mexico)' => 'America/Chihuahua',
        'Myanmar Standard Time'           => 'Asia/Rangoon',
        'N. Central Asia Standard Time'   => 'Asia/Novosibirsk',
        'Newfoundland Standard Time'      => 'America/St_Johns',
        'North Asia East Standard Time'   => 'Asia/Irkutsk',
        'North Asia Standard Time'        => 'Asia/Krasnoyarsk',
        'Pacific SA Standard Time'        => 'America/Santiago',
        'Pacific Standard Time'           => 'America/Los_Angeles',
        'Pacific Standard Time (Mexico)'  => 'America/Santa_Isabel',
        'Romance Standard Time'           => 'Europe/Paris',
        'Russia Time Zone 11'             => 'Asia/Kamchatka',
        'Russia Time Zone 3'              => 'Europe/Samara',
        'Russian Standard Time'           => 'Europe/Moscow',
        'SA Eastern Standard Time'        => 'America/Cayenne',
        'SA Pacific Standard Time'        => 'America/Bogota',
        'SA Western Standard Time'        => 'America/La_Paz',
        'SE Asia Standard Time'           => 'Asia/Bangkok',
        'Singapore Standard Time'         => 'Asia/Singapore',
        'South Africa Standard Time'      => 'Africa/Johannesburg',
        'Sri Lanka Standard Time'         => 'Asia/Colombo',
        'Taiwan Standard Time'            => 'Asia/Taipei',
        'Tokyo Standard Time'             => 'Asia/Tokyo',
        'Tonga Standard Time'             => 'Pacific/Tongatapu',
        'Turkey Standard Time'            => 'Europe/Istanbul',
        'US Eastern Standard Time'        => 'America/Indianapolis',
        'US Mountain Standard Time'       => 'America/Phoenix',
        'UTC'                             => 'UTC',
        'UTC+12'                          => 'Pacific/Tarawa',
        'UTC-02'                          => 'Atlantic/South_Georgia',
        'UTC-11'                          => 'Pacific/Midway',
        'Venezuela Standard Time'         => 'America/Caracas',
        'W. Australia Standard Time'      => 'Australia/Perth',
        'W. Central Africa Standard Time' => 'Africa/Lagos',
        'W. Europe Standard Time'         => 'Europe/Berlin',
        'West Asia Standard Time'         => 'Asia/Tashkent',
        'West Pacific Standard Time'      => 'Pacific/Port_Moresby',
        'Yakutsk Standard Time'           => 'Asia/Yakutsk',
    ];
    return $map[$tz] ?? $tz;
}

// Get a simple property value from a VEVENT block
function icsProp(string $evt, string $name): string {
    if (preg_match('/^' . preg_quote($name, '/') . '(?:;[^:]+)?:(.+)$/m', $evt, $m)) {
        return trim($m[1]);
    }
    return '';
}

// Parse a DTSTART/DTEND line into a Unix timestamp
function icsDate(string $evt, string $name): ?int {
    if (!preg_match('/^' . preg_quote($name, '/') . '(;[^:]+)?:(.+)$/m', $evt, $m)) return null;

    $params = $m[1] ?? '';
    $val    = trim($m[2]);

    // All-day date: YYYYMMDD — treat as midnight-to-midnight full day
    if (preg_match('/^\d{8}$/', $val)) {
        return mktime(0, 0, 0, (int)substr($val,4,2), (int)substr($val,6,2), (int)substr($val,0,4));
    }

    // Normalize: strip any non-digit chars after seconds (e.g. fractional seconds)
    $val = preg_replace('/^(\d{8}T\d{6}).*/', '$1', $val);

    // UTC timestamp ending with Z
    if (preg_match('/^\d{8}T\d{6}$/', $val) && substr(trim($m[2]), -1) === 'Z') {
        return gmmktime(
            (int)substr($val,9,2), (int)substr($val,11,2), (int)substr($val,13,2),
            (int)substr($val,4,2), (int)substr($val,6,2), (int)substr($val,0,4)
        );
    }

    // Has TZID parameter (may be Windows or IANA timezone name)
    if (preg_match('/TZID=([^;:]+)/', $params, $tz)) {
        $tzName = windowsToIana(trim($tz[1]));
        try {
            $formatted = substr($val,0,4).'-'.substr($val,4,2).'-'.substr($val,6,2)
                       .'T'.substr($val,9,2).':'.substr($val,11,2).':'.substr($val,13,2);
            $dt = new DateTime($formatted, new DateTimeZone($tzName));
            return $dt->getTimestamp();
        } catch (Exception $e) {
            // Fall through to UTC
        }
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

    $parts = [];
    foreach (explode(';', $rrule) as $part) {
        if (strpos($part, '=') === false) continue;
        [$k, $v] = explode('=', $part, 2);
        $parts[strtoupper(trim($k))] = strtoupper(trim($v));
    }

    $freq     = $parts['FREQ']     ?? '';
    $interval = max(1, (int)($parts['INTERVAL'] ?? 1));
    $count    = isset($parts['COUNT']) ? (int)$parts['COUNT'] : 500;
    $until    = null;
    if (!empty($parts['UNTIL'])) {
        $until = icsDateStr($parts['UNTIL']);
    }

    // BYDAY: map to PHP date('w') values (0=Sun…6=Sat)
    $dowMap = ['SU'=>0,'MO'=>1,'TU'=>2,'WE'=>3,'TH'=>4,'FR'=>5,'SA'=>6];
    $byday  = [];
    if (!empty($parts['BYDAY'])) {
        foreach (explode(',', $parts['BYDAY']) as $day) {
            $day = strtoupper(preg_replace('/[+-]?\d+/', '', trim($day)));
            if (isset($dowMap[$day])) $byday[] = $dowMap[$day];
        }
    }

    // EXDATE — excluded dates (match by date only, not time)
    $exdates = [];
    if (preg_match('/^EXDATE(?:;[^:]+)?:(.+)$/m', $evt, $exm)) {
        foreach (explode(',', trim($exm[1])) as $ex) {
            $ts = icsDateStr(trim($ex));
            if ($ts !== null) {
                $exdates[date('Ymd', $ts)] = true;
            }
        }
    }

    $limit = $rangeEnd;
    if ($until !== null) $limit = min($limit, $until);

    $cur = $dtstart;
    $n   = 0;

    while ($cur <= $limit && $n < $count) {
        $curDateKey = date('Ymd', $cur);
        $dow        = (int)date('w', $cur);

        $matchesDay = empty($byday) || in_array($dow, $byday, true);

        if ($matchesDay && !isset($exdates[$curDateKey])) {
            if ($cur + $duration > $rangeStart) {
                $blocks[] = ['start' => $cur, 'end' => $cur + $duration];
            }
            $n++;
        }

        // Advance cursor
        switch ($freq) {
            case 'DAILY':
                $cur = strtotime("+$interval day", $cur);
                break;

            case 'WEEKLY':
                if (!empty($byday)) {
                    // Step one day at a time; jump by interval weeks after completing a week cycle
                    $nextDay = strtotime('+1 day', $cur);
                    $nextDow = (int)date('w', $nextDay);
                    // If we're about to wrap to Sunday and interval > 1, skip ahead
                    if ($nextDow === 0 && $interval > 1) {
                        $nextDay = strtotime('+' . ($interval - 1) . ' week', $nextDay);
                    }
                    $cur = $nextDay;
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
    $val = preg_replace('/^(\d{8}T?\d{0,6}).*/', '$1', $val);
    if (preg_match('/^\d{8}$/', $val)) {
        return mktime(0,0,0,(int)substr($val,4,2),(int)substr($val,6,2),(int)substr($val,0,4));
    }
    if (preg_match('/^\d{8}T\d{6}$/', $val)) {
        return gmmktime(
            (int)substr($val,9,2),(int)substr($val,11,2),(int)substr($val,13,2),
            (int)substr($val,4,2),(int)substr($val,6,2),(int)substr($val,0,4)
        );
    }
    return null;
}
