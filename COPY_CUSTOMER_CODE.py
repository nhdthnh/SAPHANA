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

def copy_customer_code(source_spreadsheet_id, destination_spreadsheet_id, source_sheet_name, destination_sheet_name, column_code, column_name, column_code_sale_quotation, column_note, responsible_person):
    # Get all values from the source sheet
    data = get_all_values(source_spreadsheet_id, source_sheet_name)

    header_row = data[1]  # Assuming the header is in the second row (index 1)

    code_index = header_row.index(column_code)
    code_values = [[row[code_index]] for row in data[2:] if len(row) > code_index]
    write_values(destination_spreadsheet_id, destination_sheet_name, code_values, 'A')

    name_index = header_row.index(column_name)
    name_values = [[row[name_index]] for row in data[2:] if len(row) > name_index]
    write_values(destination_spreadsheet_id, destination_sheet_name, name_values, 'B')

    code_sale_quotation_index = header_row.index(column_code_sale_quotation)
    code_sale_quotation_values = [[row[code_sale_quotation_index]] for row in data[2:] if len(row) > code_sale_quotation_index]
    write_values(destination_spreadsheet_id,destination_sheet_name, code_sale_quotation_values, 'C')

    note_index = header_row.index(column_note)
    note_values = [[row[note_index]] for row in data[2:] if len(row) > note_index]
    write_values(destination_spreadsheet_id,destination_sheet_name, note_values, 'D')

    responsible_person_index = header_row.index(responsible_person)
    responsible_person_values = [[row[responsible_person_index] if len(row) > responsible_person_index else ""] for row in data[2:]]
    write_values(destination_spreadsheet_id, destination_sheet_name, responsible_person_values, 'E')
    print("Done")
    



# Example usage
source_spreadsheet_id = "1zxotffwggzpITJiYMJAHGJS-YzpdUAI08Wn4gMh5Opc"
destination_spreadsheet_id = "17rIeCbiYwiIncRar-i_ZiU7Czg9jGyz5YzobwP-ZMbo"
source_sheet_name = 'MÃ KHÁCH-SALE QUOTATION-SO'
destination_sheet_name = 'MT-DSKH'
column_code = "MÃ KHÁCH STORE"
column_name = "CONTACT PERSON"
column_code_sale_quotation = "MÃ SALE QUOTATION"
column_note = "Note"
responsible_person = "Người phụ trách"


def main_copy_code():
    copy_customer_code(source_spreadsheet_id, destination_spreadsheet_id, source_sheet_name, destination_sheet_name, column_code, column_name, column_code_sale_quotation, column_note, responsible_person)

# # copy_customer_code(source_spreadsheet_id, destination_spreadsheet_id, source_sheet_name, destination_sheet_name, column_code, column_name)