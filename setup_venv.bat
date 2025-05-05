@echo off
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
set PIP_CONFIG_FILE=%~dp0pip_config.ini
echo Using pip config file: %PIP_CONFIG_FILE%
pip install -r requirements.txt

echo Installing Playwright browsers...
playwright install

echo Setup complete! Virtual environment is activated and packages are installed.
echo To deactivate the virtual environment, type 'deactivate'