<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/db.php';
require_once __DIR__ . '/graph.php';

// Simple token gate — pass ?token=... in the URL
$token = $_GET['token'] ?? '';
if (!$token || $token !== 'aesop-bookings-2026') {
    http_response_code(403);
    die('Forbidden');
}

$stmt = getDB()->query(
    'SELECT id, guest_name, guest_email, start_time, end_time, created_at, outlook_event_id
     FROM bookings ORDER BY start_time DESC'
);
$rows = $stmt->fetchAll();

// Fetch Teams join URLs — patch to add Teams if missing
foreach ($rows as &$r) {
    $r['join_url']  = null;
    $r['graph_err'] = null;
    if (!$r['outlook_event_id']) continue;

    $eid = rawurlencode($r['outlook_event_id']);
    $ev  = graphGet('/me/events/' . $eid . '?$select=onlineMeeting,onlineMeetingUrl,isOnlineMeeting');

    if (isset($ev['error'])) {
        $r['graph_err'] = $ev['error']['code'] . ': ' . $ev['error']['message'];
        continue;
    }

    $joinUrl = $ev['onlineMeeting']['joinUrl'] ?? $ev['onlineMeetingUrl'] ?? null;

    // If no Teams link yet, patch the event to add one
    if (!$joinUrl) {
        $patch = graphPatch('/me/events/' . $eid, [
            'isOnlineMeeting'       => true,
            'onlineMeetingProvider' => 'teamsForBusiness',
        ]);
        if (isset($patch['error'])) {
            $r['graph_err'] = 'patch: ' . $patch['error']['code'] . ': ' . $patch['error']['message'];
        } else {
            $joinUrl = $patch['onlineMeeting']['joinUrl'] ?? $patch['onlineMeetingUrl'] ?? null;
        }
    }

    $r['join_url'] = $joinUrl;
}
unset($r);

header('Content-Type: text/html; charset=utf-8');
?><!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Bookings — AESOP Scheduler</title>
<style>
  body { font-family: system-ui, sans-serif; padding: 2rem; background: #f8fafc; color: #1e293b; }
  h1 { margin-bottom: 1.5rem; font-size: 1.4rem; }
  table { border-collapse: collapse; width: 100%; background: #fff; border-radius: 8px;
          box-shadow: 0 1px 4px rgba(0,0,0,.08); overflow: hidden; }
  th { background: #1e293b; color: #fff; text-align: left; padding: .6rem 1rem; font-size: .8rem;
       letter-spacing: .05em; text-transform: uppercase; }
  td { padding: .65rem 1rem; border-bottom: 1px solid #e2e8f0; font-size: .875rem; vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #f1f5f9; }
  .count { color: #64748b; font-size: .875rem; margin-bottom: 1rem; }
  .join-btn { display: inline-block; padding: .3rem .75rem; background: #6366f1; color: #fff;
              border-radius: 6px; text-decoration: none; font-size: .8rem; white-space: nowrap; }
  .join-btn:hover { background: #4f46e5; }
  .no-link { color: #94a3b8; font-size: .8rem; }
</style>
</head>
<body>
<h1>AESOP Scheduler — All Bookings</h1>
<div class="count"><?= count($rows) ?> booking<?= count($rows) !== 1 ? 's' : '' ?></div>
<?php if ($rows): ?>
<table>
  <thead>
    <tr>
      <th>#</th>
      <th>Name</th>
      <th>Email</th>
      <th>Start (<?= OWNER_TIMEZONE ?>)</th>
      <th>End</th>
      <th>Teams Link</th>
      <th>Booked at</th>
    </tr>
  </thead>
  <tbody>
  <?php foreach ($rows as $r): ?>
    <tr>
      <td><?= $r['id'] ?></td>
      <td><?= htmlspecialchars($r['guest_name']) ?></td>
      <td><a href="mailto:<?= htmlspecialchars($r['guest_email']) ?>"><?= htmlspecialchars($r['guest_email']) ?></a></td>
      <td><?= htmlspecialchars($r['start_time']) ?></td>
      <td><?= htmlspecialchars($r['end_time']) ?></td>
      <td>
        <?php if ($r['join_url']): ?>
          <a class="join-btn" href="<?= htmlspecialchars($r['join_url']) ?>" target="_blank">Join</a>
        <?php elseif ($r['graph_err']): ?>
          <span class="no-link" title="<?= htmlspecialchars($r['graph_err']) ?>">⚠ error</span>
        <?php else: ?>
          <span class="no-link">—</span>
        <?php endif; ?>
      </td>
      <td><?= htmlspecialchars($r['created_at']) ?></td>
    </tr>
  <?php endforeach; ?>
  </tbody>
</table>
<?php else: ?>
<p>No bookings yet.</p>
<?php endif; ?>
</body>
</html>
