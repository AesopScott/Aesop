# ============================================================
#  MeetingFlash.ps1  –  Full-screen flash reminder for Outlook
#  Runs silently in the background. Flashes your ENTIRE screen
#  red/white when an Outlook meeting is about to start.
# ============================================================
#
#  USAGE:
#    powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File "MeetingFlash.ps1"
#
#  CONFIG (edit these):
$MINUTES_BEFORE   = 1        # How many minutes before the meeting to flash
$CHECK_INTERVAL   = 30       # Seconds between calendar checks
$FLASH_CYCLES     = 6        # Number of flash on/off cycles
$FLASH_ON_MS      = 350      # Milliseconds the color is shown
$FLASH_OFF_MS     = 150      # Milliseconds between flashes
$FLASH_COLOR      = "Red"    # Flash color: Red, Orange, Yellow, etc.
# ============================================================

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- Build the full-screen overlay form (hidden until needed) ---
function Show-ScreenFlash {
    param(
        [string]$MeetingSubject,
        [datetime]$MeetingStart
    )

    $screenBounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds

    # Create a label with meeting info
    $timeStr = $MeetingStart.ToString("h:mm tt")

    for ($i = 0; $i -lt $FLASH_CYCLES; $i++) {
        # --- FLASH ON ---
        $form = New-Object System.Windows.Forms.Form
        $form.FormBorderStyle = 'None'
        $form.WindowState    = 'Maximized'
        $form.TopMost        = $true
        $form.BackColor      = [System.Drawing.Color]::FromName($FLASH_COLOR)
        $form.Opacity        = 0.85
        $form.ShowInTaskbar  = $false
        $form.StartPosition  = 'Manual'
        $form.Location       = New-Object System.Drawing.Point(0, 0)
        $form.Size           = New-Object System.Drawing.Size($screenBounds.Width, $screenBounds.Height)

        # Meeting name label
        $label = New-Object System.Windows.Forms.Label
        $label.Text      = "MEETING STARTING — $timeStr`n$MeetingSubject"
        $label.ForeColor = [System.Drawing.Color]::White
        $label.Font      = New-Object System.Drawing.Font("Segoe UI", 48, [System.Drawing.FontStyle]::Bold)
        $label.AutoSize  = $false
        $label.TextAlign = [System.Drawing.ContentAlignment]::MiddleCenter
        $label.Dock      = 'Fill'
        $form.Controls.Add($label)

        $form.Show()
        $form.BringToFront()
        [System.Windows.Forms.Application]::DoEvents()
        Start-Sleep -Milliseconds $FLASH_ON_MS
        $form.Close()
        $form.Dispose()

        # --- FLASH OFF (brief pause) ---
        Start-Sleep -Milliseconds $FLASH_OFF_MS
    }

    # --- Final hold: show the meeting info for 4 seconds so you can read it ---
    $form2 = New-Object System.Windows.Forms.Form
    $form2.FormBorderStyle = 'None'
    $form2.WindowState    = 'Maximized'
    $form2.TopMost        = $true
    $form2.BackColor      = [System.Drawing.Color]::FromName($FLASH_COLOR)
    $form2.Opacity        = 0.9
    $form2.ShowInTaskbar  = $false
    $form2.StartPosition  = 'Manual'
    $form2.Location       = New-Object System.Drawing.Point(0, 0)
    $form2.Size           = New-Object System.Drawing.Size($screenBounds.Width, $screenBounds.Height)

    $label2 = New-Object System.Windows.Forms.Label
    $label2.Text      = "MEETING NOW — $timeStr`n$MeetingSubject`n`n(click anywhere to dismiss)"
    $label2.ForeColor = [System.Drawing.Color]::White
    $label2.Font      = New-Object System.Drawing.Font("Segoe UI", 44, [System.Drawing.FontStyle]::Bold)
    $label2.AutoSize  = $false
    $label2.TextAlign = [System.Drawing.ContentAlignment]::MiddleCenter
    $label2.Dock      = 'Fill'
    $form2.Controls.Add($label2)

    # Click anywhere to dismiss
    $form2.Add_Click({ $form2.Close() })
    $label2.Add_Click({ $form2.Close() })

    # Auto-dismiss after 4 seconds via timer
    $timer = New-Object System.Windows.Forms.Timer
    $timer.Interval = 4000
    $timer.Add_Tick({ $form2.Close(); $timer.Stop() })
    $timer.Start()

    $form2.ShowDialog() | Out-Null
    $form2.Dispose()
}

# --- Connect to Outlook and poll the calendar ---
function Get-UpcomingMeetings {
    try {
        $outlook   = New-Object -ComObject Outlook.Application
        $namespace = $outlook.GetNamespace("MAPI")
        $calendar  = $namespace.GetDefaultFolder(9)  # 9 = olFolderCalendar
        $now       = Get-Date
        $windowEnd = $now.AddMinutes($MINUTES_BEFORE + 1)

        $filter = "[Start] >= '$($now.ToString("g"))' AND [Start] <= '$($windowEnd.ToString("g"))'"
        $items  = $calendar.Items
        $items.Sort("[Start]")
        $items.IncludeRecurrences = $true
        $results = $items.Restrict($filter)

        $meetings = @()
        foreach ($item in $results) {
            $meetings += [PSCustomObject]@{
                Subject = $item.Subject
                Start   = $item.Start
            }
        }
        return $meetings
    }
    catch {
        Write-Host "$(Get-Date -Format 'HH:mm:ss') - Outlook COM error: $_" -ForegroundColor Yellow
        return @()
    }
}

# --- Main loop ---
Write-Host "============================================"
Write-Host " MeetingFlash is running"
Write-Host " Checking every ${CHECK_INTERVAL}s for meetings"
Write-Host " Will flash ${MINUTES_BEFORE} minute(s) before start"
Write-Host " Press Ctrl+C to stop"
Write-Host "============================================"

$alreadyFlashed = @{}   # Track meetings we already flashed for

while ($true) {
    $meetings = Get-UpcomingMeetings

    foreach ($mtg in $meetings) {
        $key = "$($mtg.Subject)|$($mtg.Start.ToString('o'))"
        $minutesUntil = ($mtg.Start - (Get-Date)).TotalMinutes

        if ($minutesUntil -le $MINUTES_BEFORE -and $minutesUntil -ge -1 -and -not $alreadyFlashed.ContainsKey($key)) {
            Write-Host "$(Get-Date -Format 'HH:mm:ss') - FLASHING: $($mtg.Subject) at $($mtg.Start.ToString('h:mm tt'))" -ForegroundColor Red
            $alreadyFlashed[$key] = $true
            Show-ScreenFlash -MeetingSubject $mtg.Subject -MeetingStart $mtg.Start
        }
    }

    # Clean up old entries (meetings more than 10 min ago)
    $keysToRemove = @()
    foreach ($k in $alreadyFlashed.Keys) {
        $parts = $k -split '\|'
        if ($parts.Count -eq 2) {
            $mStart = [datetime]::Parse($parts[1])
            if (($mStart - (Get-Date)).TotalMinutes -lt -10) {
                $keysToRemove += $k
            }
        }
    }
    foreach ($k in $keysToRemove) { $alreadyFlashed.Remove($k) }

    Start-Sleep -Seconds $CHECK_INTERVAL
}
