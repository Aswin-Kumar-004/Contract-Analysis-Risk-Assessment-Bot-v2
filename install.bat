@echo off
REM Contract Risk Bot - Installation Script for Windows

echo Installing Contract Risk Bot...
echo.

REM Check Python
python --version
echo.

REM Install requirements
echo Installing Python dependencies...
pip install -r requirements.txt

REM Download spaCy model
echo.
echo Downloading spaCy English model...
python -m spacy download en_core_web_sm

REM Check API key
echo.
if "%ANTHROPIC_API_KEY%"=="" (
    echo WARNING: ANTHROPIC_API_KEY not set!
    echo.
    echo To use AI features, set your API key:
    echo   set ANTHROPIC_API_KEY=your_key_here
    echo.
    echo Get your API key from: https://console.anthropic.com/
    echo.
) else (
    echo ANTHROPIC_API_KEY is configured
)

echo.
echo Installation complete!
echo.
echo To run the app:
echo   streamlit run app.py
echo.
pause
