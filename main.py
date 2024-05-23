import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import tkinter.messagebox as messagebox
import os
import csv

path_of_csv = r"C:\Users\kuzey\OneDrive\Masaüstü" #Burayı değiştir
file_name = "database"                            # ve burayı


def create_csv_file(csv_name, path_for_csv):
    if not os.path.exists(os.path.join(path_for_csv, f"{csv_name}.csv")):
        with open(os.path.join(path_for_csv, f"{csv_name}.csv"), 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Kitap adi', 'Turu', 'Yazar','Yayin evi', 'Baski tarihi', 'Durumu', 'Kullanici ismi', 'Borclunun iletisim bilgileri','Odunc alinan zaman','Iade tarihi']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        return True
    else:
        return False

result = create_csv_file(file_name, path_of_csv)




def add_five_days(date_str):
    date = datetime.strptime(date_str, '%d/%m/%Y')
    days_to_add = timedelta(days=5)
    new_date = date + days_to_add
    return new_date.strftime('%d/%m/%Y')





csv_path = path_of_csv + "\\" + file_name + ".csv"


display_mapping = {
    "Available": "Mevcut",
    "Unavailable": "Mevcut değil",
}

column_mapping = {
    "Kitap adi": "Kitap adı",
    "Turu": "Türü",
    "Yayin evi": "Yayın evi",
    "Baski tarihi": "Baskı tarihi",
    "Kullanici ismi": "Kullanıcı ismi",
    "Borclunun iletisim bilgileri": "İletişim bilgisi",
    "Odunc alinan zaman": "Ödünç alınan tarih",
}


search_columns = [
    "ID", "Kitap adi", "Turu", "Yazar", "Yayin evi",
    "Baski tarihi", "Durumu", "Kullanici ismi",
    "Borclunun iletisim bilgileri", "Odunc alinan zaman"
]


search_labels = [
    "ID", "Kitap adı", "Türü", "Yazar", "Yayın evi",
    "Baskı tarihi", "Durumu", "Kullanıcı ismi",
    "İletişim bilgisi", "Ödünç alınan tarih"
]


def search_books(event=None):
    query = {}
    for entry, column in zip(search_entries, search_columns):
        query[column] = entry.get()
    filtered_df = df.copy()
    for column, value in query.items():
        if value:
            filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(value, case=False)]
    if filtered_df.empty and all(value == "" for value in query.values()):
        update_treeview(df)
    else:
        update_treeview(filtered_df)

tree = None

def update_treeview(dataframe):
    global tree
    current_date = datetime.now().strftime('%d/%m/%Y')
    for item in tree.get_children():
        tree.delete(item)

    for index, row in dataframe.iterrows():
        row_values = [display_mapping.get(value, value) if value else "" for value in row.tolist()]
        iade_tarihi_index = columns.index("Iade tarihi")
        iade_tarihi = row_values[iade_tarihi_index]
        if iade_tarihi == current_date:
            id_index = columns.index("ID")
            book_id = row_values[id_index]
            print("ID of the book with today's return date:", book_id)
            tree.insert("", "end", values=row_values, tags=('red_row',))
        else:
            tree.insert("", "end", values=row_values)
    

    tree.tag_configure('red_row', background='red')







# Function to add a book
def add_book():
    add_window = tk.Toplevel(root)
    add_window.title("Yeni Kitap Ekle")
    window_width = 300
    window_height = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    add_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    labels = ["Kitap adı", "Türü", "Yazar", "Yayın evi", "Baskı tarihi"]
    entries = {}

    for i, label in enumerate(labels):
        ttk.Label(add_window, text=label + ":").grid(row=i, column=0, padx=5, pady=5, sticky="w")  
        entry_var = tk.StringVar()  
        entry = ttk.Entry(add_window, textvariable=entry_var, justify="left") 
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[label] = entry_var

    def submit_new_book():

        book_data = {column_mapping[label]: entry.get() for label, entry in entries.items()}
        

        if any(value == "" for value in book_data.values()):
            messagebox.showerror("Hata", "Tüm alanları doldurun.")
            return

        publish_date = book_data["Baskı tarihi"]

        if len(publish_date) != 10 or publish_date.count('/') != 2:
            messagebox.showerror("Hata", "Geçersiz baskı tarihi formatı. Lütfen dd/mm/yyyy formatını kullanın.")
            return

        day, month, year = publish_date.split('/')
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            messagebox.showerror("Hata", "Geçersiz baskı tarihi formatı. Lütfen gün, ay ve yıl için sayıları kullanın.")
            return

        day = int(day)
        month = int(month)
        year = int(year)

        if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100):
            messagebox.showerror("Hata", "Geçersiz baskı tarihi. Lütfen geçerli bir tarih girin.")
            return

        new_id = df['ID'].max() + 1 if not df.empty else 1
        new_book = {
            'ID': new_id,
            **book_data,  
            'Durumu': 'Mevcut',
            'Kullanici ismi': '',
            'Borclunun iletisim bilgileri': '',
            'Odunc alinan zaman': ''
        }

        df.loc[len(df)] = new_book

        df.to_csv(csv_path, index=False)

        update_treeview(df)

        add_window.destroy()


    submit_button = ttk.Button(add_window, text="Ekle", command=submit_new_book)
    submit_button.grid(row=len(labels), columnspan=2, pady=5)


def delete_book():
    selected_items = tree.selection()
    if len(selected_items) > 1:
        messagebox.showinfo("Birden fazla kitap silme", "Birden fazla kitap silme desteklenmiyor. Lütfen sadece 1 tane kitap seçiniz.")
        return
    elif selected_items:
        item = tree.item(selected_items[0])
        values = item['values']
        kitap_adi_index = columns.index("Kitap adı")
        kitap_adi = values[kitap_adi_index]

        confirm_delete = messagebox.askyesno("Kitap Sil", f"{kitap_adi} Bu kitabı silmek istediğinize emin misiniz?")
        if confirm_delete:
            selected_index = tree.index(selected_items[0])
            df.drop(df.index[selected_index], inplace=True)
            df.reset_index(drop=True, inplace=True)
            df["ID"] =  df.index + 1

            filter_state = {column: entry.get() for entry, column in zip(search_entries, search_columns)}
            update_treeview(df)
            df.to_csv(csv_path, index=False)
            for column, value in filter_state.items():
                search_entries[search_columns.index(column)].delete(0, tk.END)
                search_entries[search_columns.index(column)].insert(0, value)
            search_books()

# Function to lend a book
def lend_book():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showinfo("Uyarı", "Ödünç vermek için bir kitap seçiniz.")
        return

    selected_item = selected_items[0]
    item = tree.item(selected_item)
    values = item['values']
    durumu_index = columns.index("Durumu")
    if values[durumu_index] != "Mevcut":
        messagebox.showinfo("Uyarı", "Seçili kitap mevcut değil. Ödünç verilemez.")
        return


    lend_window = tk.Toplevel(root)
    lend_window.title("Kitap Ödünç Ver")

    window_width = 300
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    lend_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    borrower_name_label = ttk.Label(lend_window, text="Ödünç Alan Kişi:")
    borrower_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    borrower_name_entry = ttk.Entry(lend_window)
    borrower_name_entry.grid(row=0, column=1, padx=5, pady=5)

    borrower_contact_label = ttk.Label(lend_window, text="İletişim Bilgisi:")
    borrower_contact_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    borrower_contact_entry = ttk.Entry(lend_window)
    borrower_contact_entry.grid(row=1, column=1, padx=5, pady=5)

    def submit_lend():
        borrower_name = borrower_name_entry.get()
        borrower_contact = borrower_contact_entry.get()

        if not borrower_name or not borrower_contact:
            messagebox.showerror("Hata", "Lütfen tüm bilgileri doldurun.")
            return

        book_id_index = columns.index("ID")
        book_id = values[book_id_index]
        borrow_date = datetime.now().strftime("%d/%m/%Y")
        df.loc[df['ID'] == int(book_id), 'Durumu'] = 'Mevcut değil'
        df.loc[df['ID'] == int(book_id), 'Kullanici ismi'] = borrower_name
        df.loc[df['ID'] == int(book_id), 'Borclunun iletisim bilgileri'] = borrower_contact
        df.loc[df['ID'] == int(book_id), 'Odunc alinan zaman'] = borrow_date
        df.loc[df['ID'] == int(book_id), 'Iade tarihi'] = add_five_days(borrow_date)

        df.to_csv(csv_path, index=False)

        update_treeview(df)

        lend_window.destroy()

    submit_button = ttk.Button(lend_window, text="Ödünç Ver", command=submit_lend)
    submit_button.grid(row=2, columnspan=2, pady=10)

def return_book():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showinfo("Uyarı", "İade etmek için bir kitap seçiniz.")
        return

    selected_item = selected_items[0]
    item = tree.item(selected_item)
    values = item['values']
    durumu_index = columns.index("Durumu")
    kitap_adi_index = columns.index("Kitap adı")
    kullanici_adi_index = columns.index("Kullanıcı ismi")
    kitap_adi = values[kitap_adi_index]
    kullanici_adi = values[kullanici_adi_index]

    if values[durumu_index] != "Mevcut değil":
        messagebox.showinfo("Uyarı", "Seçili kitap zaten mevcut. İade edilemez.")
        return

    return_window = tk.Toplevel(root)
    return_window.title("Kitap İade Et")

    window_width = 400
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    return_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    confirmation_label = ttk.Label(return_window, text=f'"{kitap_adi}" kitabını "{kullanici_adi}" kişisi geri getirdi mi?')
    confirmation_label.pack(pady=10)

    def confirm_return():
        selected_index = tree.index(selected_item)
        # Clear borrower information and loan date
        df.at[selected_index, 'Kullanici ismi'] = ''
        df.at[selected_index, 'Borclunun iletisim bilgileri'] = ''
        df.at[selected_index, 'Odunc alinan zaman'] = ''
        # Update status to "Mevcut"
        df.at[selected_index, 'Durumu'] = 'Mevcut'
        df.at[selected_index, 'Iade tarihi'] = ''


        df.to_csv(csv_path, index=False)
        update_treeview(df)

        return_window.destroy()
        return_button.config(state="disabled")  # Disable the button after use

    def cancel_return():
        return_window.destroy()

    yes_button = ttk.Button(return_window, text="Evet", command=confirm_return)
    yes_button.pack(side="left", padx=20, pady=10)

    no_button = ttk.Button(return_window, text="Hayır", command=cancel_return)
    no_button.pack(side="right", padx=20, pady=10)

    return_button.config(state="disabled")  # Disable the button after use



def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        values = item['values']
        durumu_index = columns.index("Durumu")
        if values[durumu_index] == "Mevcut":
            delete_button.config(state="normal")
            lend_button.config(state="normal")  
            return_button.config(state="disabled")  
        elif values[durumu_index] == "Mevcut değil":
            delete_button.config(state="disabled")
            lend_button.config(state="disabled")  
            return_button.config(state="normal")  



try:
    df = pd.read_csv(csv_path)
    df = df.fillna("")
    root = tk.Tk()
    root.title("Book Database")
    root.attributes('-fullscreen', True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    db_width = int(screen_width * 0.7)
    db_height = int(screen_height * 0.6)
    db_frame = ttk.Frame(root, width=db_width, height=db_height)
    db_frame.place(relx=0.45, rely=0.5, anchor=tk.CENTER)

    search_frame = ttk.Frame(root)
    search_frame.place(relx=0.9, rely=0.5, anchor=tk.CENTER)
    search_entries = []

    for i, (column, label) in enumerate(zip(search_columns, search_labels)):
        search_label = ttk.Label(search_frame, text=label + ":", justify="left")  
        search_label.grid(row=i, column=0, padx=5, pady=5, sticky="w") 
        search_entry = ttk.Entry(search_frame, width=20, justify="left")  
        search_entry.grid(row=i, column=1, padx=5, pady=5)
        search_entry.bind("<KeyRelease>", search_books)
        search_entries.append(search_entry)

    tree = ttk.Treeview(db_frame, padding=5, height=20)
    columns = [column_mapping.get(column, column) for column in df.columns.tolist()]
    tree["columns"] = columns
    tree["show"] = "headings"
    for column in columns:
        tree.heading(column, text=column)
        if column == "ID":
            tree.column(column, width=30)
        elif column == "Ödünç alınan tarih":
            tree.column(column, width=120)
        else:
            tree.column(column, width=100)

    for index, row in df.iterrows():
        row_values = [display_mapping.get(value, value) if value else "" for value in row.tolist()]
        tree.insert("", "end", values=row_values)
    
    tree.pack(expand=True, fill=tk.BOTH)
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    button_frame = tk.Frame(root)
    button_frame.place(relx=0.5, rely=0.2, anchor=tk.S, y=-10)

    add_button = ttk.Button(button_frame, text="Kitap Ekle", command=add_book)
    add_button.pack(side=tk.LEFT, padx=10)

    delete_button = ttk.Button(button_frame, text="Sil", command=delete_book, state="disabled")
    delete_button.pack(side=tk.LEFT, padx=10)

    lend_button = ttk.Button(button_frame, text="Ödünç Ver", command=lend_book, state="disabled")
    lend_button.pack(side=tk.LEFT, padx=10)

    return_button = ttk.Button(button_frame, text="İade et", command=return_book, state="disabled")
    return_button.pack(side=tk.LEFT, padx=10)

    # Call update_treeview at the start to highlight rows with today's return date
    update_treeview(df)
    
    root.mainloop()
    
except FileNotFoundError:
    print("Error: File not found.")
