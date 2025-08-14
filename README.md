# Bass Trainer

A simple Python-based bass note training application with two quiz modes:  
- **Bass Note Quiz** — identify notes on the bass fretboard  
- **Note Order Quiz** — guess the next or previous note in the chromatic scale  

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

## Run From Python
1. Clone or download this repository.
2. Open a terminal/PowerShell in the project folder.
3. Run the app:
```bash
python bass_trainer.py
```

---

## Packaging as a Windows Executable (.exe)

### Install PyInstaller

```bash
pip install pyinstaller
```

> ⚠ Note: On Windows, PowerShell may not automatically recognize `pyinstaller` if Python is installed via Microsoft Store.

---

### Build the Executable
PyInstaller will generate a `dist/bass_trainer.exe` file.
```bash
python -m PyInstaller --onefile --windowed --icon=bass_trainer_icon.ico bass_trainer.py

```
