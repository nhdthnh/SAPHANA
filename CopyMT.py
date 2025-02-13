import gspread
from oauth2client.service_account import ServiceAccountCredentials

def Copy(sheet_name):
    # Sử dụng OAuth2 để xác thực
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('Configure/credentials.json', scope)
    client = gspread.authorize(creds)

    # Đọc ID1 và ID2 từ file spreadsheet_id
    with open('Configure/spreadsheet_id.txt', 'r') as file:
        lines = file.readlines()
        ID1 = lines[0].strip()  # Hàng 1 cho ID1
        ID2 = lines[1].strip()  # Hàng 2 cho ID2

    try:
        # Mở file Google Sheets đầu tiên
        source_sheet = client.open_by_key(ID1).worksheet(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Spreadsheet with ID {ID1} not found.")
        return

    try:
        # Mở file Google Sheets thứ hai
        destination_sheet = client.open_by_key(ID2).worksheet(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Spreadsheet with ID {ID2} not found.")
        return

    # Lấy tất cả dữ liệu từ sheet nguồn và bỏ qua header
    data = source_sheet.get_all_values()[1:]  # Bỏ qua hàng đầu tiên (header)

    # Dán dữ liệu bắt đầu từ ô A2 với định dạng RAW
    destination_sheet.update('A2', data, value_input_option='RAW')  # Cập nhật dữ liệu mới bắt đầu từ ô A2 với định dạng RAW
    print (f"Cloning sheet {sheet_name} successfully")
