import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

with open("creds.json") as f:
    creds_json = json.load(f)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Open the Google Sheet by URL
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1gLarCMGluthM7cbp4hSCMrDfjMwJHS1PsB8DzmX0pjc/edit")

# Define tab enhancements
enhancements = {
    "Goals": ["Progress", "Priority"],
    "To Do": ["Category", "Last Updated"],
    "Notes": ["Tag"],
    "Pets": ["Medication", "Vet Visit Date", "Follow-Up Needed"],
    "Travel": ["Status", "Checklist Link"]
}

for tab, new_columns in enhancements.items():
    try:
        ws = sheet.worksheet(tab)
        data = ws.get_all_records()
        headers = ws.row_values(1)

        for col in new_columns:
            if col not in headers:
                headers.append(col)
                for row in data:
                    row[col] = ""

        updated_data = [headers] + [[row.get(col, "") for col in headers] for row in data]
        ws.clear()
        ws.update("A1", updated_data)
        print(f"✅ Updated tab: {tab}")

    except gspread.exceptions.WorksheetNotFound:
        print(f"❌ Tab not found: {tab}")
