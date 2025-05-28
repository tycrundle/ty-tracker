import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Load JSON credentials
with open("creds.json") as f:
    json_creds = json.load(f)

# Authorize
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
client = gspread.authorize(creds)

# Open the full Google Sheet by URL
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1gLarCMGluthM7cbp4hSCMrDfjMwJHS1PsB8DzmX0pjc/edit")

# List of known tabs to sync
tabs = ["Agenda", "Goals", "To Do", "Notes", "Pets", "Travel"]

# Fetch and display contents for each
for tab in tabs:
    worksheet = sheet.worksheet(tab)
    data = worksheet.get_all_records()
    print(f"\n✅ Synced tab: {tab} — {len(data)} rows")
