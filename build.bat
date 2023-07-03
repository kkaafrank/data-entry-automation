py -m PyInstaller --noconfirm --log-level ERROR --onefile .\automation_gui.py -n claim_entry_automation
COPY dist\claim_entry_automation.exe claim_entry_automation.exe
