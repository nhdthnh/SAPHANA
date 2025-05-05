import re

from googleapiclient.discovery import build
from google.oauth2 import service_account
import tkinter as tk
from tkinter import messagebox
import COPY_CUSTOMER_CODE

# Initialize Google Sheets API
creds = service_account.Credentials.from_service_account_file('Configure/credentials.json')
service = build('sheets', 'v4', credentials=creds)
def copy_customer_code_gui():
    # Function to get all values from a specific sheet
    def get_all_values(spreadsheet_id, sheet_name):
        range_name = f"{sheet_name}!A:Z"  # Adjust the range as needed
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        return values


    # Function to write values to a specific sheet starting from A2

    root = tk.Tk()
    root.title("Copy Customer Code")
    root.resizable(False, False)  # Không cho phép thay đổi kích thước cửa sổ
    # Labels and entries for each parameter
    tk.Label(root, text="Source Spreadsheet ID:").grid(row=0, column=0)
    source_spreadsheet_id_entry = tk.Entry(root, width=50)
    source_spreadsheet_id_entry.grid(row=0, column=1)

    # tk.Label(root, text="Destination Spreadsheet ID:").grid(row=1, column=0)
    # destination_spreadsheet_id_entry = tk.Entry(root, width=50)
    # destination_spreadsheet_id_entry.grid(row=1, column=1)

    tk.Label(root, text="Source Sheet Name:").grid(row=1, column=0)
    source_sheet_name_entry = tk.Entry(root, width=50)
    source_sheet_name_entry.grid(row=1, column=1)
    source_sheet_name_entry.insert(0, "MÃ KHÁCH-SALE QUOTATION-SO")

    tk.Label(root, text="Destination Sheet Name:").grid(row=2, column=0)
    destination_sheet_name_entry = tk.Entry(root, width=50)
    destination_sheet_name_entry.grid(row=2, column=1)
    destination_sheet_name_entry.insert(0, "MT-DSKH")

    tk.Label(root, text="HEADER MT-DSKH", font=("Arial", 10, "bold")).grid(row=3, column=0)
    tk.Label(root, text="HEADER MÃ KHÁCH-SALE QUOTATION-SO", font=("Arial", 10, "bold")).grid(row=3, column=1)

    tk.Label(root, text="Customer Code:").grid(row=4, column=0)
    column_code_entry = tk.Entry(root, width=50)
    column_code_entry.grid(row=4, column=1)
    column_code_entry.insert(0, "MÃ KHÁCH STORE")

    tk.Label(root, text="Customer Store:").grid(row=5, column=0)
    column_name_entry = tk.Entry(root, width=50)
    column_name_entry.grid(row=5, column=1)
    column_name_entry.insert(0, "CONTACT PERSON")

    tk.Label(root, text="Mã Đơn:").grid(row=6, column=0)
    column_code_sale_quotation_entry = tk.Entry(root, width=50)
    column_code_sale_quotation_entry.grid(row=6, column=1)
    column_code_sale_quotation_entry.insert(0, "MÃ SALE QUOTATION")

    tk.Label(root, text="Miền:").grid(row=7, column=0)
    column_note_entry = tk.Entry(root, width=50)
    column_note_entry.grid(row=7, column=1)
    column_note_entry.insert(0, "Note")

    tk.Label(root, text="").grid(row=8, column=0)
    column_person_entry = tk.Entry(root, width=50)
    column_person_entry.grid(row=8, column=1)
    column_person_entry.insert(0, "Người phụ trách")


    with open ("Configure/spreadsheet_id.txt", "r") as file:
        lines = file.readlines()
        ID1 = lines[0].strip()
        ID2 = lines[1].strip()  
        ID3 = lines[2].strip()
        source_spreadsheet_id_entry.insert(0, ID3)


    def on_submit():
        source_spreadsheet_id = source_spreadsheet_id_entry.get()
        # destination_spreadsheet_id = destination_spreadsheet_id_entry.get()
        source_sheet_name = source_sheet_name_entry.get()
        destination_sheet_name = destination_sheet_name_entry.get()
        column_code = column_code_entry.get()
        column_name = column_name_entry.get()
        column_code_sale_quotation = column_code_sale_quotation_entry.get()
        column_note = column_note_entry.get()
        column_person= column_person_entry.get()
        COPY_CUSTOMER_CODE.copy_customer_code(source_spreadsheet_id, ID1, source_sheet_name, destination_sheet_name, column_code, column_name, column_code_sale_quotation, column_note, column_person)
        COPY_CUSTOMER_CODE.copy_customer_code(source_spreadsheet_id, ID2, source_sheet_name, destination_sheet_name, column_code, column_name, column_code_sale_quotation, column_note, column_person)
        # messagebox.showinfo("Success", "Customer code and contact person copied successfully!")
        # root.quit()
        print("Customer code and contact person copied successfully!")

        # Test access to the destination spreadsheet
    # Submit button
    submit_button = tk.Button(root, text="Copy Data", command=on_submit)
    submit_button.grid(row=9, column=0, columnspan=2)

#     root.mainloop()
#     on_submit()
# copy_customer_code_gui()