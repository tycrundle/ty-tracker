# === sheet_schema.py ===

tab_schemas = {
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

category_tag_map = {
    "[TO-DO]": "To-Do",
    "[NOTE]": "Notes",
    "[ADDRESS]": "Addresses",
    "[BIRTHDAY]": "Birthdays Anniversaries",
    "[REMINDER]": "Agenda",
    "[FINANCE]": "Finances",
    "[BOOK]": "Books Media",
    "[SHOPPING]": "Shopping Wishlist",
    "[FITNESS]": "Fitness Health",
    "[PROJECT]": "Work Projects",
    "[CONTACT]": "Contacts Networking",
    "[TRAVEL]": "Travel",
    "[PET]": "Pets",
    "[GOAL]": "Goals",
    "[AI]": "AI Requests",
    "[ARCHIVE]": "Archive",
    "[LOG]": "Logs",
    "[META]": "Meta",
    "[AUTOMATION]": "Automation Logs",
    "[SYNC]": "Sync Log"
}

def get_field_count(tab_name):
    return len(tab_schemas.get(tab_name, []))
