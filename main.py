import sqlite3 as sl
from tkinter import *
from tkinter import ttk
import os
from functools import partial


def connection():
    """
    This function allows the connection to the DB to perform SQL queries.
    :return: An object that allows SQL queries to the DB.
    """
    return sl.connect('computers.db')


def get_all_data():
    """
    This function perform a query to get all the date from a table.
    :return: All the form selected table.
    """
    db_data = connection()
    with db_data:
        return db_data.execute("SELECT * FROM computer")


def show_all():
    """This function will put in shape all the data from the DB and show it."""
    table_with_data = []
    data = get_all_data()
    for row in data:
        table_with_data.append(row)

    return table_with_data


def main_menu():
    for computer in computer_list:
        ttk.Label(frm, text=computer[0], padding=10).grid(column=1, row=computer[0])
        ttk.Label(frm, text=computer[1], padding=10).grid(column=2, row=computer[0])
        ttk.Label(frm, text=computer[2], padding=10).grid(column=3, row=computer[0])
        ttk.Label(frm, text=computer[3], padding=10).grid(column=4, row=computer[0])
        ttk.Button(frm, text=f"WAKE UP !", command=partial(do_wol, computer[3], computer[1])).grid(column=5,
                                                                                                   row=computer[0])


def ping(address):
    return os.system(f"ping -c 1 -t100 {address}")


def is_alive():
    for computer in computer_list:
        if ping(computer[2]) == 0:
            ttk.Label(frm, text="UP", padding=10).grid(column=0, row=computer[0])
        else:
            ttk.Label(frm, text="DOWN", padding=10).grid(column=0, row=computer[0])
    root.after(3000, is_alive)  # every second...


def do_wol(mac, name):
    if os.system(f"wol {mac}") == 0:
        message_box.configure(text=f"Wake packet send to {name}.")
    else:
        message_box.configure(text=f"Could not send packet to {name}.")


def default_message():
    ttk.Label(frm, text="Click on the wake up button to wake up a computer.", padding=10).grid(
        row=(len(computer_list) + 1), columnspan=6)


if __name__ == '__main__':
    computer_list = show_all()
    root = Tk()
    root.title("Wake On Lan")
    frm = ttk.Frame(root, padding=30)
    frm.grid()
    ttk.Label(frm, text="Wake On Lan", padding=10).grid(column=0, row=0, columnspan=6)
    is_alive()
    main_menu()
    message_box = ttk.Label(frm, text="Click on the wake up button to wake up a computer.", padding=10)
    message_box.grid(row=(len(computer_list) + 1), columnspan=6)

    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=5, row=(len(computer_list) + 2))

    root.mainloop()
