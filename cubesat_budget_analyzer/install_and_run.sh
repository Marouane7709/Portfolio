#!/bin/bash

echo "Installing CubeSat Budget Analyzer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed! Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install the package
pip install -e .

# Run the application
echo "Starting CubeSat Budget Analyzer..."
cubesat-budget-analyzer

# Deactivate virtual environment when done
deactivate 