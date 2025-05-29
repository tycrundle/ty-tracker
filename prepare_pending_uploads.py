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

category_config = {
    "[TO-DO]": ("To-Do", 6),
    "[NOTE]": ("Notes", 3),
    "[ADDRESS]": ("Addresses", 4),
    "[BIRTHDAY]": ("Birthdays  Anniversaries", 4),
    "[REMINDER]": ("Agenda", 6),
    "[FINANCE]": ("Finances", 5),
    "[BOOK]": ("Books  Media", 4),
    "[SHOPPING]": ("Shopping  Wishlist", 5),
    "[FITNESS]": ("Fitness  Health", 4),
    "[PROJECT]": ("Work  Projects", 5),
    "[CONTACT]": ("Contacts  Networking", 5),
    "[TRAVEL]": ("Travel", 6),
    "[PET]": ("Pets", 5),
    "[GOAL]": ("Goals", 5),
    "[AI]": ("AI Requests", 4),
    "[ARCHIVE]": ("Archive", 5),
    "[LOG]": ("Logs", 3),
    "[META]": ("Meta", 3),
    "[AUTOMATION]": ("Automation Logs", 4),
    "[SYNC]": ("Sync Log", 4)
}

for i, row in enumerate(memory_data, start=2):
    log = row["Log"]
    if "[Processed]" in log:
        continue

    for tag, (tab, field_count) in category_config.items():
        if tag in log:
            parts = log.replace(tag, "").strip().split(" | ")
            row_data = [row["Date"], tab] + parts + [""] * (field_count - len(parts)) + ["Pending"]
            new_rows.append(row_data)
            memory_ws.update_cell(i, 2, f"[Processed] {log}")
            break

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
