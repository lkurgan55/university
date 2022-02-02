import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from hashlib import md5

USERS = {'admin': ''}

if os.path.isfile('database.json'):
    with open('database.json', 'r') as fp:
        USERS = json.load(fp)
        print(USERS)
else:
    with open('database.json', 'w') as fp:
        json.dump(USERS, fp)


class User():
    def __init__(self, login):
        pass

    def change_pass(self):
        pass

def check_user(login, password):
    login = login.get()
    password = md5(password.get().encode()).hexdigest()
    if (login in USERS.keys()):
            if (USERS[login] == password or USERS[login] == ""):
                messagebox.showinfo("Good", f"You have signed in by'{login}'")
            else:
                messagebox.showerror("Error", "Wrong password")
    else:
        messagebox.showerror("Error", "Login doesn`t exist")
    print(login, password)

def register_user(login2, password1, password2):
    login = login2.get()
    password = md5(password1.get().encode()).hexdigest()
    password_repeat = md5(password2.get().encode()).hexdigest()
    
    print(login, password, password_repeat)

    if (password == password_repeat):
        if (login not in USERS.keys()):
            USERS[login] = password
            with open('database.json', 'w') as fp:
                json.dump(USERS, fp)
            messagebox.showinfo("Good", f"'{login}' was added to database")
        else:
            messagebox.showerror("Error", "Login already exists")
    else:
        messagebox.showerror("Error", "Passwords are different")


def login_window(root):
    
    root.title('login')
    root.geometry('400x500')    
    
    login = tk.StringVar()
    tk.Label(root, text='Sign in').pack()
    login_label = ttk.Label(root, text="login:")
    login_label.pack(pady=10)
    login_entry = ttk.Entry(root, width=25, textvariable=login)
    login_entry.pack()
    login_entry.focus()
    
    password = tk.StringVar()
    password_label = ttk.Label(root, text="password:")
    password_label.pack(pady=10)
    password_entry = ttk.Entry(root, width=25, textvariable=password, show="*")
    password_entry.pack()

    

    login_button = ttk.Button(root, text="Login", command=lambda: check_user(login, password))
    login_button.pack(pady=10)

    login2 = tk.StringVar()
    tk.Label(root, text='Sign up').pack(pady=(20,0))
    login2_label = ttk.Label(root, text="login:")
    login2_label.pack(pady=10)
    login2_entry = ttk.Entry(root, width=25, textvariable=login2)
    login2_entry.pack()
    login2_entry.focus()
    
    password1 = tk.StringVar()
    password1_label = ttk.Label(root, text="password:")
    password1_label.pack(pady=10)
    password1_entry = ttk.Entry(root, width=25, textvariable=password1, show="*")
    password1_entry.pack()

    password2 = tk.StringVar()
    password2_label = ttk.Label(root, text="repeat password:")
    password2_label.pack(pady=10)
    password2_entry = ttk.Entry(root, width=25, textvariable=password2, show="*")
    password2_entry.pack()

    login_button = ttk.Button(root, text="register", command=lambda: register_user(login2, password1, password2))
    login_button.pack(pady=10)

    



root = tk.Tk()

login_window(root)

root.mainloop()

