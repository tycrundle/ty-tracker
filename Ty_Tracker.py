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
    "Birthdays / Anniversaries": ["Name", "Date", "Type", "Notes"],
    "Contacts / Networking": ["Name", "Company", "Role", "Notes", "Follow-Up Date"],
    "AI Requests": ["Date", "Request", "Status", "Response Notes"],
    "Archive": ["Original Tab", "Date Archived", "Title", "Details", "Status"],
    "Logs": ["Timestamp", "Action", "Details"],
    "Meta": ["Key", "Value", "Last Updated"]
}

# 5. Create any missing tabs and initialize headers
for tab_name, headers in tabs.items():
    try:
        worksheet = sheet.worksheet(tab_name)
        if not worksheet.get_all_values():
            worksheet.append_row(headers)
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab_name, rows=100, cols=len(headers))
        worksheet.append_row(headers)

# 6. Optional: Append test row to Agenda tab to verify
agenda = sheet.worksheet("Agenda")
agenda.append_row([
    "2025-05-28",        # Date
    "12:00 PM",          # Start Time
    "12:30 PM",          # End Time
    "GitHub Action Test",# Title
    "Row added via GitHub workflow",  # Details
    "N/A",               # Location / Link
    "Automation",        # Category
    "Scheduled",         # Status
    "None",              # Reminder
    "No",                # Recurring
    "Confirmed"          # Confirmed?
])

print("✅ Success: All tabs synced and test row added.")
