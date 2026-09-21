#!/usr/bin/env python3
"""Export the generated HTML resume to a PDF with clickable links using Chromium."""
import shutil
import subprocess
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
browser = next((shutil.which(name) for name in ('google-chrome', 'chromium', 'chromium-browser') if shutil.which(name)), None)
if not browser:
    raise SystemExit('Install Chrome/Chromium, or print resume.html to PDF from your browser (A4, no headers/footers).')
out = ROOT / 'assets/documents/Mahmud-Un-Naby-Resume.pdf'
out.parent.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='portfolio-resume-') as profile:
    subprocess.run([browser, '--headless', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--no-pdf-header-footer', '--run-all-compositor-stages-before-draw', '--virtual-time-budget=2000', f'--user-data-dir={profile}', f'--print-to-pdf={out}', (ROOT / 'resume.html').as_uri()], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
print(f'Created {out}')
