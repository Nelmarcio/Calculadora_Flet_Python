; Inno Setup script para empacotar o build onedir do PyInstaller.
; Requisitos:
; 1) Gerar build: pyinstaller --noconfirm --clean CalculadoraFlet.spec
; 2) Instalar Inno Setup e compilar: iscc installer\CalculadoraFlet.iss
;
; Você pode sobrescrever defines na linha de comando:
;   iscc /DMyAppPublisher="Minha Empresa" /DMyAppVersion="1.2.3" installer\CalculadoraFlet.iss

#ifndef MyAppName
	#define MyAppName "Calculadora Flet"
#endif

#ifndef MyAppExeName
	#define MyAppExeName "CalculadoraFlet.exe"
#endif

#ifndef MyAppPublisher
	#define MyAppPublisher "Minha Empresa"
#endif

#ifndef MyAppURL
	#define MyAppURL ""
#endif

#ifndef MyAppVersion
	#define MyAppVersion "1.0.0"
#endif

; Ícone opcional: coloque um arquivo installer\app.ico
#define MyAppSetupIcon "app.ico"

[Setup]
AppId={{9D7D5F7C-6A0D-4C0F-8E7B-5A2D2A0B4F25}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=Instalador_{#MyAppName}_v{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

PrivilegesRequired=admin

VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName}

; Se existir installer\app.ico, usa como ícone do instalador.
#ifexist MyAppSetupIcon
SetupIconFile={#MyAppSetupIcon}
UninstallDisplayIcon={app}\{#MyAppExeName}
#endif

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"; Flags: checkedonce

[Files]
; Copia tudo do build onedir (dist\CalculadoraFlet\...)
Source: "..\dist\CalculadoraFlet\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir {#MyAppName}"; Flags: nowait postinstall skipifsilent
