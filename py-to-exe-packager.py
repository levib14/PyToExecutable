"""
Python Code to Executable Packager
Converts Python code into standalone Windows (.exe) or macOS (.app) applications
with full support for GUI frameworks, images, and all Python modules
py-to-exe-packager.py
created by Levi Brant, Thebrantbrothers@gmail.com
12/30/2025
"""

import os
import sys
import subprocess
import tempfile
import shutil
import re
from pathlib import Path

class PyToExecutable:
    def __init__(self):
        self.check_dependencies()
        self.gui_frameworks = {
            'tkinter': [],
            'PyQt5': ['PyQt5'],
            'PyQt6': ['PyQt6'],
            'PySide2': ['PySide2'],
            'PySide6': ['PySide6'],
            'wx': ['wxPython'],
            'pygame': ['pygame'],
            'pyglet': ['pyglet'],
            'kivy': ['kivy'],
        }
    
    def check_dependencies(self):
        """Check if PyInstaller is installed"""
        try:
            import PyInstaller
        except ImportError:
            print("PyInstaller not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully!")
    
    def detect_imports(self, code: str) -> set:
        """Detect all imports in the code"""
        imports = set()
        
        # Pattern for: import module or from module import ...
        import_patterns = [
            r'^\s*import\s+([\w\.]+)',
            r'^\s*from\s+([\w\.]+)\s+import',
        ]
        
        for line in code.split('\n'):
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    module = match.group(1).split('.')[0]
                    imports.add(module)
        
        return imports
    
    def get_gui_packages(self, imports: set) -> list:
        """Determine which GUI packages need to be installed"""
        packages = []
        for framework, install_names in self.gui_frameworks.items():
            if framework in imports:
                packages.extend(install_names)
        return packages
    
    def get_hidden_imports_for_framework(self, imports: set) -> list:
        """Get framework-specific hidden imports"""
        hidden = []
        
        # Tkinter hidden imports
        if 'tkinter' in imports or 'Tkinter' in imports:
            hidden.extend([
                'tkinter',
                'tkinter.ttk',
                'tkinter.messagebox',
                'tkinter.filedialog',
                'tkinter.font',
                '_tkinter',
            ])
        
        # PyQt/PySide hidden imports
        qt_frameworks = ['PyQt5', 'PyQt6', 'PySide2', 'PySide6']
        for framework in qt_frameworks:
            if framework in imports:
                hidden.extend([
                    f'{framework}.QtCore',
                    f'{framework}.QtGui',
                    f'{framework}.QtWidgets',
                    f'{framework}.QtSvg',
                ])
        
        # PIL/Pillow hidden imports
        if 'PIL' in imports or 'Image' in imports:
            hidden.extend([
                'PIL',
                'PIL.Image',
                'PIL.ImageTk',
                'PIL.ImageDraw',
                'PIL.ImageFont',
            ])
        
        # Pygame hidden imports
        if 'pygame' in imports:
            hidden.extend(['pygame', 'pygame.mixer', 'pygame.font'])
        
        # Matplotlib hidden imports
        if 'matplotlib' in imports:
            hidden.extend([
                'matplotlib',
                'matplotlib.backends.backend_tkagg',
                'matplotlib.backends.backend_qt5agg',
            ])
        
        return hidden
    
    def create_executable(self, code: str, app_name: str, output_dir: str = ".", 
                         icon_path: str = None, console: bool = True,
                         additional_files: list = None, hidden_imports: list = None,
                         packages: list = None, auto_detect: bool = True):
        """
        Convert Python code to executable
        
        Args:
            code: Python code as string
            app_name: Name for the application
            output_dir: Directory to save the executable
            icon_path: Optional path to .ico (Windows) or .icns (macOS) file
            console: Whether to show console window (False for GUI apps)
            additional_files: List of tuples (source_path, dest_folder) for bundling files
            hidden_imports: List of module names to explicitly include
            packages: List of packages to install before building
            auto_detect: Automatically detect imports and install dependencies
        """
        # Auto-detect imports if enabled
        detected_imports = set()
        if auto_detect:
            print("🔍 Analyzing code for dependencies...")
            detected_imports = self.detect_imports(code)
            print(f"   Detected imports: {', '.join(sorted(detected_imports)) if detected_imports else 'None'}")
        
        # Determine packages to install
        all_packages = list(packages) if packages else []
        
        if auto_detect and detected_imports:
            gui_packages = self.get_gui_packages(detected_imports)
            
            # Add common packages if detected
            if 'PIL' in detected_imports or 'Image' in detected_imports:
                if 'pillow' not in [p.lower() for p in all_packages]:
                    all_packages.append('pillow')
            
            if 'numpy' in detected_imports:
                if 'numpy' not in all_packages:
                    all_packages.append('numpy')
            
            if 'requests' in detected_imports:
                if 'requests' not in all_packages:
                    all_packages.append('requests')
            
            # Add GUI framework packages
            all_packages.extend(gui_packages)
        
        # Remove duplicates
        all_packages = list(set(all_packages))
        
        # Install required packages
        if all_packages:
            print(f"\n📦 Installing required packages: {', '.join(all_packages)}")
            for package in all_packages:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    print(f"   ✓ {package}")
                except Exception as e:
                    print(f"   ⚠ {package} - may already be installed or failed")
        
        # Determine all hidden imports
        all_hidden_imports = list(hidden_imports) if hidden_imports else []
        
        if auto_detect and detected_imports:
            framework_imports = self.get_hidden_imports_for_framework(detected_imports)
            all_hidden_imports.extend(framework_imports)
            
            # Add the detected imports themselves
            all_hidden_imports.extend(detected_imports)
        
        # Remove duplicates
        all_hidden_imports = list(set(all_hidden_imports))
        
        # Create temporary directory for build
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write code to temporary Python file
            script_path = Path(temp_dir) / f"{app_name}.py"
            with open(script_path, 'w') as f:
                f.write(code)
            
            # Build PyInstaller command
            cmd = [
                sys.executable,
                "-m", "PyInstaller",
                "--onefile",
                "--name", app_name,
                "--distpath", output_dir,
                "--workpath", os.path.join(temp_dir, "build"),
                "--specpath", temp_dir,
                "--clean",  # Clean cache
            ]
            
            # Add icon if provided
            if icon_path and os.path.exists(icon_path):
                cmd.extend(["--icon", icon_path])
            
            # GUI mode (no console)
            if not console:
                cmd.append("--windowed")
                cmd.append("--noconsole")
            
            # Add hidden imports
            if all_hidden_imports:
                print(f"\n🔧 Including hidden imports ({len(all_hidden_imports)} modules)")
                for module in all_hidden_imports:
                    cmd.extend(["--hidden-import", module])
            
            # Add additional files/folders
            if additional_files:
                print(f"\n📁 Bundling additional files ({len(additional_files)} items)")
                for source, dest in additional_files:
                    if os.path.exists(source):
                        separator = ";" if sys.platform == "win32" else ":"
                        cmd.extend(["--add-data", f"{source}{separator}{dest}"])
                        print(f"   ✓ {source} -> {dest}")
                    else:
                        print(f"   ⚠ File not found: {source}")
            
            # Collect all binary dependencies
            cmd.append("--collect-all")
            cmd.append("PIL")  # Always collect PIL if present
            
            cmd.append(str(script_path))
            
            print(f"\n🔨 Building executable: {app_name}")
            print("   This may take 1-3 minutes...\n")
            
            # Run PyInstaller
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    ext = "app" if sys.platform == "darwin" else "exe"
                    exe_path = os.path.join(output_dir, f"{app_name}.{ext}" if ext == "exe" else app_name)
                    
                    print("=" * 60)
                    print("✓ SUCCESS! Executable created successfully!")
                    print("=" * 60)
                    print(f"📍 Location: {exe_path}")
                    
                    # Show file size
                    if os.path.exists(exe_path):
                        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                        print(f"📊 Size: {size_mb:.2f} MB")
                    
                    # Show how to access bundled files
                    if additional_files:
                        print("\n📝 Access bundled files in your code:")
                        print("   import sys, os")
                        print("   if getattr(sys, 'frozen', False):")
                        print("       base_path = sys._MEIPASS")
                        print("   else:")
                        print("       base_path = os.path.dirname(__file__)")
                        print("   file_path = os.path.join(base_path, 'your_file.txt')")
                    
                    return True
                else:
                    print("=" * 60)
                    print("✗ BUILD FAILED")
                    print("=" * 60)
                    print(result.stderr)
                    
                    # Try to provide helpful error messages
                    if "ModuleNotFoundError" in result.stderr:
                        print("\n💡 Tip: Try installing missing modules or add them to hidden imports")
                    
                    return False
            except Exception as e:
                print(f"✗ Error during build: {e}")
                return False

def parse_file_list(file_input: str) -> list:
    """Parse comma-separated list of files with optional destinations"""
    if not file_input.strip():
        return []
    
    files = []
    for item in file_input.split(','):
        item = item.strip()
        if not item:
            continue
        
        if ':' in item:
            source, dest = item.split(':', 1)
            files.append((source.strip(), dest.strip()))
        elif '->' in item:
            source, dest = item.split('->', 1)
            files.append((source.strip(), dest.strip()))
        else:
            files.append((item, '.'))
    
    return files

def main():
    packager = PyToExecutable()
    
    print("=" * 60)
    print("🐍 Python Code to Executable Packager")
    print("   Full support for GUI, images, and all modules")
    print("=" * 60)
    print()
    
    # Get application name
    app_name = input("Enter application name: ").strip()
    if not app_name:
        app_name = "MyApp"
    
    # Get Python code
    print("\nEnter your Python code (type 'END' on a new line when finished):")
    print("Tip: Use tkinter, PyQt, PIL, pygame, or any Python library!\n")
    code_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        code_lines.append(line)
    
    code = "\n".join(code_lines)
    
    if not code.strip():
        print("No code provided. Exiting.")
        return
    
    # Get optional settings
    print("\n--- Basic Settings ---")
    
    # Detect if it's likely a GUI app
    is_gui = any(x in code.lower() for x in ['tkinter', 'pyqt', 'pyside', 'wx.', 'pygame'])
    default_console = 'n' if is_gui else 'y'
    
    console_input = input(f"Show console window? (y/n, default={'n' if is_gui else 'y'}): ").strip().lower()
    console = console_input != 'n' if not is_gui else console_input == 'y'
    
    icon_path = input("Icon file path (.ico/.icns, leave blank for none): ").strip()
    output_dir = input("Output directory (leave blank for current): ").strip() or "."
    
    # Additional files
    print("\n--- Additional Resources (Optional) ---")
    print("Include images, data files, or folders?")
    print("Format: logo.png, data.txt:data, images_folder->assets")
    files_input = input("Files (comma-separated, leave blank for none): ").strip()
    additional_files = parse_file_list(files_input)
    
    # Manual overrides
    print("\n--- Advanced Options (Optional) ---")
    auto_detect_input = input("Auto-detect dependencies? (y/n, default=y): ").strip().lower()
    auto_detect = auto_detect_input != 'n'
    
    if not auto_detect:
        imports_input = input("Hidden imports (comma-separated): ").strip()
        hidden_imports = [m.strip() for m in imports_input.split(',') if m.strip()] if imports_input else None
        
        packages_input = input("Packages to install (comma-separated): ").strip()
        packages = [p.strip() for p in packages_input.split(',') if p.strip()] if packages_input else None
    else:
        hidden_imports = None
        packages = None
        print("✓ Will auto-detect and install dependencies")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Build executable
    print("\n" + "=" * 60)
    packager.create_executable(
        code=code,
        app_name=app_name,
        output_dir=output_dir,
        icon_path=icon_path if icon_path else None,
        console=console,
        additional_files=additional_files,
        hidden_imports=hidden_imports,
        packages=packages,
        auto_detect=auto_detect
    )
    print("=" * 60)

if __name__ == "__main__":
    main()
