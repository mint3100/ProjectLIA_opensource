import tkinter as tk
from tkinter import ttk
import sqlite3

# Level System Data Checker
# Created : 23.12.31
# Modified : 24.09.11

def show_data():
    conn = sqlite3.connect('level.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()


    for row in treeview.get_children():
        treeview.delete(row)
    for row in rows:
        treeview.insert('', 'end', values=row[0:])
    conn.close()

root = tk.Tk()
root.title("LIA Data Checker V1.0")

treeview = ttk.Treeview(root, columns=('Column 1', 'Column 2', 'Column 3'))
treeview.heading('#1', text='Column 1')
treeview.heading('#2', text='Column 2')
treeview.heading('#3', text='Column 3')
treeview.pack()

show_button = tk.Button(root, text="데이터 조회", command=show_data)
show_button.pack()

root.mainloop()
