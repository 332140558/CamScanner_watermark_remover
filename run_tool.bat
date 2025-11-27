@echo off
cd /d "%~dp0"
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate
    echo Installing dependencies...
    pip install -r pdf_watermark_remover\requirements.txt
) else (
    call .venv\Scripts\activate
)

echo Starting PDF Watermark Remover...
python pdf_watermark_remover\main.py
pause
