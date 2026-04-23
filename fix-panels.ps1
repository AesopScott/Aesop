$file = 'C:\Users\scott\Code\Aesop\ai-academy\courses.html'
$content = Get-Content $file -Raw -Encoding UTF8
$changes = @()

# ============================================================
# MEGA-MENU FIXES
# ============================================================

# dv-13: --soon -> --live
$old = "class=""mega-link mega-link--soon"" data-panel=""dv-13"" onclick=""megaSelect(this,'dv-13')"">AI Security and Red-Teaming</button>"
$new = "class=""mega-link mega-link--live"" data-panel=""dv-13"" onclick=""megaSelect(this,'dv-13')"">AI Security and Red-Teaming</button>"
if ($content.Contains($old)) { $content = $content.Replace($old, $new); $changes += 'dv-13 mega: --soon->--live' }
else { $changes += 'WARN: dv-13 mega string not found' }

# dv-16: --live -> --soon
$old = "class=""mega-link mega-link--live"" data-panel=""dv-16"" onclick=""megaSelect(this,'dv-16')"">Security Auditing for AI-Generated Code</button>"
$new = "class=""mega-link mega-link--soon"" data-panel=""dv-16"" onclick=""megaSelect(this,'dv-16')"">Security Auditing for AI-Generated Code</button>"
if ($content.Contains($old)) { $content = $content.Replace($old, $new); $changes += 'dv-16 mega: --live->--soon' }
else { $changes += 'WARN: dv-16 mega string not found' }

# ============================================================
# REMOVE core-panel--cs FROM ALREADY-LIVE PANELS
# (badge is already core-badge-live, CTA is already Enter Course link)
# ============================================================
$livePanels = @(
    'cp7','cp8','cp10','cp11','cp13','cp14','cp15','cp17',
    'am-1','am-8','ap-7',
    'ar-1','ar-8','ar-10',
    'bu-1','bu-2','bu-3','bu-4','bu-5','bu-7','bu-11',
    'dv-1','dv-2','dv-3','dv-4','dv-5','dv-7','dv-9','dv-10','dv-14','dv-17'
)
foreach ($id in $livePanels) {
    $old = "class=""core-panel core-panel--cs"" id=""$id"""
    $new = "class=""core-panel"" id=""$id"""
    if ($content.Contains($old)) { $content = $content.Replace($old, $new); $changes += "$id`: removed core-panel--cs" }
    else { $changes += "WARN: $id core-panel--cs not found" }
}

# ============================================================
# dv-13 PANEL: activate badge + CTA + remove cs class
# ============================================================

# Panel div class
$old = "class=""core-panel core-panel--cs"" id=""dv-13"""
$new = "class=""core-panel"" id=""dv-13"""
if ($content.Contains($old)) { $content = $content.Replace($old, $new); $changes += 'dv-13 panel: removed core-panel--cs' }
else { $changes += 'WARN: dv-13 panel div not found' }

# Badge: unique anchor = the desc text for dv-13
$old = @"
          <div class="core-panel__badges">
            <span class="core-badge-cs">Coming Soon</span>
            <span class="core-badge-mods">8 Modules</span>
          </div>
        </div>
        <div class="core-modules-label">Course modules</div>
        <div class="core-modules-grid">
          <div class="core-mod">
            <div class="core-mod__num">M1</div>
            <div class="core-mod__info">
              <div class="core-mod__title">The AI Security Threat Model</div>
"@
$new = @"
          <div class="core-panel__badges">
            <span class="core-badge-live"><span class="live-dot"></span> Live</span>
            <span class="core-badge-mods">8 Modules</span>
          </div>
        </div>
        <div class="core-modules-label">Course modules</div>
        <div class="core-modules-grid">
          <div class="core-mod">
            <div class="core-mod__num">M1</div>
            <div class="core-mod__info">
              <div class="core-mod__title">The AI Security Threat Model</div>
"@
if ($content.Contains($old)) { $content = $content.Replace($old, $new); $changes += 'dv-13: badge fixed' }
else { $changes += 'WARN: dv-13 badge context not found' }

# Ghost CTA -> Enter Course (unique anchor: the M8 module title + CTA + next panel id)
$old = @"
        </div>
        <span class="core-panel__cta core-panel__cta--ghost">Coming Soon</span>
      </div>
      <div class="core-panel core-panel--cs" id="dv-14">
"@
$new = @"
        </div>
        <a href="/ai-academy/modules/electives-hub.html?course=ai-security-and-red-teaming" class="core-panel__cta">Enter Course &rarr;</a>
      </div>
      <div class="core-panel" id="dv-14">
"@
if ($content.Contains($old)) { $content = $content.Replace($old, $new); $changes += 'dv-13: CTA fixed (also fixed dv-14 class)' }
else { $changes += 'WARN: dv-13 CTA context not found' }

# ============================================================
# dv-15 PANEL: activate badge + CTA + remove cs class
# ============================================================

# Panel div class
$old = "class=""core-panel core-panel--cs"" id=""dv-15"""
$new = "class=""core-panel"" id=""dv-15"""
if ($content.Contains($old)) { $content = $content.Replace($old, $new); $changes += 'dv-15 panel: removed core-panel--cs' }
else { $changes += 'WARN: dv-15 panel div not found' }

# Badge (unique anchor: dv-15's M1 module title)
$old = @"
          <div class="core-panel__badges">
            <span class="core-badge-cs">Coming Soon</span>
            <span class="core-badge-mods">8 Modules</span>
          </div>
        </div>
        <div class="core-modules-label">Course modules</div>
        <div class="core-modules-grid">
          <div class="core-mod"><div class="core-mod__num">M1</div><div class="core-mod__info"><div class="core-mod__title">Why AI Code Needs a Different Review Process</div>
"@
$new = @"
          <div class="core-panel__badges">
            <span class="core-badge-live"><span class="live-dot"></span> Live</span>
            <span class="core-badge-mods">8 Modules</span>
          </div>
        </div>
        <div class="core-modules-label">Course modules</div>
        <div class="core-modules-grid">
          <div class="core-mod"><div class="core-mod__num">M1</div><div class="core-mod__info"><div class="core-mod__title">Why AI Code Needs a Different Review Process</div>
"@
if ($content.Contains($old)) { $content = $content.Replace($old, $new); $changes += 'dv-15: badge fixed' }
else { $changes += 'WARN: dv-15 badge context not found' }

# Ghost CTA -> Enter Course
$old = @"
        <span class="core-panel__cta core-panel__cta--ghost">In Development</span>
      </div>

      <div class="core-panel core-panel--cs" id="dv-16">
"@
$new = @"
        <a href="/ai-academy/modules/electives-hub.html?course=ai-code-review-fundamentals" class="core-panel__cta">Enter Course &rarr;</a>
      </div>

      <div class="core-panel core-panel--cs" id="dv-16">
"@
if ($content.Contains($old)) { $content = $content.Replace($old, $new); $changes += 'dv-15: CTA fixed' }
else { $changes += 'WARN: dv-15 CTA context not found' }

# ============================================================
# WRITE FILE
# ============================================================
$content | Set-Content $file -NoNewline -Encoding UTF8

Write-Host "=== RESULTS ==="
$changes | ForEach-Object { Write-Host $_ }
Write-Host ""
Write-Host "Total operations: $($changes.Count)"
$warnings = $changes | Where-Object { $_ -match '^WARN' }
Write-Host "Warnings: $($warnings.Count)"
