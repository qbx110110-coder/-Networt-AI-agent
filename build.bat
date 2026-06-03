@echo off
REM Build script for Network AI Agent on Windows
REM This script creates an executable and installer for Windows

setlocal enabledelayedexpansion

echo.
echo =========================================================
echo Network AI Agent - Windows Build Script
echo =========================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Installing build dependencies...
pip install -r requirements-build.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/4] Building executable...
python build_installer.py
if errorlevel 1 (
    echo Error: Failed to build executable
    pause
    exit /b 1
)

echo.
echo =========================================================
echo Build Complete!
echo =========================================================
echo.
echo Output Files:
echo   - Executable: dist\NetworkAIAgent\NetworkAIAgent.exe
echo   - Installer: Network-AI-Agent-Setup.exe (if NSIS installed)
echo.
echo Installation Instructions:
echo   1. Run Network-AI-Agent-Setup.exe to install
echo   2. Configure your OpenAI API key in .env file
echo   3. Update config/config.yaml with your device settings
echo   4. Run the application from Start Menu
echo.
echo Note: To create the installer, install NSIS from:
echo   https://nsis.sourceforge.io
echo.
pause
