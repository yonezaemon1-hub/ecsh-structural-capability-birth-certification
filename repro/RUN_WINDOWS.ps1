$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
$python = if($pythonCmd){ $pythonCmd.Source } else { 'C:\Users\meteo\AppData\Local\Programs\Python\Python310\python.exe' }
if(-not (Test-Path $python)){ throw "Python not found: $python" }

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$outDir = Join-Path $here "RUN_$stamp"
New-Item -ItemType Directory -Path $outDir | Out-Null

$inputs = @('ecsh_repro.py','ECSH_REPRO_SPEC.json','README.txt')
$manifest = foreach($f in $inputs){
    $p = Join-Path $here $f
    $h = Get-FileHash -Algorithm SHA256 -LiteralPath $p
    [pscustomobject]@{ File=$f; SHA256=$h.Hash }
}
$manifest | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $outDir 'INPUT_SHA256_MANIFEST.json')

$seed = 20260816
$json = Join-Path $outDir "results_seed_$seed.json"
$log  = Join-Path $outDir "stdout_seed_$seed.txt"
& $python (Join-Path $here 'ecsh_repro.py') --spec (Join-Path $here 'ECSH_REPRO_SPEC.json') --seed $seed --out $json 2>&1 | Tee-Object -FilePath $log
if($LASTEXITCODE -ne 0){ throw "Experiment failed for seed $seed" }

Get-ChildItem $outDir -File | Get-FileHash -Algorithm SHA256 |
    Select-Object Path,Hash | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $outDir 'OUTPUT_SHA256_MANIFEST.json')

Write-Host "`nPASS_ECSH_CANONICAL_REPRO_EXECUTED" -ForegroundColor Green
Write-Host "Evidence: $outDir"
