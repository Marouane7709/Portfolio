# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/Marouane7709/cubesat-budget-analyzer.git
cd cubesat-budget-analyzer
```

2. Create and activate a virtual environment (recommended):

On Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

On Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the package:
```bash
pip install -e .
```

## Running the Application

After installation, you can run the application in two ways:

1. Using the command-line entry point:
```bash
cubesat-budget-analyzer
```

2. Running the module directly:
```bash
python -m cubesat_budget_analyzer
```

## Troubleshooting

If you encounter any issues:

1. Make sure you have all prerequisites installed
2. Try updating pip: `python -m pip install --upgrade pip`
3. If you get dependency errors, try installing dependencies manually:
   ```bash
   pip install -r requirements.txt
   ```
4. For PyQt6 issues on Linux, make sure you have the required system packages:
   ```bash
   sudo apt-get install python3-pyqt6  # For Ubuntu/Debian
   ``` 