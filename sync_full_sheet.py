import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from sheet_schema import tab_schemas

# Use GitHub Secret stored in the environment
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Connect to your sheet
SHEET_NAME = "Ty's Tracker"
sheet = client.open(SHEET_NAME)

# Open required tabs
pending_tab = sheet.worksheet("Pending Uploads")
log_tab = sheet.worksheet("Sync Log")
archive_tab = sheet.worksheet("Archive")

# Get all pending entries
pending_data = pending_tab.get_all_values()
headers = pending_data[0]
entries = pending_data[1:]

synced = []
archived = []
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for row in entries:
    if not any(row):  # skip blank rows
        continue

    date, target_tab, *fields = row
    schema = tab_schemas.get(target_tab)
    if schema and len(fields) >= len(schema):
        try:
            tab = sheet.worksheet(target_tab)
            tab.append_row(fields[:len(schema)], value_input_option="USER_ENTERED")
            archived.append([target_tab, now] + fields[:3] + ["Synced"])
            synced.append(row)
        except Exception as e:
            log_tab.append_row([now, "sync_full_sheet.py", "Error", str(e)])

# Rewrite Pending Uploads without synced rows
if synced:
    remaining = [headers] + [row for row in entries if row not in synced]
    pending_tab.clear()
    pending_tab.append_rows(remaining, value_input_option="USER_ENTERED")

# Archive entries
if archived:
    archive_tab.append_rows(archived, value_input_option="USER_ENTERED")

# Log result
log_tab.append_row([now, "sync_full_sheet.py", "Success", f"Processed {len(synced)} entries"])
