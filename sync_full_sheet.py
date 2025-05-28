import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Set up scope and credentials
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Open the spreadsheet
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1gLarCMGluthM7cbp4hSCMrDfjMwJHS1PsB8DzmX0pjc/edit?usp=sharing")

# List of sheet names to fetch
tabs = ["Agenda", "To-Do", "Travel", "Notes"]
data = {}

# Read all tabs into dictionary
for tab in tabs:
    worksheet = sheet.worksheet(tab)
    rows = worksheet.get_all_records()
    data[tab] = rows

# Write data to local JSON file
with open("data/full_sheet.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Full sheet synced and saved to data/full_sheet.json")
