param(
  [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot\.."),
  [string]$SpecFile = "CalculadoraFlet.spec",
  [string]$IssFile = "installer\CalculadoraFlet.iss",
  [string]$Publisher = "Minha Empresa",
  [string]$Version = "1.0.0",
  [string]$IsccPath = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Set-Location $ProjectRoot

function Resolve-IsccPath {
  if ($IsccPath -and (Test-Path $IsccPath)) { return (Resolve-Path $IsccPath).Path }

  $cmd = Get-Command iscc.exe -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }

  $candidates = @(
    "${env:LocalAppData}\Programs\Inno Setup 6\ISCC.exe",
    "${env:LocalAppData}\Programs\Inno Setup 5\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 5\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 5\ISCC.exe"
  ) | Where-Object { $_ -and (Test-Path $_) }

  if ($candidates.Count -gt 0) { return $candidates[0] }

  $uninstallRoots = @(
    'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
    'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
  )

  foreach ($root in $uninstallRoots) {
    if (-not (Test-Path $root)) { continue }
    foreach ($subkey in (Get-ChildItem $root -ErrorAction SilentlyContinue)) {
      try {
        $p = Get-ItemProperty $subkey.PSPath -ErrorAction Stop
        if ($p.DisplayName -and $p.DisplayName -match 'Inno Setup') {
          $installLocation = $p.InstallLocation
          if ($installLocation) {
            $iscc = Join-Path $installLocation 'ISCC.exe'
            if (Test-Path $iscc) { return $iscc }
          }
        }
      } catch {
        continue
      }
    }
  }

  return $null
}

# 1) Build onedir
& "$PSScriptRoot\build_portable.ps1" -ProjectRoot $ProjectRoot -SpecFile $SpecFile

# 2) Compilar instalador (Inno Setup)
Write-Host "Procurando ISCC.exe (Inno Setup)..." -ForegroundColor Cyan
$isccPath = Resolve-IsccPath
if (-not $isccPath) {
  throw "ISCC.exe não encontrado. Dica: no seu PC ele pode estar em '%LOCALAPPDATA%\\Programs\\Inno Setup 6\\ISCC.exe'. Você também pode passar -IsccPath 'C:\\caminho\\ISCC.exe'."
}

Write-Host "Usando: $isccPath" -ForegroundColor DarkGray
Write-Host "Compilando instalador: $IssFile" -ForegroundColor Cyan
& $isccPath "/DMyAppPublisher=$Publisher" "/DMyAppVersion=$Version" "$IssFile"

Write-Host "OK: instalador gerado em installer_output\\" -ForegroundColor Green
