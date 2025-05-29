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

# === HEADER MAP ===
header_map = {
    "To-Do": ["Task", "Due Date", "Priority", "Category", "Status"],
    "Notes": ["Date", "Note", "Tags"],
    "Addresses": ["Name", "Street Address", "City/State/ZIP", "Notes"],
    "Birthdays  Anniversaries": ["Name", "Date", "Type", "Notes"],
    "Agenda": ["Date", "Title"],
    "Goals": ["Goal", "Start Date", "Target Date", "Progress", "Notes"],
    "Contacts  Networking": ["Name", "Company", "Role", "Notes", "Follow-Up Date"],
    "Books  Media": ["Title", "Type (Book/Show)", "Status", "Notes"],
    "Fitness  Health": ["Activity", "Duration", "Notes"],
    "Shopping  Wishlist": ["Item", "Category", "Priority", "Link", "Notes"],
    "Work  Projects": ["Project", "Task", "Due Date", "Status", "Notes"],
    "Travel": ["Trip", "Start Date", "End Date", "Details", "Location", "Status"],
    "Pets": ["Name", "Type", "Care Task", "Due Date", "Notes"],
    "Finances": ["Category", "Description", "Amount", "Notes"],
    "AI Requests": ["Request", "Status", "Response Notes"]
}

# === HELPER TO BUILD ROWS ===
def create_row(date, tab, fields):
    header_fields = header_map.get(tab, [])
    full_fields = [date, tab] + fields[:len(header_fields)] + [""] * (len(header_fields) - len(fields))
    return full_fields + ["", "Pending"]

# === LOAD MEMORY LOGS ===
memory_data = memory_ws.get_all_records()
new_rows = []

for i, row in enumerate(memory_data, start=2):
    log = row["Log"]
    date = row["Date"]
    if "[Processed]" in log:
        continue

    entry_handled = False

    # === AUTO-TAG PARSERS ===
    if "[TO-DO]" in log:
        fields = log.replace("[TO-DO]", "").strip().split(" | ")
        new_rows.append(create_row(date, "To-Do", fields))
        entry_handled = True

    elif "[NOTE]" in log:
        fields = log.replace("[NOTE]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Notes", fields))
        entry_handled = True

    elif "[ADDRESS]" in log:
        fields = log.replace("[ADDRESS]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Addresses", fields))
        entry_handled = True

    elif "[BIRTHDAY]" in log:
        fields = log.replace("[BIRTHDAY]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Birthdays  Anniversaries", fields))
        entry_handled = True

    elif "[REMINDER]" in log:
        fields = log.replace("[REMINDER]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Agenda", fields))
        entry_handled = True

    elif "[GOAL]" in log:
        fields = log.replace("[GOAL]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Goals", fields))
        entry_handled = True

    elif "[CONTACT]" in log:
        fields = log.replace("[CONTACT]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Contacts  Networking", fields))
        entry_handled = True

    elif "[MEDIA]" in log:
        fields = log.replace("[MEDIA]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Books  Media", fields))
        entry_handled = True

    elif "[FITNESS]" in log:
        fields = log.replace("[FITNESS]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Fitness  Health", fields))
        entry_handled = True

    elif "[SHOP]" in log:
        fields = log.replace("[SHOP]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Shopping  Wishlist", fields))
        entry_handled = True

    elif "[PROJECT]" in log:
        fields = log.replace("[PROJECT]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Work  Projects", fields))
        entry_handled = True

    elif "[TRAVEL]" in log:
        fields = log.replace("[TRAVEL]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Travel", fields))
        entry_handled = True

    elif "[PET]" in log:
        fields = log.replace("[PET]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Pets", fields))
        entry_handled = True

    elif "[FINANCE]" in log:
        fields = log.replace("[FINANCE]", "").strip().split(" | ")
        new_rows.append(create_row(date, "Finances", fields))
        entry_handled = True

    elif "[AI]" in log:
        fields = log.replace("[AI]", "").strip().split(" | ")
        new_rows.append(create_row(date, "AI Requests", fields))
        entry_handled = True

    if entry_handled:
        memory_ws.update_cell(i, 2, f"[Processed] {log}")

# === STAGE TO PENDING UPLOADS ===
for row in new_rows:
    pending_ws.append_row(row)

# === LOG RESULT ===
sync_log = sheet.worksheet("Sync Log")
sync_log.append_row([
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "prepare_pending_uploads.py",
    "Success",
    f"Staged {len(new_rows)} entries to Pending Uploads"
])
