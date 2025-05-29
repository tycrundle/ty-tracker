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

def create_row(date, tab, fields):
    header_fields = header_map.get(tab, [])
    full_fields = [date, tab] + fields[:len(header_fields)] + [""] * (len(header_fields) - len(fields))
    return full_fields + ["", "Pending"]

# === PROCESS MEMORY ===
memory_data = memory_ws.get_all_records()
new_rows = []
update_requests = []

for i, row in enumerate(memory_data, start=2):
    log = row["Log"]
    date = row["Date"]
    if "[Processed]" in log:
        continue

    handled = False

    def process(tag, tab_name):
        nonlocal handled
        if tag in log:
            fields = log.replace(tag, "").strip().split(" | ")
            new_rows.append(create_row(date, tab_name, fields))
            update_requests.append({
                'range': f"B{i}",
                'values': [[f"[Processed] {log}"]]
            })
            handled = True

    process("[TO-DO]", "To-Do")
    process("[NOTE]", "Notes")
    process("[ADDRESS]", "Addresses")
    process("[BIRTHDAY]", "Birthdays  Anniversaries")
    process("[REMINDER]", "Agenda")
    process("[GOAL]", "Goals")
    process("[CONTACT]", "Contacts  Networking")
    process("[MEDIA]", "Books  Media")
    process("[FITNESS]", "Fitness  Health")
    process("[SHOP]", "Shopping  Wishlist")
    process("[PROJECT]", "Work  Projects")
    process("[TRAVEL]", "Travel")
    process("[PET]", "Pets")
    process("[FINANCE]", "Finances")
    process("[AI]", "AI Requests")

# === APPEND TO PENDING ===
for row in new_rows:
    pending_ws.append_row(row)

# === BATCH UPDATE MEMORY ===
if update_requests:
    memory_ws.batch_update([{'range': u['range'], 'values': u['values']} for u in update_requests])

# === LOG ===
sheet.worksheet("Sync Log").append_row([
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "prepare_pending_uploads.py",
    "Success",
    f"Staged {len(new_rows)} entries to Pending Uploads"
])
