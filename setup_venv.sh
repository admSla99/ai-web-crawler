#!/bin/bash

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export PIP_CONFIG_FILE="$SCRIPT_DIR/pip_config.ini"
echo "Using pip config file: $PIP_CONFIG_FILE"
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install

echo "Setup complete! Virtual environment is activated and packages are installed."
echo "To deactivate the virtual environment, type 'deactivate'"
