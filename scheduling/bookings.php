<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/db.php';

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
  td { padding: .65rem 1rem; border-bottom: 1px solid #e2e8f0; font-size: .875rem; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #f1f5f9; }
  .count { color: #64748b; font-size: .875rem; margin-bottom: 1rem; }
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
