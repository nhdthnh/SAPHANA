import tkinter as tk
from tkinter import messagebox
def editID():
    # Định nghĩa mật khẩu đúng
    CORRECT_PASSWORD = "@cronis1"

    def load_default_values():
        with open("Configure/spreadsheet_id.txt", "r") as f:
            lines = f.readlines()
            return lines

    def show_main_window():
        # Ẩn cửa sổ nhập mật khẩu
        password_window.destroy()
        
        # Tạo cửa sổ chính
        main_window = tk.Tk()
        main_window.title("Spreadsheet ID")
        main_window.geometry("500x50")  # Kéo dài kích thước cửa sổ
        main_window.resizable(False, False)  # Không cho phép thay đổi kích thước cửa sổ
        # Tạo các label và entry
        tk.Label(main_window, text="Spreadsheet ID:").grid(row=0, column=0)
        spreadsheet_entry = tk.Entry(main_window, width=50)
        spreadsheet_entry.grid(row=0, column=1)

        # Tạo các label và entry cho dòng thứ hai
        tk.Label(main_window, text="Second ID:").grid(row=1, column=0)
        second_line_entry = tk.Entry(main_window, width=50)
        second_line_entry.grid(row=1, column=1)

        # Tải các giá trị mặc định từ file
        spreadsheet, second_line = load_default_values()
        spreadsheet_entry.insert(0, spreadsheet)
        second_line_entry.insert(0, second_line)

        def save_info():
            spreadsheet = spreadsheet_entry.get()
            second_line = second_line_entry.get()
            # Lưu thông tin vào file
            with open("Configure/spreadsheet_id.txt", "w") as f:
                f.write(f"{spreadsheet.strip()}\n{second_line.strip()}")
            
            messagebox.showinfo("Success", "Information saved successfully!")
            main_window.destroy()

        # Tạo nút Save
        save_button = tk.Button(main_window, text="Save", command=save_info)
        save_button.grid(row=0, column=2)
        main_window.mainloop()

    def check_password():
        entered_password = password_entry.get()
        if entered_password == CORRECT_PASSWORD:
            show_main_window()  # Mở cửa sổ chính
        else:
            messagebox.showerror("Error", "Incorrect password!")


    # Tạo cửa sổ nhập mật khẩu
    password_window = tk.Tk()
    password_window.title("Enter Password")

    tk.Label(password_window, text="Password:").pack()
    password_entry = tk.Entry(password_window, show = "*")
    password_entry.pack()
    password_entry.bind("<Return>", lambda event: check_password())

    # Tạo nút xác nhận mật khẩu
    submit_button = tk.Button(password_window, text="Submit", command=check_password)
    submit_button.pack()

    password_window.mainloop()