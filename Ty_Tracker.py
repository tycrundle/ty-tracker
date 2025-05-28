import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# 1. Load JSON credentials from local file created by workflow
with open("creds.json") as f:
    json_creds = json.load(f)

# 2. Set the scope and authorize
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
client = gspread.authorize(creds)

# 3. Open the Google Sheet by key
sheet = client.open_by_key("1gLarCMGluthM7cbp4hSCMrDfjMwJHS1PsB8DzmX0pjc")

# 4. Define all required tabs and their headers
tabs = {
    "Agenda": ["Date", "Start Time", "End Time", "Title", "Details", "Location / Link", "Category", "Status", "Reminder", "Recurring", "Confirmed?"],
    "To-Do": ["Task", "Due Date", "Priority", "Category", "Status", "Notes"],
    "Travel": ["Trip", "Start Date", "End Date", "Details", "Location", "Status"],
    "Notes": ["Date", "Note", "Tags"],
    "Addresses": ["Name", "Street Address", "City/State/ZIP", "Notes"],
    "Shopping / Wishlist": ["Item", "Category", "Priority", "Link", "Notes"],
    "Books / Media": ["Title", "Type (Book/Show)", "Status", "Notes"],
    "Finances": ["Date", "Category", "Description", "Amount", "Notes"],
    "Fitness / Health": ["Date", "Activity", "Duration", "Notes"],
    "Work / Projects": ["Project", "Task", "Due Date", "Status", "Notes"],
    "Birthdays / Anniversaries": ["Name", "Date", "Type", "Gift Idea", "Notes"],
    "Contacts / Networking": ["Name", "Company", "Role", "Contact Info", "Last Contacted", "Notes"],
    "AI Requests": ["Date", "Request", "Status", "Response Summary", "Follow-Up?"],
    "Archive": ["Original Tab", "Date Archived", "Title", "Details", "Status"],
    "Logs": ["Timestamp", "Action", "Details"],
    "Meta": ["Key", "Value", "Last Updated"],
    "Automation Logs": ["Date", "Script", "Outcome", "Details"],
    "Sync Log": ["Date", "Action", "Status", "Notes"]
}

# 5. Create missing tabs and/or enforce headers
for tab_name, headers in tabs.items():
    try:
        worksheet = sheet.worksheet(tab_name)
        current_headers = worksheet.row_values(1)
        if current_headers != headers:
            worksheet.delete_row(1)
            worksheet.insert_row(headers, 1)
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab_name, rows=100, cols=len(headers))
        worksheet.insert_row(headers, 1)

# 6. Add test row to Sync Log
log = sheet.worksheet("Sync Log")
log.append_row([
    "2025-05-28", "Ty_Tracker.py header sync", "Success", "All tabs confirmed and headers enforced"
])

print("✅ Success: All tabs checked, headers updated, and sync logged.")
