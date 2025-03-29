import tkinter as tk
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from tkinter import filedialog  # Nhập thư viện cho hộp thoại chọn tệp

# Read Spreadsheet ID from file


# Initialize Google Sheets API
creds = service_account.Credentials.from_service_account_file('Configure/credentials.json')
service = build('sheets', 'v4', credentials=creds)


def get_column_a_values(sheet_name, header, spreadsheet_id_value):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id_value, range=sheet_name).execute()
    values = result.get('values', [])
    if not values or len(values) < 2:
        return None  # No data

    header_index = values[0].index(header) if header in values[0] else None  # Tìm chỉ số của header
    if header_index is None:
        return None  # Header không tìm thấy

    # Trả về danh sách các giá trị cho header cụ thể
    return [row[header_index] for row in values[1:] if row]  # Bỏ qua hàng đầu và hàng trống

class TextInputApp:

    def __init__(self, master):   
        def get():
            try:
                sheet_name = self.text1.get("1.0", tk.END).strip()  # Get sheet name from text1
                column_name = self.text2.get("1.0", tk.END).strip()
                id_sheet =  self.text_id.get("1.0",tk.END).strip()
                item_codes = get_column_a_values(sheet_name, column_name, id_sheet)
                print(item_codes)
                # Remove periods from each item code
                item_codes = [code.replace('.', '') for code in item_codes] if item_codes else []
                item_code_values = ", ".join([f"'{value}'" for value in item_codes]) if item_codes else ""
                if item_codes:
                    self.text3.delete("1.0", tk.END)  # Clear existing text
                    self.text3.insert(tk.END, item_code_values)  # Insert item codes into text3
                else:
                    self.text3.delete("1.0", tk.END)  # Clear existing text
                    self.text3.insert(tk.END, "No data found.")  # Indicate no data found
            except Exception as e:
                self.text3.delete("1.0", tk.END)  # Clear existing text
                self.text3.insert(tk.END, f"Error: {str(e)}")  # Log error message

        
        def browse():
            file_path = filedialog.askopenfilename()  # Mở hộp thoại chọn tệp
            if file_path:  # Kiểm tra nếu có tệp được chọn
                self.text3.delete("1.0", tk.END)  # Xóa nội dung hiện tại trong text1
                self.text3.insert(tk.END, file_path)  # Chèn đường dẫn tệp vào text1
                
                # Mở và đọc nội dung của file txt với encoding utf-8
                with open(file_path, 'r', encoding='utf-8') as file:  # Mở file để đọc
                    content = file.read()  # Đọc nội dung file
                    self.text4.delete("1.0", tk.END)  # Xóa nội dung hiện tại trong text4
                    self.text4.insert(tk.END, content)  # Chèn nội dung vào text4
        
        def save_as():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                       filetypes=[("Text files", "*.txt"), ("All files", "*.*")])  # Mở hộp thoại lưu tệp
            if file_path:  # Kiểm tra nếu có tệp được chọn
                content = self.text4.get("1.0", tk.END)  # Lấy nội dung từ text4
                with open(file_path, 'w', encoding='utf-8') as file:  # Mở file để ghi
                    file.write(content)  # Ghi nội dung vào file

        self.master = master
        master.title("Text Input Application")
        master.resizable(False, False)  # Không cho phép thay đổi kích thước cửa sổ
        # Tạo một khung để chứa text1 và text2
        sheet = tk.Frame(master)
        sheet.pack(side=tk.TOP)
        self.label_id = tk.Label(sheet, text="Spreadsheet ID: ")
        self.label_id.pack(side=tk.LEFT)
        self.text_id = tk.Text(sheet, height=1, width=50)
        self.text_id.pack(side=tk.LEFT)  # Đặt text1 bên trái
        with open('Configure/spreadsheet_id.txt', 'r') as file:
            lines = file.readlines()
            spreadsheet_id = lines[1].strip()  # Hàng 1 cho ID1
        self.text_id.insert(tk.END, spreadsheet_id)  # Chèn nội dung vào text4
        self.label1 = tk.Label(sheet, text="Sheet name: ")
        self.label1.pack(side=tk.LEFT)
        self.text1 = tk.Text(sheet, height=1, width=20)
        self.text1.pack(side=tk.LEFT)  # Đặt text1 bên trái

        self.label2 = tk.Label(sheet, text="Column: ")
        self.label2.pack(side=tk.LEFT)
        self.text2 = tk.Text(sheet, height=1, width=20)
        self.text2.pack(side=tk.LEFT)  # Đặt text2 bên phải
        self.button_get = tk.Button(sheet, text="GET", command= get)
        self.button_get.pack(side=tk.LEFT)
        self.button_browse = tk.Button(sheet, text="BROWSE", command= browse)
        self.button_browse.pack(side=tk.LEFT)
        self.button_save = tk.Button(sheet, text="SAVE AS", command=save_as)  # Thêm nút SAVE AS
        self.button_save.pack(side=tk.LEFT)

        modify = tk.Frame(master)
        modify.pack(side=tk.TOP)

        # Thêm label và text3
        self.label3 = tk.Label(modify, text="OUTPUT:")
        self.label3.grid(row=0, column=0)  # Đặt label3 ở hàng 0, cột 0
        self.text3 = tk.Text(modify, height=50, width=40)
        self.text3.grid(row=1, column=0)  # Đặt text3 ở hàng 1, cột 0

        # Thêm label và text4
        self.label4 = tk.Label(modify, text="FILE CONTENT")
        self.label4.grid(row=0, column=1)  # Đặt label4 ở hàng 0, cột 1
        self.text4 = tk.Text(modify, height=50, width=100)
        self.text4.grid(row=1, column=1)  # Đặt text4 ở hàng 1, cột 1

if __name__ == "__main__":
    root = tk.Tk()
    app = TextInputApp(root)
    root.mainloop()  # Khởi động vòng lặp chính của Tkinter
