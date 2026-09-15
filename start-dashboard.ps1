# Start Dashboard Apuestas with auto port detection
$ErrorActionPreference = 'Continue'
Set-Location $PSScriptRoot

$port = 5178
Write-Host "Iniciando Vite en $port..."
Start-Process powershell -ArgumentList "-NoExit","-Command","npm run dev -- --host 127.0.0.1 --port $port" -WindowStyle Normal

Write-Host "Esperando a que el servidor esté listo..."
Start-Sleep -Seconds 4

$maxAttempts = 15
$attempt = 0
while ($attempt -lt $maxAttempts) {
    try {
        $req = Invoke-WebRequest -Uri "http://127.0.0.1:$port/" -UseBasicParsing -TimeoutSec 2
        if ($req.StatusCode -eq 200) { break }
    } catch {}
    Start-Sleep -Seconds 1
    $attempt++
}

Start-Process "http://127.0.0.1:$port"
Write-Host "Dashboard abierto en http://127.0.0.1:$port"
