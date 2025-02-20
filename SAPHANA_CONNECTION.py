import decimal
import socket
from hdbcli import dbapi

def connect_and_process_data(host, port, user, password, sheet_name, service, spreadsheet_id, sql_query_code):

    # Set default timeout for socket connections
    socket.setdefaulttimeout(10)  # 10 seconds timeout
    
    conn = dbapi.connect(
        address=host,
        port=port,
        user=user,
        password=password
    )
    print(f"SAP HANA CONNECTED FOR SHEET NAME: {sheet_name}!")
    
    # Reset timeout to default
    socket.setdefaulttimeout(None)
    
    # Tạo một con trỏ để thực thi câu lệnh SQL
    cursor = conn.cursor()

    # Đọc truy vấn từ file
    with open(sql_query_code, 'r', encoding='utf-8') as file:
        sql_query = file.read()
    
    # Thực hiện truy vấn
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    # Chuẩn bị dữ liệu để đưa vào Google Sheets
    values = []
    for row in results:
        # Chuyển đổi các giá trị Decimal thành float
        converted_row = []
        for value in row:
            if isinstance(value, (decimal.Decimal)):
                converted_row.append(float(value))
            else:
                converted_row.append(value)
        values.append(converted_row)
    
    # Xóa tất cả các dòng từ hàng 2 trở xuống
    clear_range = f'{sheet_name}!A2:Z'
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=clear_range
    ).execute()
    
    # Cập nhật vào Google Sheets
    body = {
        'values': values
    }
    
    # Xác định range để update (từ A2 trở đi)
    range_name = f'{sheet_name}!A2'
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"Successfully updated data to Google Sheets for sheet: {sheet_name}!")
    # Đóng kết nối
    cursor.close()
    conn.close()