[Setup]
AppName=Texplorateur
AppVersion=1.0
DefaultDirName={pf}\Texplorateur
DefaultGroupName=Texplorateur
OutputBaseFilename=Install_Texplorateur
Compression=lzma
SolidCompression=yes
SetupIconFile=icone.ico
ArchitecturesInstallIn64BitMode=x64
AppPublisher=FUZZ STUDIOS
AppComments=Un outil de recherche pour retrouver vos fichiers Windows si vous ne vous souvenez pas du nom du fichier mais d'une phrase à l'interieur de celui-ci
AppContact=fredlobster71@gmail.com
LicenseFile=license.txt

[Files]
Source: "Texplorateur_V2.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Texplorateur"; Filename: "{app}\Texplorateur_V2.exe"
Name: "{group}\Désinstaller Texplorateur"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Texplorateur"; Filename: "{app}\Texplorateur_V2.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Créer une icône sur le bureau"; GroupDescription: "Icônes supplémentaires:"

[Run]
Filename: "{app}\Texplorateur_V2.exe"; Description: "Lancer Texplorateur"; Flags: nowait postinstall skipifsilent
