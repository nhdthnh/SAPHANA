from hdbcli import dbapi
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from SAPHANA_CONNECTION import connect_and_process_data  # Import the new module
import GET_CUSTOMER_CODE
import COPY_CUSTOMER_CODE

# Khai báo biến toàn cục

def main_function():
    print("🔄 Running task...")  # In ra console để kiểm tra
    # Biến đếm số lần chạy và số lần chạy thành công

    # Đọc thông tin kết nối từ file
    with open('Configure/connection_info.txt', 'r') as file:
        for line in file:
            key, value = line.split(':', 1)  # Tách key và value
            if key.strip() == 'host':
                host = value.strip()  # Địa chỉ máy chủ SAP HANA
            elif key.strip() == 'port':
                port = int(value.strip())  # Cổng mặc định của SAP HANA
            elif key.strip() == 'user':
                user = value.strip()  # Tên người dùng
            elif key.strip() == 'password':
                password = value.strip()  # Mật khẩu

    # Đọc Spreadsheet ID từ file
    with open('Configure/spreadsheet_id.txt', 'r') as file:
        lines = file.readlines()
        spreadsheet_id = lines[0].strip()  # Hàng 1 cho ID1
        spreadsheet_id1 = lines[1].strip()

    # Khởi tạo Google Sheets service
    creds = service_account.Credentials.from_service_account_file('Configure/credentials.json')
    service = build('sheets', 'v4', credentials=creds)

    def log_error(service, spreadsheet_id, error_message):
        try:
            # Lấy thời gian hiện tại
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Chuẩn bị dữ liệu log
            log_data = [[current_time, str(error_message)]]
            
            # Đọc dữ liệu hiện tại từ sheet LOG
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='LOG!A:B'
            ).execute()
            
            # Nếu đã có dữ liệu, thêm vào đầu danh sách
            if 'values' in result:
                existing_data = result['values']
                log_data.extend(existing_data)
            
            # Cập nhật toàn bộ dữ liệu
            body = {
                'values': log_data
            }
            
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='LOG!A1',
                valueInputOption='RAW',
                body=body
            ).execute()
        except Exception as e:
            print(f"Can not log: {str(e)}")

    # Đọc tên sheet từ file
    with open('Configure/sheet_name.txt', 'r') as file:
        sheet_names = []  # Khởi tạo danh sách rỗng
        for line in file:  # Sử dụng vòng lặp for để đọc từng dòng
            sheet_name = line.strip()  # Lấy tên sheet từ dòng hiện tại
            print(f"Processing sheet: {sheet_name}")
            # Kết nối đến SAP HANA
            try:
                query_file = f"SQL QUERY/{sheet_name}.txt"  # Tạo tên file query tương ứng với sheet_name và thêm đường dẫn folder
                connect_and_process_data(host, port, user, password, sheet_name, service, spreadsheet_id, query_file)  # Pass the specific query file
                log_error(service, spreadsheet_id, "Update google sheet successfully")
            except Exception as e:
                error_message = f"Connect SAP HANA unsuccessfully: {str(e)}"
                print(error_message)
                # Ghi log lỗi vào sheet LOG
                log_error(service, spreadsheet_id, error_message)
                break

    with open('Configure/second_sheet_name.txt', 'r') as file:
        for line in file:  # Sử dụng vòng lặp for để đọc từng dòng
            sheet_name1 = line.strip()  # Lấy tên sheet từ dòng hiện tại
            print(f"Processing sheet: {sheet_name1}")
            # Kết nối đến SAP HANA
            try:
                query_file = f"SQL QUERY/{sheet_name1}.txt"  # Tạo tên file query tương ứng với sheet_name và thêm đường dẫn folder
                connect_and_process_data(host, port, user, password, sheet_name1, service, spreadsheet_id1, query_file)  # Pass the specific query file
                log_error(service, spreadsheet_id1, "Update google sheet successfully")
            except Exception as e:
                error_message = f"Connect SAP HANA unsuccessfully: {str(e)}"
                print(error_message)
                log_error(service, spreadsheet_id1, error_message)
                break
            
COPY_CUSTOMER_CODE.main_copy_code()
GET_CUSTOMER_CODE.Modify_Customer_code()
main_function()