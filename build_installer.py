#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Installer script for Network AI Agent
Creates a Windows installer using NSIS
"""

import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    """Build executable using PyInstaller"""
    print("="*60)
    print("Building Network AI Agent Executable...")
    print("="*60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Error: PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Build executable
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--add-data", "config:config",
        "--add-data", ".env.example:.",
        "--add-data", "README.md:.",
        "--hidden-import=paramiko",
        "--hidden-import=openai",
        "--hidden-import=yaml",
        "--hidden-import=dotenv",
        "--name=NetworkAIAgent",
        "--icon=assets/icon.ico" if Path("assets/icon.ico").exists() else "",
        "src/main.py"
    ]
    
    # Remove empty strings
    cmd = [c for c in cmd if c]
    
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print("Error: Failed to build executable")
        return False
    
    print("Executable built successfully!")
    return True

def create_installer():
    """Create Windows installer using NSIS"""
    print("="*60)
    print("Creating Windows Installer...")
    print("="*60)
    
    # Check if NSIS is installed
    nsis_path = Path("C:/Program Files (x86)/NSIS/makensis.exe")
    if not nsis_path.exists():
        nsis_path = Path("C:/Program Files/NSIS/makensis.exe")
    
    if not nsis_path.exists():
        print("Warning: NSIS not found. Installer script created but not compiled.")
        print("To create the installer:")
        print("1. Install NSIS from https://nsis.sourceforge.io")
        print("2. Run: makensis.exe network_ai_agent_installer.nsi")
        return True
    
    # Compile NSIS script
    result = subprocess.run([str(nsis_path), "network_ai_agent_installer.nsi"])
    
    if result.returncode != 0:
        print("Error: Failed to create installer")
        return False
    
    print("Installer created successfully!")
    return True

def main():
    """Main build function"""
    # Check dependencies
    try:
        import setuptools
    except ImportError:
        print("Installing setuptools...")
        subprocess.run([sys.executable, "-m", "pip", "install", "setuptools"], check=True)
    
    # Build executable
    if not build_executable():
        print("Failed to build executable")
        sys.exit(1)
    
    # Create installer
    if not create_installer():
        print("Warning: Failed to create installer, but executable is ready")
    
    print("\n" + "="*60)
    print("Build complete!")
    print("="*60)
    print("\nOutput:")
    print("  - Executable: dist/NetworkAIAgent.exe")
    print("  - Installer: Network-AI-Agent-Setup.exe")
    print("\nInstallation:")
    print("  1. Run Network-AI-Agent-Setup.exe")
    print("  2. Follow the installation wizard")
    print("  3. Configure .env file with your OpenAI API key")
    print("  4. Run the application")

if __name__ == "__main__":
    main()
