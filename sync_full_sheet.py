import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Sheets
with open("creds.json") as f:
    json_creds = json.load(f)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
client = gspread.authorize(creds)

# Connect to the Google Sheet by key
sheet = client.open_by_key("1gLarCMGluthM7cbp4hSCMrDfjMwJHS1PsB8DzmX0pjc")

# Define the tabs and headers to enforce
tabs_and_headers = {
    "Agenda": [
        "Date", "Start Time", "End Time", "Title", "Details", "Location / Link",
        "Category", "Status", "Reminder", "Recurring", "Confirmed?"
    ],
    "To-Do": ["Task", "Due Date", "Category", "Status", "Priority", "Notes"],
    "Travel": [
        "Trip Name", "Start Date", "End Date", "Location", "Flight/Hotel Info",
        "Confirmation #", "Notes"
    ],
    "Notes": ["Title", "Content", "Created Date", "Tags"],
    "Addresses": ["Name", "Street Address", "City", "State", "ZIP", "Notes"],
    "Automation Logs": ["Timestamp", "Action", "Status", "Details", "Source"],
    "Sync Log": ["Timestamp", "File", "Update Type", "Result", "Notes"]
}

# Iterate through and ensure all tabs exist with headers
for tab, headers in tabs_and_headers.items():
    try:
        worksheet = sheet.worksheet(tab)
        current_headers = worksheet.row_values(1)
        if current_headers != headers:
            worksheet.delete_rows(1)
            worksheet.insert_row(headers, 1)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab, rows="100", cols=str(len(headers)))
        worksheet.insert_row(headers, 1)

print("✅ Success: All tabs verified and headers updated.")
