import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Thêm import cho ttk
import threading
import time
import SAPHANA  # Giả sử bạn đã định nghĩa các chức năng trong SAPHANA.py
from PIL import Image
import pystray
from pystray import MenuItem, Icon
import sys

# Thêm biến toàn cục để kiểm soát việc lặp lại
running = True

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):  # Phương thức này cần thiết để tương thích với Python
        pass

def run_task():
    try:
        # Gọi hàm từ SAPHANA.py để thực hiện công việc
        SAPHANA.main_function()  # Thay thế bằng hàm chính của bạn
        root.after(0, lambda: [start_scheduled_task()])  # Gọi lại hàm để lặp lại
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}"))

def run_task_maunal():
    SAPHANA.main_function()
    # Thêm thông báo hoàn tất
    if messagebox.askyesno("Thông báo", "Chạy xong! Bạn có muốn thoát không?"):
        root.quit()  # Thoát GUI nếu người dùng chọn Yes

def on_quit(icon, item):
    global running  # Sử dụng biến toàn cục
    running = False  # Dừng việc lặp lại
    icon.stop()
    root.quit()

def on_icon_double_click(icon, item):
    root.deiconify()  # Hiển thị lại cửa sổ chính
    root.lift()  # Đưa cửa sổ lên trên cùng
    root.focus_force()  # Đảm bảo cửa sổ nhận được tiêu điểm

def setup(icon):
    icon.visible = True
    icon.on_double_click = on_icon_double_click  # Gán hàm xử lý cho sự kiện double click

def showGUI():
    root.mainloop()    

def minimize_to_tray():
    root.withdraw()  # Ẩn cửa sổ chính
    icon = Icon("test_icon", Image.open("icon.png"), "SAP HANA Task Scheduler", menu=pystray.Menu(
        MenuItem("Quit", on_quit)
    ))
    icon.run(setup)

def schedule_task(interval):
    global running  # Sử dụng biến toàn cục
    while running:  # Kiểm tra biến running
        time.sleep(interval)  # Chờ 20 giây
        SAPHANA.main_function()  # Thay thế bằng hàm chính của bạn

def start_scheduled_task():
    interval = 10
    # interval = int(schedule_var.get()) * 60  # Chuyển đổi phút thành giây
    threading.Thread(target=schedule_task, args=(interval,), daemon=True).start()
    # minimize_to_tray()  # Thay đổi từ iconify sang minimize_to_tray

# Tạo cửa sổ chính
root = tk.Tk()
root.title("SAP HANA Task Scheduler")

# Nút chạy thủ công
run_button = tk.Button(root, text="RUN", command=run_task_maunal)
run_button.pack(pady=10)

# Chọn thời gian tự động
schedule_var = tk.StringVar(value='15')  # Mặc định là 15 phút
schedule_label = tk.Label(root, text="Chọn thời gian tự động (phút):")
schedule_label.pack(pady=5)

schedule_options = [15, 60, 180]  # 15 phút, 1 giờ, 3 giờ
schedule_menu = tk.OptionMenu(root, schedule_var, *schedule_options)
schedule_menu.pack(pady=5)

# Nút thiết lập
schedule_button = tk.Button(root, text="THIẾT ĐẶT", command=start_scheduled_task)
schedule_button.pack(pady=10)

# Tạo một textbox lớn để hiển thị console output
console_output = tk.Text(root, height=10, width=50)
console_output.pack(pady=10)

# Chuyển hướng stdout đến textbox
sys.stdout = RedirectText(console_output)

# Chạy GUI
root.mainloop()
