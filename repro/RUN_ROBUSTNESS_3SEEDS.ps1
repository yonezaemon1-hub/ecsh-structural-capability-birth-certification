$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
$python = if($pythonCmd){ $pythonCmd.Source } else { 'C:\Users\meteo\AppData\Local\Programs\Python\Python310\python.exe' }
if(-not (Test-Path $python)){ throw "Python not found: $python" }
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$outDir = Join-Path $here "ROBUSTNESS_$stamp"
New-Item -ItemType Directory -Path $outDir | Out-Null
foreach($seed in @(20260816,20260817,20260818)){
    $json = Join-Path $outDir "results_seed_$seed.json"
    $log  = Join-Path $outDir "stdout_seed_$seed.txt"
    & $python (Join-Path $here 'ecsh_repro.py') --spec (Join-Path $here 'ECSH_REPRO_SPEC.json') --seed $seed --out $json 2>&1 | Tee-Object -FilePath $log
    if($LASTEXITCODE -ne 0){ throw "Experiment failed for seed $seed" }
}
Write-Host "`nPASS_ECSH_ROBUSTNESS_3SEEDS_EXECUTED" -ForegroundColor Green
Write-Host "Evidence: $outDir"
