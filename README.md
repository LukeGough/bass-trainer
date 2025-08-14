# Bass Trainer

A simple Python app to help you learn bass notes and note order through interactive quizzes.

---

## Installation

### Prerequisites

- Python 3.10+ ([Download here](https://www.python.org/downloads/))
- `pip` package manager

---

### Clone the Repository

```bash
git clone https://github.com/username/bass-trainer.git
cd bass-trainer
```

Or download as a ZIP and extract.

---

### Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

> Alternatively, install individually:

```bash
pip install numpy sounddevice
```

---

## Running from Python

Open a terminal or PowerShell in the project folder and run:

```bash
python bass_trainer.py
```

- You can select either **Bass Note Quiz** or **Note Order Quiz**.
- Note style can be **sharp**, **flat**, or **both** (both sharps and flats accepted).

---

## Packaging as a Windows Executable (.exe)

### Install PyInstaller

```bash
pip install pyinstaller
```

> ⚠ Note: On Windows, PowerShell may not automatically recognize `pyinstaller` if Python is installed via Microsoft Store.

---

### Run PyInstaller via Python module (recommended)

```bash
python -m PyInstaller --onefile --windowed --icon=bass_trainer_icon.ico bass_trainer.py
```

This will generate a `dist/bass_trainer.exe` file.

---

### Optional: Temporary PATH fix

If PyInstaller is installed but not found:

1. Find your user-base path:

```powershell
python -m site --user-base
```

2. Add the Scripts folder to your PATH:

```powershell
$env:Path += ";C:\Users\<username>\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python\Scripts"
```

3. Then run PyInstaller as usual.

---
