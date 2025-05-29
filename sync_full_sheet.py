import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# === AUTH SETUP ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# === OPEN SHEET ===
sheet = client.open("Ty's Tracker")

# === DESTINATION TAB FIELD MAP ===
destination_tabs = {
    "Agenda": ["Date", "Start Time", "End Time", "Title", "Details", "Location_Link", "Category", "Status", "Reminder", "Recurring", "Confirmed?"],
    "To-Do": ["Task", "Due Date", "Priority", "Category", "Status", "Notes"],
    "Travel": ["Trip", "Start Date", "End Date", "Details", "Location", "Status"],
    "Notes": ["Date", "Note", "Tags"],
    "Addresses": ["Name", "Street Address", "City_State_ZIP", "Notes"],
    "Shopping Wishlist": ["Item", "Category", "Priority", "Link", "Notes"],
    "Books Media": ["Title", "Type", "Status", "Notes"],
    "Finances": ["Date", "Category", "Description", "Amount", "Notes"],
    "Fitness Health": ["Date", "Activity", "Duration", "Notes"],
    "Work Projects": ["Project", "Task", "Due Date", "Status", "Notes"],
    "Birthdays Anniversaries": ["Name", "Date", "Type", "Gift Idea", "Notes"],
    "Contacts Networking": ["Name", "Company", "Role", "Contact Info", "Last Contacted", "Notes"],
    "AI Requests": ["Date", "Request", "Status", "Response Summary", "Follow-Up?"],
    "Archive": ["Original Tab", "Date Archived", "Title", "Details", "Status"],
    "Logs": ["Timestamp", "Action", "Details"],
    "Meta": ["Key", "Value", "Last Updated"],
    "Automation Logs": ["Date", "Script", "Outcome", "Details"],
    "Sync Log": ["Date", "Action", "Status", "Notes"],
    "GPT_Memory": ["Date", "Log"]
}

# === PROCESS PENDING UPLOADS ===
pending_ws = sheet.worksheet("Pending Uploads")
pending_data = pending_ws.get_all_records()

for i, row in enumerate(pending_data, start=2):  # skip header row
    if row['Status'].strip().lower() != "pending":
        continue

    tab_name = row['Original Tab'].strip()
    if tab_name not in destination_tabs:
        pending_ws.update_cell(i, 9, "Error: Unknown Tab")
        continue

    try:
        dest_ws = sheet.worksheet(tab_name)
        expected_fields = destination_tabs[tab_name]
        row_data = [row.get(f"Field{j+1}", "") for j in range(len(expected_fields))]
        dest_ws.append_row(row_data)
        pending_ws.update_cell(i, 9, "Synced")
    except Exception as e:
        pending_ws.update_cell(i, 9, f"Error: {str(e)}")

# === LOG SYNC ===
sync_log = sheet.worksheet("Sync Log")
sync_log.append_row([
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Sync Full",
    "Success",
    "Processed all pending uploads"
])
