param(
  [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot\.."),
  [switch]$KeepDist,
  [switch]$KeepBuild
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Set-Location $ProjectRoot

function Remove-IfExists([string]$PathToRemove) {
  if (Test-Path $PathToRemove) {
    Write-Host "Removendo: $PathToRemove" -ForegroundColor Cyan
    Remove-Item -Recurse -Force $PathToRemove
  }
}

# Artefatos do PyInstaller
if (-not $KeepDist) { Remove-IfExists ".\dist" }
if (-not $KeepBuild) { Remove-IfExists ".\build" }

# Saída do instalador
Remove-IfExists ".\installer\installer_output"

# Cache Python
Get-ChildItem -Recurse -Force -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
  ForEach-Object { Remove-IfExists $_.FullName }

Get-ChildItem -Recurse -Force -File -Include "*.pyc","*.pyo" -ErrorAction SilentlyContinue |
  Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "OK: limpeza concluída." -ForegroundColor Green
