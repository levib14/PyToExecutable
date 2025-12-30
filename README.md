# 🐍 PyToExecutable

**Convert any Python script into a standalone executable (.exe or .app) with full GUI support!**

Turn your Python code into distributable applications that run on Windows and macOS without requiring Python to be installed. Perfect for sharing tools, games, and GUI applications with anyone.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- 🚀 **One-Click Conversion** - Paste your code, get an executable
- 🎨 **Full GUI Support** - tkinter, PyQt5/6, PySide2/6, wxPython, pygame, and more
- 🖼️ **Image & Resource Bundling** - Include images, data files, and assets
- 🔍 **Auto-Dependency Detection** - Automatically finds and installs required packages
- 📦 **Single File Output** - Everything bundled into one portable executable
- 🎯 **Smart Console Detection** - Automatically detects if your app needs a console window
- 🌐 **Cross-Platform** - Works on Windows and macOS
- 💾 **No Python Required** - Generated executables run standalone

---

## 📋 Requirements

- Python 3.7 or higher
- PyInstaller (auto-installed if not present)

---

## 🚀 Quick Start

### Installation

1. Download `py_to_exe_packager.py`
2. Run it:
   ```bash
   python py_to_exe_packager.py
   ```

That's it! PyInstaller will be installed automatically if needed.

### Basic Usage

```bash
python py_to_exe_packager.py
```

Follow the prompts:
1. Enter your application name
2. Paste your Python code
3. Type `END` on a new line
4. Configure options (or use defaults)
5. Wait for the build to complete

**Your executable is ready!** 🎉

---

## 📖 Examples

### Example 1: Simple GUI Calculator

```python
import tkinter as tk

root = tk.Tk()
root.title("Calculator")
root.geometry("300x400")

display = tk.Entry(root, font=("Arial", 20), justify="right")
display.pack(fill="both", padx=10, pady=10)

# Add calculator buttons here...

root.mainloop()
END
```

**Settings:**
- Show console window? → `n` (it's a GUI app!)
- Auto-detect dependencies? → `y`

**Output:** `Calculator.exe` or `Calculator.app` - ready to distribute!

### Example 2: Image Viewer with PIL

```python
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Photo Viewer")

img = Image.open("photo.jpg")
photo = ImageTk.PhotoImage(img)

label = tk.Label(root, image=photo)
label.pack()

root.mainloop()
END
```

**Settings:**
- Files: `photo.jpg`
- The packager will auto-install Pillow!

### Example 3: PyQt5 Application

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("My PyQt App")
window.setGeometry(100, 100, 600, 400)

label = QLabel("Hello PyQt5!", window)
label.move(200, 150)

window.show()
sys.exit(app.exec_())
END
```

**The packager automatically:**
- Detects PyQt5
- Installs it if needed
- Adds hidden imports
- Suggests windowed mode

### Example 4: Pygame Game

```python
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((30, 30, 60))
    # Your game logic here...
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
END
```

---

## 🎯 Supported GUI Frameworks

| Framework | Status | Auto-Install |
|-----------|--------|--------------|
| tkinter | ✅ Built-in | N/A |
| PyQt5 | ✅ Full Support | Yes |
| PyQt6 | ✅ Full Support | Yes |
| PySide2 | ✅ Full Support | Yes |
| PySide6 | ✅ Full Support | Yes |
| wxPython | ✅ Full Support | Yes |
| pygame | ✅ Full Support | Yes |
| Kivy | ✅ Full Support | Yes |
| pyglet | ✅ Full Support | Yes |

---

## 🔧 Advanced Usage

### Programmatic API

```python
from py_to_exe_packager import PyToExecutable

packager = PyToExecutable()

code = """
import tkinter as tk
root = tk.Tk()
root.title("My App")
tk.Label(root, text="Hello World!").pack()
root.mainloop()
"""

packager.create_executable(
    code=code,
    app_name="MyApp",
    console=False,  # GUI app, no console
    icon_path="icon.ico",
    additional_files=[
        ("data.txt", "."),
        ("images/logo.png", "images"),
    ],
    auto_detect=True  # Auto-install dependencies
)
```

### Including Additional Files

**Format Options:**
- `file.txt` → Bundled at root
- `file.txt:folder` → Bundled in `folder/`
- `file.txt->folder` → Alternative syntax
- `images/` → Bundle entire folder

**Accessing Bundled Files in Your Code:**

```python
import sys
import os

# Get the correct base path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = sys._MEIPASS
else:
    # Running as script
    base_path = os.path.dirname(__file__)

# Load your file
file_path = os.path.join(base_path, 'data.txt')
with open(file_path, 'r') as f:
    data = f.read()
```

### Custom Icons

**Windows:** Use `.ico` files
**macOS:** Use `.icns` files

```bash
Icon file path: assets/myapp.ico
```

---

## 🛠️ Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| **Application Name** | Name of the executable | Required |
| **Console Window** | Show terminal window | Auto-detect |
| **Icon Path** | Custom icon file | None |
| **Output Directory** | Where to save executable | Current directory |
| **Additional Files** | Bundle resources | None |
| **Auto-detect** | Find dependencies automatically | Yes |
| **Hidden Imports** | Manual module includes | Auto-detected |
| **Packages** | Install before building | Auto-detected |

---

## 📦 Distribution

Your generated executable is **completely standalone**:

✅ No Python installation required  
✅ No dependencies to install  
✅ Single file to distribute  
✅ Works on any compatible OS  

Simply share the `.exe` (Windows) or `.app` (macOS) file!

---

## 🐛 Troubleshooting

### "Module not found" errors

The packager should auto-detect modules, but if you get errors:
1. Manually specify hidden imports
2. Install the package: `pip install package-name`
3. Add to packages list when prompted

### Executable won't run

- Check if antivirus is blocking it (common with PyInstaller)
- Verify all required files are bundled
- Test with console mode enabled to see errors

### Large file size

Executables include Python and all dependencies:
- Typical size: 10-50 MB
- Use virtual environments for smaller builds
- Consider using `--onedir` mode (not single file)

### File conflicts (like email.py)

Rename any files in your directory that match Python standard library names:
```bash
mv email.py my_email_script.py
```

---

## 🙏 Acknowledgments

- Built with [PyInstaller](https://www.pyinstaller.org/)
- Supports all major Python GUI frameworks
- Inspired by the need to easily share Python applications

---
