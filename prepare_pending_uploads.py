import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from sheet_schema import tab_schemas, category_tag_map

# Secure credential handling from GitHub Secrets
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Sheet setup
SHEET_NAME = "Ty's Tracker"
sheet = client.open(SHEET_NAME)

# Read from GPT_Memory
memory_tab = sheet.worksheet("GPT_Memory")
memory_data = memory_tab.get_all_values()
headers = memory_data[0]
entries = memory_data[1:]

# Prepare staged data
pending_tab = sheet.worksheet("Pending Uploads")
now = datetime.now().strftime("%Y-%m-%d")

updated_memory = [headers]
staged_entries = []

for row in entries:
    if not any(row):  # skip empty
        continue

    date, log = row
    if log.startswith("[Processed]"):
        updated_memory.append(row)
        continue

    for tag, tab in category_tag_map.items():
        if log.startswith(tag):
            schema = tab_schemas.get(tab)
            if schema:
                stripped = log.replace(tag, "").strip()
                parts = [p.strip() for p in stripped.split("|")]
                row_data = [date] + parts
                while len(row_data) < len(schema):
                    row_data.append("")
                staged_entries.append([now, tab] + row_data[:len(schema)])
                row[1] = f"[Processed] {log}"
            break

    updated_memory.append(row)

# Write to Pending Uploads
if staged_entries:
    existing = pending_tab.get_all_values()
    if not existing:
        headers = ["Date", "Target Tab"] + list(tab_schemas.values())[0]
        pending_tab.append_row(headers, value_input_option="USER_ENTERED")

    pending_tab.append_rows(staged_entries, value_input_option="USER_ENTERED")

# Update GPT_Memory with processed marks
memory_tab.clear()
memory_tab.append_row(headers)
if updated_memory[1:]:
    memory_tab.append_rows(updated_memory[1:], value_input_option="USER_ENTERED")

# Write to Sync Log
log_tab = sheet.worksheet("Sync Log")
log_tab.append_row([
    now,
    "prepare_pending_uploads.py",
    "Success",
    f"Staged {len(staged_entries)} entries to Pending Uploads"
])
