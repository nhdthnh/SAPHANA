import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Read Spreadsheet ID
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
        return None  # No data in column A
    return [row[0] for row in values[1:] if row]  # Skip header and empty rows
def Modify_Customer_code():
    # Retrieve customer codes from Google Sheets
    sheet_name = "MT-DSKH"
    customer_codes = get_column_a_values(sheet_name)
    if customer_codes:
        card_code_values = ", ".join([f"'{value}'" for value in customer_codes])

        # Read MT.txt content
        file_path = 'SQL QUERY/MT.txt'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                mt_content = file.read()
            print("Original content loaded successfully.")

            # Update the WHERE clause
            pattern = r'WHERE T2\."CardCode" IN \((.*?)\)'
            replacement = f'WHERE T2."CardCode" IN ({card_code_values})'
            new_mt_content = re.sub(pattern, replacement, mt_content, flags=re.DOTALL)

            # Verify the replacement result
            if new_mt_content == mt_content:
                print("No changes made. Check the regex pattern or the file content.")
            else:
                # Write back updated content
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_mt_content)
                print("File updated successfully.")

        except Exception as e:
            print(f"Error reading or writing the file: {e}")
    else:
        print("No valid data in column A of the Google Sheet.")
