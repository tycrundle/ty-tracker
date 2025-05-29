import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

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

    # Example format: [TO-DO] Finish website build | 2025-05-31 | High | Work | Not Started
    if "[TO-DO]" in log:
        parts = log.replace("[TO-DO]", "").strip().split(" | ")
        new_rows.append([
            row["Date"], "To-Do",
            parts[0] if len(parts) > 0 else "",
            parts[1] if len(parts) > 1 else "",
            parts[2] if len(parts) > 2 else "",
            parts[3] if len(parts) > 3 else "",
            parts[4] if len(parts) > 4 else "",
            "", "Pending"
        ])
        memory_ws.update_cell(i, 2, f"[Processed] {log}")

    elif "[NOTE]" in log:
        parts = log.replace("[NOTE]", "").strip().split(" | ")
        new_rows.append([
            row["Date"], "Notes",
            row["Date"],
            parts[0] if len(parts) > 0 else "",
            parts[1] if len(parts) > 1 else "",
            "", "", "", "Pending"
        ])
        memory_ws.update_cell(i, 2, f"[Processed] {log}")

# === ADD TO PENDING UPLOADS ===
for row in new_rows:
    pending_ws.append_row(row)

# === LOG ===
sync_log = sheet.worksheet("Sync Log")
sync_log.append_row([
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "prepare_pending_uploads.py",
    "Success",
    f"Staged {len(new_rows)} entries to Pending Uploads"
])
