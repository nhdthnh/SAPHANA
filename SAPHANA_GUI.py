import tkinter as tk
from tkinter import messagebox
import threading
import time
import SAPHANA  # Giả sử bạn đã định nghĩa các chức năng trong SAPHANA.py
import sys
import GET_CUSTOMER_CODE
import GET_PRODUCT_CODE
import ADVANCE  # Thêm import cho file ADVANCE.py
import ConnectionGUI
import ID
import CopyMT
# Thêm biến toàn cục để kiểm soát việc lặp lại
running = True

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        if string.strip():  # Kiểm tra xem chuỗi không rỗng
            # Thêm thời gian vào đầu mỗi dòng
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")  # Lấy thời gian hiện tại
            self.text_widget.insert(tk.END, f"[{current_time}] {string}\n")  # Thêm thời gian và xuống dòng
            self.text_widget.see(tk.END)

    def flush(self):  # Phương thức này cần thiết để tương thích với Python
        pass

def run_task():
    try:
        # Gọi hàm từ SAPHANA.py để thực hiện công việc
        SAPHANA.main_function()  # Thay thế bằng hàm chính của bạn
        if checkbox_var.get():  # Kiểm tra xem checkbox có được chọn không
            values = text_var.get().split(",")  # Tách các giá trị bằng dấu phẩy
            for value in values:  # Lặp qua từng giá trị
                CopyMT.Copy(value.strip())  # Gọi hàm CopyMT.Copy với giá trị đã được loại bỏ khoảng trắng
        root.after(0, lambda: [start_scheduled_task()])  # Gọi lại hàm để lặp lại
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", f"Error: {str(e)}"))

def run_task_maunal():
    run_button.config(bg='green')  # Change button color to green when task starts
    try:
        SAPHANA.main_function()
        if checkbox_var.get():  # Kiểm tra xem checkbox có được chọn không
            values = text_var.get().split(",")  # Tách các giá trị bằng dấu phẩy
            for value in values:  # Lặp qua từng giá trị
                CopyMT.Copy(value.strip())  # Gọi hàm CopyMT.Copy với giá trị đã được loại bỏ khoảng trắng
        # Thêm thông báo hoàn tất
        messagebox.showinfo("Notification", "Done!!! 😺")
    finally:
        run_button.config(bg='red')  # Revert button color back to red after task completion

def on_quit():
    global running  # Sử dụng biến toàn cục
    running = False  # Dừng việc lặp lại
    root.destroy()

def on_icon_double_click(icon, item):
    root.deiconify()  # Hiển thị lại cửa sổ chính
    root.lift()  # Đưa cửa sổ lên trên cùng
    root.focus_force()  # Đảm bảo cửa sổ nhận được tiêu điểm

def schedule_task(interval):
    global running  # Sử dụng biến toàn cục
    while running:  # Kiểm tra biến running
        time.sleep(interval)  # Chờ 20 giây
        SAPHANA.main_function()  # Thay thế bằng hàm chính của bạn
        if checkbox_var.get():  # Kiểm tra xem checkbox có được chọn không
            values = text_var.get().split(",")  # Tách các giá trị bằng dấu phẩy
            for value in values:  # Lặp qua từng giá trị
                CopyMT.Copy(value.strip())  # Gọi hàm CopyMT.Copy với giá trị đã được loại bỏ khoảng trắng
        print("Restarting task...")

def start_scheduled_task():
    # interval = 10
    interval = int(schedule_var.get()) * 60  # Chuyển đổi phút thành giây
    threading.Thread(target=schedule_task, args=(interval,), daemon=True).start()
    print(f"Scheduled in {int(interval/60)} mins")

def Modify_customer_code():
    GET_CUSTOMER_CODE.Modify_Customer_code()

def Modify_Product_code():
    GET_PRODUCT_CODE.Modify_Product_code()

def load_listboxes_from_file():
    try:
        with open('Configure/sheet_name.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                sheet_output.insert(tk.END, line.strip())  # Thêm dòng vào sheet_output
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file: {str(e)}")

# Thêm các nút để tương tác với Listbox
def add_item():
    item = entry.get()
    sheet_output.insert(tk.END, item)  # Thêm mục vào sheet_output
    entry.delete(0, tk.END)  # Xóa giá trị trong entry
    save_to_file()

def delete_item():
    selected_item_index = sheet_output.curselection()
    if selected_item_index:
        if sheet_output.curselection():
            sheet_output.delete(selected_item_index)
        save_to_file()

def modify_item():
    selected_item_index = sheet_output.curselection()
    if selected_item_index:
        item = entry.get()
        if item:
            sheet_output.delete(selected_item_index)
            sheet_output.insert(selected_item_index, item)
            entry.delete(0, tk.END)  # Xóa giá trị trong entry
            save_to_file()

def save_to_file():
    with open('Configure/sheet_name.txt', 'w') as file:
        for item in sheet_output.get(0, tk.END):
            file.write(f"{item}\n")        

def open_text_input_app():
    new_window = tk.Toplevel(root)  # Tạo cửa sổ mới
    app = ADVANCE.TextInputApp(new_window)  # Khởi động ứng dụng TextInputApp

def editConnection():
    ConnectionGUI.edit_connection()

def editID():
    ID.editID()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("SAP HANA Task Scheduler")
# root.geometry("800x600")  # Đặt kích thước cố định cho cửa sổ GUI

root.resizable(False, False)  # Không cho phép thay đổi kích thước cửa sổ
root.iconbitmap("icon.ico")
# Tạo thanh menu
menu_bar = tk.Menu(root)
Configure = tk.Menu(menu_bar, tearoff=0)
Configure.add_command(label="Connection", command=editConnection)
Configure.add_command(label="Spreadsheet ID", command=editID)
menu_bar.add_cascade(label="Configure", menu=Configure)



code_menu = tk.Menu(menu_bar, tearoff=0)
code_menu.add_command(label="Customer", command=Modify_customer_code)
code_menu.add_command(label="Product", command=Modify_Product_code)
code_menu.add_command(label="Advance", command=open_text_input_app)
menu_bar.add_cascade(label="Modify", menu=code_menu)

# Gán thanh menu cho cửa sổ
root.config(menu=menu_bar)

# Create a frame to hold the RUN button and the schedule options
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

# Nút chạy thủ công
run_button = tk.Button(top_frame, text="RUN", command=run_task_maunal, bg='red', fg = 'white')  # Set initial color to red
run_button.pack(side=tk.LEFT, padx=(0, 5))  # Align to the left

# Chọn thời gian tự động
schedule_var = tk.StringVar(value='240')  # Mặc định là 15 phút
schedule_label = tk.Label(top_frame, text="Select automatic time (minutes):")
schedule_label.pack(side=tk.LEFT, padx=(5, 5))

schedule_options = [15, 60, 180,240]  # 15 phút, 1 giờ, 3 giờ
schedule_menu = tk.OptionMenu(top_frame, schedule_var, *schedule_options)
schedule_menu.pack(side=tk.LEFT, padx=(0, 5))

# Nút thiết lập
schedule_button = tk.Button(top_frame, text="SCHEDULE", command=start_scheduled_task, bg='blue', fg='white')
schedule_button.pack(side=tk.LEFT, padx=(5, 10))
 
both_sheet = tk.Frame(root)
both_sheet.pack(pady=10)

text_label = tk.Label(both_sheet,text="Copy Sheet")
text_label.pack(side=tk.LEFT)
text_var = tk.StringVar(value="MT")  # Biến cho Text
text_entry = tk.Entry(both_sheet, textvariable=text_var, width=30)  # Tạo Entry với giá trị mặc định
text_entry.pack(side=tk.LEFT, padx=(10, 5))  # Đặt Entry bên trái

checkbox_var = tk.BooleanVar(value=True)  # Biến cho Checkbox
checkbox = tk.Checkbutton(both_sheet, text="Run both sheet", variable=checkbox_var)  # Tạo Checkbox
checkbox.pack(side=tk.LEFT)  # Đặt Checkbox bên cạnh Entry

Modify_label = tk.Label(root, text="Modify sheet to run")
Modify_label.pack(padx=0)

txt_frame_modify = tk.Frame(root)
txt_frame_modify.pack(pady=10)

# Entry for adding/modifying items
entry = tk.Entry(txt_frame_modify, width=20)
entry.pack(side=tk.LEFT, padx=(10, 10))

# Nút thêm
add_button = tk.Button(txt_frame_modify, text="ADD", command=add_item)
add_button.pack(side=tk.LEFT, padx=(5, 5))

# Nút xóa
delete_button = tk.Button(txt_frame_modify, text="DELETE", command=delete_item)
delete_button.pack(side=tk.LEFT, padx=(5, 5))

# Nút sửa
modify_button = tk.Button(txt_frame_modify, text="MODIFY", command=modify_item)
modify_button.pack(side=tk.LEFT, padx=(5, 5))

txt_frame = tk.Frame(root)
txt_frame.pack(pady=10)

# Thay thế sheet_output bằng Listbox
sheet_output = tk.Listbox(txt_frame, height=10, width=50, bd=1, highlightbackground="black", highlightcolor="black")
sheet_output.pack(side=tk.LEFT, padx=(0, 10))  # Thêm khoảng cách bên phải

console_frame = tk.Frame(root)  # Tạo một frame mới để chứa label và button
console_frame.pack(pady=10)  # Đặt frame với khoảng cách trên và dưới

console_label = tk.Label(console_frame, text="Console output")  # Chuyển console_label vào frame
console_label.pack(side=tk.LEFT, padx=(0, 5))  # Đặt label bên trái với khoảng cách bên phải

# Thêm nút để xóa console
clear_button = tk.Button(console_frame, text="Clear", command=lambda: console_output.delete(1.0, tk.END))  # Nút để xóa nội dung console
clear_button.pack(side=tk.LEFT)  # Đặt nút bên cạnh label

# Tạo một Text widget lớn để hiển thị console output
console_output = tk.Text(root, height=10, width=50, bd=1, highlightbackground="black", highlightcolor="black")
console_output.pack(pady=10, fill=tk.X, expand=True)  # Cập nhật để chiếm 100% chiều rộng
console_output.config(wrap=tk.WORD)  # Cho phép xuống hàng theo từ

# Chuyển hướng stdout đến textbox
sys.stdout = RedirectText(console_output)

# Gọi hàm để tải dữ liệu vào Listbox khi khởi động
load_listboxes_from_file()

# Thêm sự kiện để dừng tất cả các thread khi cửa sổ chính đóng
root.protocol("WM_DELETE_WINDOW", on_quit)  # Gọi hàm on_quit khi cửa sổ chính bị đóng

# Chạy GUI
root.mainloop()
