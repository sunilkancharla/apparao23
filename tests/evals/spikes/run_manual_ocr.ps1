# User-operated offline handoff. No downloads, Windows setting changes or OCR online.
$ErrorActionPreference = 'Stop'
$trialProjectRoot = 'F:\document_assistant'
$trialRunRoot = Join-Path $trialProjectRoot 'data\t09-manual-ocr\manual-01'
Set-Location -LiteralPath $trialProjectRoot
$trialMeterPath = Join-Path $trialRunRoot 'meter.json'
$trialMeter = Get-Content -Raw -Encoding UTF8 -LiteralPath $trialMeterPath | ConvertFrom-Json
if ($trialMeter.PSObject.Properties.Name -contains 'offline_started') {
    throw 'This run already started offline. Do not reset or retry its ledger.'
}
if ($trialMeter.reserved + 3 -gt $trialMeter.limit - 16) {
    throw 'Shared process budget cannot cover this handoff and cleanup.'
}
$trialEvent = @{slots=3; purpose='Manual offline PowerShell/venv redirector/controller'; at=[DateTimeOffset]::UtcNow.ToString('o')}
$trialMeter.reserved += 3
$trialMeter.events += $trialEvent
$trialMeter | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath $trialMeterPath
$trialEvent | ConvertTo-Json -Compress | Add-Content -Encoding UTF8 -LiteralPath (Join-Path $trialRunRoot 'events.jsonl')
Write-Host 'Disconnect Wi-Fi, Ethernet, tethering and all external links before answering the next prompt.'
Write-Host 'This synthetic-only trial has NO filesystem confinement. Keep the computer disconnected until teardown is verified.'
$trialNetwork = @{
    adapters=@(Get-NetAdapter -IncludeHidden | Select-Object ifIndex,Status,HardwareInterface)
    routes=@(Get-NetRoute | Where-Object { $_.DestinationPrefix -in @('0.0.0.0/0','::/0') } |
        Select-Object InterfaceIndex,AddressFamily,DestinationPrefix,NextHop,State)
}
$trialNetwork | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $trialRunRoot 'local-network-metadata.json')
& (Join-Path $trialProjectRoot '.venv\Scripts\python.exe') -I -S -B `
    (Join-Path $trialProjectRoot 'tests\evals\spikes\ocr_trial.py') offline
$trialSummaryPath = Join-Path $trialRunRoot 'summary.json'
if (Test-Path -LiteralPath $trialSummaryPath) {
    $trialSummary = Get-Content -Raw -Encoding UTF8 -LiteralPath $trialSummaryPath | ConvertFrom-Json
    Write-Host "Trial status: $($trialSummary.status)"
    if ($trialSummary.teardown_verified -eq $true) {
        Write-Host 'Owned trial workers have stopped. You may reconnect and report the status.'
    } else {
        Write-Host 'REMAIN DISCONNECTED: teardown is unverified. Stop the owned trial process tree before reconnecting.'
    }
} else {
    Write-Host 'No completion report. Remain disconnected until you confirm the controller and its owned workers have stopped.'
}
