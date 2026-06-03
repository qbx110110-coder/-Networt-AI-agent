# NSIS Installer Script for Network AI Agent

; Include modern interface
!include "MUI2.nsh"
!include "x64.nsh"
!include "WinVer.nsh"

; Basic settings
Name "Network AI Agent"
OutFile "Network-AI-Agent-Setup.exe"
InstallDir "$PROGRAMFILES\NetworkAIAgent"
InstallDirRegKey HKCU "Software\NetworkAIAgent" "Install_Dir"

; Request admin privileges
RequestExecutionLevel admin

; MUI Settings
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "SimpChinese"

; Installer version info
VIProductVersion "1.0.0.0"
VIAddVersionKey /LANG=1033 "ProductName" "Network AI Agent"
VIAddVersionKey /LANG=1033 "Comments" "Intelligent Network Device Configuration Agent with LLM Integration"
VIAddVersionKey /LANG=1033 "CompanyName" "Network AI Team"
VIAddVersionKey /LANG=1033 "FileDescription" "Network AI Agent Installer"
VIAddVersionKey /LANG=1033 "FileVersion" "1.0.0.0"
VIAddVersionKey /LANG=1033 "ProductVersion" "1.0.0.0"
VIAddVersionKey /LANG=1033 "LegalCopyright" "MIT License"

Section "Install"
  SetOutPath "$INSTDIR"
  
  ; Copy files from build directory
  File /r "dist\NetworkAIAgent\*.*"
  
  ; Create shortcuts
  CreateDirectory "$SMPROGRAMS\NetworkAIAgent"
  CreateShortCut "$SMPROGRAMS\NetworkAIAgent\Network AI Agent.lnk" "$INSTDIR\NetworkAIAgent.exe"
  CreateShortCut "$SMPROGRAMS\NetworkAIAgent\Uninstall.lnk" "$INSTDIR\uninstall.exe"
  
  ; Create desktop shortcut
  CreateShortCut "$DESKTOP\Network AI Agent.lnk" "$INSTDIR\NetworkAIAgent.exe"
  
  ; Copy config files
  SetOverwrite try
  File ".env.example"
  File "README.md"
  
  ; Write registry keys
  WriteRegStr HKCU "Software\NetworkAIAgent" "Install_Dir" "$INSTDIR"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\NetworkAIAgent" "DisplayName" "Network AI Agent"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\NetworkAIAgent" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\NetworkAIAgent" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\NetworkAIAgent" "Publisher" "Network AI Team"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\NetworkAIAgent" "URLInfoAbout" "https://github.com/qbx110110-coder/-Networt-AI-agent"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\NetworkAIAgent" "DisplayVersion" "1.0.0"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
SectionEnd

Section "Uninstall"
  ; Remove registry keys
  DeleteRegKey HKCU "Software\NetworkAIAgent"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\NetworkAIAgent"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\NetworkAIAgent\Network AI Agent.lnk"
  Delete "$SMPROGRAMS\NetworkAIAgent\Uninstall.lnk"
  RMDir "$SMPROGRAMS\NetworkAIAgent"
  Delete "$DESKTOP\Network AI Agent.lnk"
  
  ; Remove installation directory
  RMDir /r "$INSTDIR"
  
SectionEnd
