import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from sheet_schema import tab_schemas

# === AUTH ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# === OPEN SHEET ===
sheet = client.open("Ty's Tracker")
pending_ws = sheet.worksheet("Pending Uploads")
pending_data = pending_ws.get_all_records()

# === PROCESS PENDING UPLOADS ===
for i, row in enumerate(pending_data, start=2):
    if row['Status'].strip().lower() != "pending":
        continue

    tab = row['Original Tab'].strip()
    if tab not in tab_schemas:
        pending_ws.update_cell(i, 9, "Error: Unknown Tab")
        continue

    try:
        ws = sheet.worksheet(tab)
        headers = tab_schemas[tab]
        row_data = [row.get(f"Field{j+1}", "") for j in range(len(headers))]
        ws.append_row(row_data)
        pending_ws.update_cell(i, 9, "Synced")
    except Exception as e:
        pending_ws.update_cell(i, 9, f"Error: {str(e)}")

# === LOG SYNC ===
sheet.worksheet("Sync Log").append_row([
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "sync_full_sheet.py",
    "Success",
    "Processed all pending uploads"
])
