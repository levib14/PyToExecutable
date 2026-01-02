# test - Build Instructions

This package contains everything you need to build your Python application into a standalone executable.

## Contents
- test.py - Your Python script
- build_windows.bat - Windows build script
- build_mac.sh - macOS build script
- README.md - This file

## Requirements

### Third-Party Dependencies
This application requires the following Python packages:
- smtplib
- geocoder

The build scripts will automatically install these for you.


## Building on Windows
1. Double-click build_windows.bat
2. Wait for the build to complete
3. Find your executable in the dist folder

## Building on macOS
1. Open Terminal in this folder
2. Run: chmod +x build_mac.sh
3. Run: ./build_mac.sh
4. Find your application in the dist folder

## Manual Build (Advanced)
If you prefer to build manually:

```bash
# Install PyInstaller
pip install pyinstaller

# Install dependencies
pip install smtplib
pip install geocoder

# Build
pyinstaller --onefile --noconsole --name=test test.py
```

## Troubleshooting
- Make sure Python is installed and in your PATH
- Some antivirus software may flag PyInstaller executables as false positives
- Large dependencies may take several minutes to bundle
- If a dependency fails to install, try installing it manually first

## Notes
- Windows executables (.exe) must be built on Windows
- macOS applications (.app) must be built on macOS
- The executable will include all dependencies and can run without Python installed
- The first build may take longer as PyInstaller analyzes dependencies
