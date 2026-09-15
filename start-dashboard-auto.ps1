# Auto-detect Vite port and open browser
Set-Location $PSScriptRoot

$job = Start-Job -ScriptBlock {
    Set-Location $using:PSScriptRoot
    npm run dev
}

$portFound = $null
$timeout = 30
$elapsed = 0
while ($elapsed -lt $timeout) {
    $output = Receive-Job $job -Keep
    if ($output) {
        foreach ($line in $output) {
            if ($line -match 'Local:\s+http://127\.0\.0\.1:(\d+)') {
                $portFound = $matches[1]
                break
            }
        }
    }
    if ($portFound) { break }
    Start-Sleep -Seconds 1
    $elapsed++
}

if (-not $portFound) {
    Write-Host "No se pudo detectar el puerto. Se asume 5178"
    $portFound = 5178
}

Start-Process "http://127.0.0.1:$portFound"
Write-Host "Dashboard abierto en http://127.0.0.1:$portFound"
