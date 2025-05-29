import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from sheet_schema import tab_schemas, category_tag_map, get_field_count

# === AUTH ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# === OPEN SHEET ===
sheet = client.open("Ty's Tracker")
memory_ws = sheet.worksheet("GPT_Memory")
pending_ws = sheet.worksheet("Pending Uploads")

# === LOAD MEMORY LOGS ===
memory_data = memory_ws.get_all_records()
new_rows = []

for i, row in enumerate(memory_data, start=2):
    log = row["Log"]
    if "[Processed]" in log:
        continue

    for tag, tab in category_tag_map.items():
        if tag in log:
            parts = log.replace(tag, "").strip().split(" | ")
            total_fields = get_field_count(tab)
            padded = parts + [""] * (total_fields - len(parts))
            new_rows.append([row["Date"], tab] + padded[:6] + ["Pending"])
            memory_ws.update_cell(i, 2, f"[Processed] {log}")
            break

# === ADD TO PENDING UPLOADS ===
for row in new_rows:
    pending_ws.append_row(row)

# === LOG ===
sheet.worksheet("Sync Log").append_row([
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "prepare_pending_uploads.py",
    "Success",
    f"Staged {len(new_rows)} entries to Pending Uploads"
])
