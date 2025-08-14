# Installation

## Prerequisites

* Python 3.10+ ([Download here](https://www.python.org/downloads/))
* `pip` package manager

## Dependencies

Install required Python packages:
`pip install numpy sounddevice`

# Run From Python

1. Clone or download this repository.
2. Open a terminal/PowerShell in the project folder.
3. Run the app with Python:
`python bass_trainer.py`

# Packaging as a Windows Executable (.exe)

## Install PyInstaller
`pip install pyinstaller`

### PyInstaller not be addeed to PATH
* Windows PowerShell doesn’t always include the folder where pip installs scripts in the PATH.
* Even though pyinstaller is installed, PowerShell may not be able to find it.

Find where PyInstaller is installed
`python -m site --user-base`

It will output something like:
`C:\Users\<username>\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages`

Add that folder to your PATH temporarily
* Replace <username> with your Windows username.
`$env:Path += ";C:\Users\<username>\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python\Scripts"`

## Build the Executable
`pyinstaller --onefile --windowed --icon=bass_trainer_icon.ico bass_trainer.py`

## If Python was installed from the Microsoft Store
* The user Scripts folder isn’t exactly where PowerShell expects.

If PowerShell still can’t find pyinstaller.exe, here is a way to run PyInstaller without messing with PATH:

Run PyInstaller via Python module instead of calling pyinstaller directly:
`python -m PyInstaller --onefile --windowed --icon=bass_trainer_icon.ico bass_trainer.py`