import tkinter as tk
from tkinter import messagebox
def edit_connection():
# Định nghĩa mật khẩu đúng
    CORRECT_PASSWORD = "@cronis1"

    def load_default_values():
        try:
            with open("Configure/connection_info.txt", "r") as f:
                lines = f.readlines()
                # Đọc các giá trị từ file
                host = lines[0].strip().split(": ")[1]
                port = lines[1].strip().split(": ")[1]
                user = lines[2].strip().split(": ")[1]
                password = lines[3].strip().split(": ")[1]
                return host, port, user, password
        except FileNotFoundError:
            return "", "", "", ""  # Trả về giá trị rỗng nếu file không tồn tại

    def show_main_window():
        # Ẩn cửa sổ nhập mật khẩu
        password_window.withdraw()
        
        # Tạo cửa sổ chính
        main_window = tk.Tk()
        main_window.title("Configure/Connection Info")
        main_window.geometry("300x150")  # Kéo dài kích thước cửa sổ

        # Tạo các label và entry
        tk.Label(main_window, text="Host:").grid(row=0, column=0)
        host_entry = tk.Entry(main_window)
        host_entry.grid(row=0, column=1)

        tk.Label(main_window, text="Port:").grid(row=1, column=0)
        port_entry = tk.Entry(main_window)
        port_entry.grid(row=1, column=1)

        tk.Label(main_window, text="User:").grid(row=2, column=0)
        user_entry = tk.Entry(main_window)
        user_entry.grid(row=2, column=1)

        tk.Label(main_window, text="Password:").grid(row=3, column=0)
        password_entry = tk.Entry(main_window, show='*')
        password_entry.grid(row=3, column=1)

        # Tải các giá trị mặc định từ file
        host, port, user, password = load_default_values()
        host_entry.insert(0, host)
        port_entry.insert(0, port)
        user_entry.insert(0, user)
        password_entry.insert(0, password)

        def save_info():
            host = host_entry.get()
            port = port_entry.get()
            user = user_entry.get()
            password = password_entry.get()
            
            # Lưu thông tin vào file
            with open("Configure/connection_info.txt", "w") as f:
                f.write(f"host: {host}\n")
                f.write(f"port: {port}\n")
                f.write(f"user: {user}\n")
                f.write(f"password: {password}\n")
            
            messagebox.showinfo("Success", "Information saved successfully!")
            main_window.destroy()

        # Tạo nút Save
        save_button = tk.Button(main_window, text="Save", command=save_info)
        save_button.grid(row=4, columnspan=2)

        main_window.mainloop()

    def check_password():
        entered_password = password_entry.get()
        if entered_password == CORRECT_PASSWORD:
            password_window.withdraw()  # Ẩn cửa sổ nhập mật khẩu
            show_main_window()  # Mở cửa sổ chính
        else:
            messagebox.showerror("Error", "Incorrect password!")

    # Thêm sự kiện nhấn phím Enter


    # Tạo cửa sổ nhập mật khẩu
    password_window = tk.Tk()
    password_window.title("Enter Password")

    tk.Label(password_window, text="Password:").pack()
    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()
    password_entry.bind("<Return>", lambda event: check_password())

    # Tạo nút xác nhận mật khẩu
    submit_button = tk.Button(password_window, text="Submit", command=check_password)
    submit_button.pack()

    password_window.mainloop()