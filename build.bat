py -m PyInstaller --noconfirm --log-level ERROR .\automation_gui.py -n claim_entry_automation
COPY .env.shared dist\claim_entry_automation\.env.shared
COPY .env dist\claim_entry_automation\.env
