import re
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Read Spreadsheet ID from file
with open('Configure/spreadsheet_id.txt', 'r') as file:
    lines = file.readlines()
    spreadsheet_id = lines[0].strip()  # Hàng 1 cho ID1

# Initialize Google Sheets API
creds = service_account.Credentials.from_service_account_file('Configure/credentials.json')
service = build('sheets', 'v4', credentials=creds)

# Function to get column A values
def get_column_a_values(sheet_name):
    range_name = f"{sheet_name}!A:A"
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    if not values or len(values) < 2:
        return None  # No data
    return [row[0] for row in values[1:] if row]  # Skip header and empty rows

def Modify_Product_code():
    item_codes = get_column_a_values("QUEENAM-SP")

    item_code_values = ", ".join([f"'{value}'" for value in item_codes]) if item_codes else ""

    # Get all .txt files in the SQL QUERY directory
    directory = 'SQL QUERY'
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

    for txt_file in txt_files:
        file_path = os.path.join(directory, txt_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                mt_content = file.read()
            print(f"Original content loaded successfully from {file_path}.")

            # Update WHERE T0."ItemCode"
            if item_code_values:
                pattern_itemcode = r'."ItemCode" IN \((.*?)\)'
                replacement_itemcode = f'."ItemCode" IN ({item_code_values})'
                
                mt_content = re.sub(pattern_itemcode, replacement_itemcode, mt_content, flags=re.DOTALL)
                print(replacement_itemcode)
            
                # Write back updated content
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(mt_content)
                print(f"File updated successfully: {file_path}")

        except Exception as e:
            print(f"Error reading or writing the file {file_path}: {e}")
