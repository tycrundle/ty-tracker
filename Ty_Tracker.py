import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the required scopes
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from GitHub Secret passed as an environment variable
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Authorize gspread with the credentials
client = gspread.authorize(creds)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === AUTH SETUP ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# === OPEN SHEET ===
sheet = client.open("Ty's Tracker")

# === ALL HEADERS DEFINED ===
expected_headers = {
    "Agenda": ['Date', 'Start Time', 'End Time', 'Title', 'Details', 'Location_Link', 'Category', 'Status', 'Reminder', 'Recurring', 'Confirmed?'],
    "GPT_Memory": ['Date', 'Log'],
    "Addresses": ['Name', 'Street Address', 'City_State_ZIP', 'Notes'],
    "Pending Uploads": ['Date', 'Original Tab', 'Field1', 'Field2', 'Field3', 'Field4', 'Field5', 'Field6', 'Status'],
    "Shopping Wishlist": ['Item', 'Category', 'Priority', 'Link', 'Notes'],
    "Books Media": ['Title', 'Type', 'Status', 'Notes'],
    "Finances": ['Date', 'Category', 'Description', 'Amount', 'Notes'],
    "Fitness Health": ['Date', 'Activity', 'Duration', 'Notes'],
    "Work Projects": ['Project', 'Task', 'Due Date', 'Status', 'Notes'],
    "Birthdays Anniversaries": ['Name', 'Date', 'Type', 'Gift Idea', 'Notes'],
    "Contacts Networking": ['Name', 'Company', 'Role', 'Contact Info', 'Last Contacted', 'Notes'],
    "AI Requests": ['Date', 'Request', 'Status', 'Response Summary', 'Follow-Up?'],
    "Archive": ['Original Tab', 'Date Archived', 'Title', 'Details', 'Status'],
    "Logs": ['Timestamp', 'Action', 'Details'],
    "Meta": ['Key', 'Value', 'Last Updated'],
    "Goals": ['Goal', 'Start Date', 'Target Date', 'Progress', 'Notes'],
    "Notes": ['Date', 'Note', 'Tags'],
    "Pets": ['Name', 'Type', 'Care Task', 'Due Date', 'Notes'],
    "Travel": ['Trip', 'Start Date', 'End Date', 'Details', 'Location', 'Status'],
    "To-Do": ['Task', 'Due Date', 'Priority', 'Category', 'Status', 'Notes'],
    "Automation Logs": ['Date', 'Script', 'Outcome', 'Details'],
    "Sync Log": ['Date', 'Action', 'Status', 'Notes']
}

# === VALIDATION ===
for tab_name, expected_cols in expected_headers.items():
    try:
        ws = sheet.worksheet(tab_name)
        actual_cols = ws.row_values(1)
        if actual_cols != expected_cols:
            print(f"[⚠️] Header mismatch in '{tab_name}'")
            print(f"    Expected: {expected_cols}")
            print(f"    Found:    {actual_cols}")
        else:
            print(f"[✅] '{tab_name}' headers are valid.")
    except Exception as e:
        print(f"[❌] Cannot access '{tab_name}': {str(e)}")
