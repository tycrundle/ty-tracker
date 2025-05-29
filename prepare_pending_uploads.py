import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the required scopes
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from GitHub Secret passed as an environment variable
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Authorize gspread with the credentials
client = gspread.authorize(creds)

import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from sheet_schema import tab_schemas, category_tag_map, get_field_count

# === AUTH ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# === SHEET ===
sheet = client.open("Ty's Tracker")
memory_ws = sheet.worksheet("GPT_Memory")
pending_ws = sheet.worksheet("Pending Uploads")
sync_log = sheet.worksheet("Sync Log")

memory_data = memory_ws.get_all_records()
new_rows = []

for i, row in enumerate(memory_data, start=2):
    log = row["Log"]
    if "[Processed]" in log:
        continue

    matched = False
    for tag, tab in category_tag_map.items():
        if tag in log:
            parts = log.replace(tag, "").strip().split(" | ")
            if not parts or parts[0].strip() == "":
                continue  # skip empty logs

            total_fields = get_field_count(tab)
            padded = parts + [""] * max(0, 6 - len(parts))
            row_fields = padded[:6]
            while len(row_fields) < 6:
                row_fields.append("")
            new_rows.append([row["Date"], tab] + row_fields + ["Pending"])
            memory_ws.update_cell(i, 2, f"[Processed] {log}")
            matched = True
            break

    if not matched:
        sync_log.append_row([datetime.now().isoformat(), "prepare_pending_uploads.py", "Skipped", f"Unrecognized tag: {log}"])

# === Add to Pending Uploads ===
for row in new_rows:
    try:
        pending_ws.append_row(row)
    except Exception as e:
        sync_log.append_row([datetime.now().isoformat(), "prepare_pending_uploads.py", "Error", str(e)])

sync_log.append_row([
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "prepare_pending_uploads.py",
    "Success",
    f"Staged {len(new_rows)} entries to Pending Uploads"
])
