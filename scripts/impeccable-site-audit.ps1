param(
  [switch]$Json,
  [switch]$Gpt,
  [switch]$Gemini,
  [switch]$FailOnFindings,
  [int]$ChunkSize = 80,
  [string]$OutFile = "",
  [string[]]$ExtraTargets = @()
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $repoRoot

$designFilePattern = '\.(html|css|jsx|tsx|vue|svelte)$'
$excludedPatterns = @(
  '(^|/)\.agents/',
  '(^|/)\.impeccable/',
  '(^|/)\.git/',
  '(^|/)archive/',
  '(^|/)ai-academy/archive/',
  '(^|/)ai-academy/admin/archive/',
  '(^|/)ai-academy/modules/archive/',
  '(^|/)ai-academy/modules/[^/]+/archive/',
  '(^|/)docs/',
  '(^|/)models/',
  '(^|/)__pycache__/',
  '(^|/)node_modules/',
  '(^|/)cloudflare/'
)

function Test-IsExcludedDesignFile {
  param([string]$Path)
  $normalized = $Path -replace '\\', '/'
  foreach ($pattern in $excludedPatterns) {
    if ($normalized -match $pattern) {
      return $true
    }
  }
  return $false
}

$targets = @(
  git ls-files |
    Where-Object { $_ -match $designFilePattern } |
    Where-Object { -not (Test-IsExcludedDesignFile $_) } |
    Where-Object { Test-Path -LiteralPath $_ }
)

foreach ($target in $ExtraTargets) {
  if ($target -and $target.Trim()) {
    $targets += $target.Trim()
  }
}

$targets = @($targets | Sort-Object -Unique)

if (-not $targets.Count) {
  throw "No design files found for Impeccable audit."
}

$allFindings = New-Object System.Collections.Generic.List[object]
$failedChunks = New-Object System.Collections.Generic.List[string]

for ($i = 0; $i -lt $targets.Count; $i += $ChunkSize) {
  $end = [Math]::Min($i + $ChunkSize - 1, $targets.Count - 1)
  $chunk = @($targets[$i..$end])
  $argsList = @("impeccable", "detect", "--json")
  if ($Gpt) { $argsList += "--gpt" }
  if ($Gemini) { $argsList += "--gemini" }
  $argsList += $chunk

  $output = & npx @argsList 2>&1
  $exitCode = $LASTEXITCODE
  $text = ($output | Out-String).Trim()

  if ($text) {
    try {
      $parsed = $text | ConvertFrom-Json
      foreach ($item in @($parsed)) {
        $allFindings.Add($item) | Out-Null
      }
    } catch {
      $failedChunks.Add("Chunk $($i + 1)-$($end + 1): unable to parse Impeccable JSON output. Exit $exitCode. Output: $text") | Out-Null
    }
  }

  if ($exitCode -ne 0 -and $exitCode -ne 2) {
    $failedChunks.Add("Chunk $($i + 1)-$($end + 1): Impeccable exited with code $exitCode.") | Out-Null
  }
}

$summary = [ordered]@{
  scannedFiles = $targets.Count
  findingCount = $allFindings.Count
  failedChunkCount = $failedChunks.Count
  bySeverity = [ordered]@{}
  byAntipattern = [ordered]@{}
  findings = @($allFindings.ToArray())
  failedChunks = @($failedChunks.ToArray())
}

foreach ($finding in $allFindings) {
  $severity = if ($finding.severity) { [string]$finding.severity } else { "unknown" }
  $name = if ($finding.antipattern) { [string]$finding.antipattern } else { "unknown" }

  if (-not $summary.bySeverity.Contains($severity)) {
    $summary.bySeverity[$severity] = 0
  }
  $summary.bySeverity[$severity]++

  if (-not $summary.byAntipattern.Contains($name)) {
    $summary.byAntipattern[$name] = 0
  }
  $summary.byAntipattern[$name]++
}

$jsonText = $summary | ConvertTo-Json -Depth 8

if ($OutFile.Trim()) {
  $outPath = if ([System.IO.Path]::IsPathRooted($OutFile)) { $OutFile } else { Join-Path $repoRoot $OutFile }
  New-Item -ItemType Directory -Force (Split-Path $outPath -Parent) | Out-Null
  Set-Content -LiteralPath $outPath -Value $jsonText -Encoding UTF8
}

if ($Json) {
  $jsonText
} else {
  Write-Host "Impeccable full-site design audit" -ForegroundColor Cyan
  Write-Host "Scanned files: $($summary.scannedFiles)"
  Write-Host "Findings: $($summary.findingCount)"
  if ($summary.failedChunkCount) {
    Write-Host "Failed chunks: $($summary.failedChunkCount)" -ForegroundColor Yellow
  }
  Write-Host ""
  Write-Host "Findings by antipattern:"
  $summary.byAntipattern.GetEnumerator() |
    Sort-Object Value -Descending |
    ForEach-Object { Write-Host ("  {0}: {1}" -f $_.Key, $_.Value) }
  Write-Host ""
  Write-Host "Top findings:"
  $allFindings |
    Select-Object -First 25 |
    ForEach-Object {
      Write-Host ("  [{0}] {1} - {2}:{3}" -f $_.severity, $_.name, $_.file, $_.line)
    }
}

if ($failedChunks.Count -gt 0) {
  exit 1
}

if ($FailOnFindings -and $allFindings.Count -gt 0) {
  exit 2
}
