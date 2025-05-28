import gspread
import json
import os
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

# 3. Open the Google Sheet by URL
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1gLarCMGluthM7cbp4hSCMrDfjwJHS1Ps8BDzmX0pjc/edit")
agenda = sheet.worksheet("Agenda")

# 4. Append a test row
agenda.append_row([
    "2025-05-28",           # Date
    "12:00 PM",             # Start Time
    "12:30 PM",             # End Time
    "GitHub Action Test",   # Title
    "Row added via GitHub workflow",  # Details
    "N/A",                  # Location / Link
    "Automation",           # Category
    "Scheduled",            # Status
    "None",                 # Reminder
    "No",                   # Recurring
    "Confirmed"             # Confirmed?
])

print("✅ Success: Row appended to Google Sheet.")
