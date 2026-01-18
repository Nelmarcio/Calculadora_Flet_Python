# Calculadora Flet (Windows)

Projeto de calculadora feita com **Flet** e empacotada para Windows com **PyInstaller (onedir)** + **Inno Setup**.

## Requisitos

- Windows 10/11
- Python (recomendado 3.11/3.12)
- Inno Setup 6 (para gerar o instalador)

> Observação: builds com `--onefile` tendem a disparar mais falso-positivo de antivírus. Este projeto usa `onedir` + instalador.

## Rodar em modo desenvolvimento

```powershell
# na raiz do projeto
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\Calculadora_Flet.py
```

## Gerar executável (pasta onedir)

Gera `dist\CalculadoraFlet\CalculadoraFlet.exe`.

```powershell
.\.venv\Scripts\Activate.ps1
pyinstaller --noconfirm --clean CalculadoraFlet.spec
```

Ou usando o script:

```powershell
.\.scripts\build_portable.ps1
```

## Gerar instalador (Inno Setup)

1. Instale o Inno Setup 6.

2. (Opcional) adicione um ícone:

- coloque um arquivo `.ico` em `installer\app.ico`

3. Gere o instalador:

```powershell
.\.scripts\build_installer.ps1 -Publisher "Sua Empresa" -Version "1.0.0"
```

Se o Inno Setup estiver instalado por usuário (ex.: `AppData`), você pode passar o caminho do `ISCC.exe`:

```powershell
.\.scripts\build_installer.ps1 -Publisher "Sua Empresa" -Version "1.0.0" -IsccPath "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"
```

Saída:

- `installer_output\Instalador_Calculadora Flet_vX.Y.Z.exe`

O instalador:

- instala em **Arquivos de Programas**
- cria atalho no **Menu Iniciar**
- cria atalho na **Área de Trabalho** (opcional/selecionável)

### Gerar direto pelo Inno Setup (GUI)

1. Gere primeiro o app (PyInstaller `onedir`):

```powershell
pyinstaller --noconfirm --clean CalculadoraFlet.spec
```

2. (Opcional) coloque o ícone do instalador em `installer\app.ico`.

3. Abra o Inno Setup Compiler (Compil32.exe).

4. No Inno Setup: **File > Open...** e abra `installer\CalculadoraFlet.iss`.

5. (Opcional) ajuste no topo do `.iss`:

- `#define MyAppPublisher "Sua Empresa"`
- `#define MyAppVersion "1.0.0"`

6. Clique em **Compile**.

Saída: `installer_output\Instalador_Calculadora Flet_vX.Y.Z.exe`

## Limpar artefatos gerados

Remove `build/`, `dist/` e `installer/installer_output/`.

```powershell
.\.scripts\clean.ps1
```

## Scripts

- `scripts/clean.ps1`: remove artefatos gerados (PyInstaller + saída do instalador) e caches Python.
  - exemplos: `./scripts/clean.ps1`, `./scripts/clean.ps1 -KeepDist`.
- `scripts/build_portable.ps1`: gera o build **onedir** em `dist/CalculadoraFlet/` usando `CalculadoraFlet.spec`.
- `scripts/build_installer.ps1`: gera o instalador.
  - faz o build onedir automaticamente e depois compila `installer/CalculadoraFlet.iss` com Inno Setup.
  - exemplos: `./scripts/build_installer.ps1 -Publisher "Sua Empresa" -Version "1.0.0"`.

## Assinatura digital (opcional)

Para reduzir alertas do SmartScreen/antivírus, use um certificado de **Code Signing** e assine o `.exe` do instalador e/ou o app.
Ferramenta: `signtool.exe` (Windows SDK).

## Estrutura

- `Calculadora_Flet.py`: app
- `CalculadoraFlet.spec`: build PyInstaller (onedir)
- `installer/CalculadoraFlet.iss`: instalador Inno Setup
- `scripts/`: scripts de build/clean
