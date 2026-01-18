param(
  [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot\.."),
  [string]$SpecFile = "CalculadoraFlet.spec"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Set-Location $ProjectRoot

Write-Host "[1/2] Limpando dist/build..." -ForegroundColor Cyan
if (Test-Path .\dist) { Remove-Item -Recurse -Force .\dist }
if (Test-Path .\build) { Remove-Item -Recurse -Force .\build }

Write-Host "[2/2] Gerando build onedir via PyInstaller ($SpecFile)..." -ForegroundColor Cyan
pyinstaller --noconfirm --clean "$SpecFile"

Write-Host "OK: build gerado em dist\\CalculadoraFlet" -ForegroundColor Green
