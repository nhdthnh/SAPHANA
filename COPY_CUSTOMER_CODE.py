import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Initialize Google Sheets API
creds = service_account.Credentials.from_service_account_file('Configure/credentials.json')
service = build('sheets', 'v4', credentials=creds)

# Function to get all values from a specific sheet
def get_all_values(spreadsheet_id, sheet_name):
    range_name = f"{sheet_name}!A:Z"  # Adjust the range as needed
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values

# Function to write values to a specific sheet starting from A2
def write_values(spreadsheet_id, sheet_name, values, start_column):
    range_name = f"{sheet_name}!{start_column}2"
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="USER_ENTERED", body=body).execute()
    return result

def copy_customer_code(source_spreadsheet_id, destination_spreadsheet_id, source_sheet_name, destination_sheet_name, column_code, column_name):
    # Get all values from the source sheet
    data = get_all_values(source_spreadsheet_id, source_sheet_name)

    # Find the index of the column with header "MÃ KHÁCH STORE"
    header_row = data[1]  # Assuming the header is in the second row (index 1)
    code_index = header_row.index(column_code)

    # Extract values of the column with header "MÃ KHÁCH STORE"
    code_values = [[row[code_index]] for row in data[2:] if len(row) > code_index]

    # Write values to the destination sheet starting from A2
    write_values(destination_spreadsheet_id, destination_sheet_name, code_values, 'A')

    # Find the index of the column with header "CONTACT PERSON"
    name_index = header_row.index(column_name)

    # Extract values of the column with header "CONTACT PERSON"
    name_values = [[row[name_index]] for row in data[2:] if len(row) > name_index]

    # Write values to the destination sheet starting from B2
    write_values(destination_spreadsheet_id, destination_sheet_name, name_values, 'B')


# # Example usage
# source_spreadsheet_id = "1zxotffwggzpITJiYMJAHGJS-YzpdUAI08Wn4gMh5Opc"
# destination_spreadsheet_id = "1T1AAZer-6S2NmvbCb6XjRhAgXDEnmg70EtigTFK4xeo"
# source_sheet_name = 'MÃ KHÁCH-SALE QUOTATION-SO'
# destination_sheet_name = 'MT-DSKH'
# column_code = "MÃ KHÁCH STORE"
# column_name = "CONTACT PERSON"

# copy_customer_code(source_spreadsheet_id, destination_spreadsheet_id, source_sheet_name, destination_sheet_name, column_code, column_name)