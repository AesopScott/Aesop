$lines = Get-Content 'C:\Users\scott\Code\Aesop\ai-academy\courses.html' -Encoding UTF8

# Check dv-13 and dv-15 panels
foreach ($panelId in @('dv-13','dv-15')) {
    Write-Host "=== $panelId ==="
    $started = $false
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "id=""$panelId""") { $started = $true }
        if ($started -and ($lines[$i] -match 'core-badge|core-panel__cta')) {
            Write-Host "L$($i+1): $($lines[$i].Trim())"
        }
        if ($started -and $i -gt 0 -and $lines[$i] -match 'class="core-panel"' -and $lines[$i] -notmatch "id=""$panelId""") { break }
    }
}

# Mega-menu check
Write-Host ""
Write-Host "=== MEGA-MENU: dv-13 and dv-16 ==="
for ($i = 0; $i -lt $lines.Count; $i++) {
    if (($lines[$i] -match 'dv-13' -or $lines[$i] -match 'dv-16') -and $lines[$i] -match 'mega-link') {
        Write-Host "L$($i+1): $($lines[$i].Trim())"
    }
}

# Check remaining core-panel--cs on live panel IDs
Write-Host ""
Write-Host "=== REMAINING core-panel--cs ==="
$liveIds = @('cp7','cp8','cp10','cp11','cp13','cp14','cp15','cp17','am-1','am-8','ap-7','ar-1','ar-8','ar-10','bu-1','bu-2','bu-3','bu-4','bu-5','bu-7','bu-11','dv-1','dv-2','dv-3','dv-4','dv-5','dv-7','dv-9','dv-10','dv-13','dv-14','dv-15','dv-17')
$remaining = 0
foreach ($id in $liveIds) {
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "core-panel--cs" -and $lines[$i] -match "id=""$id""") {
            Write-Host "STILL HAS CS: $id at L$($i+1)"
            $remaining++
        }
    }
}
if ($remaining -eq 0) { Write-Host "All cleared!" }
