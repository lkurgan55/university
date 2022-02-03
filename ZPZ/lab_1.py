import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from hashlib import md5

USERS = {'admin': ['', 0, False]} # структура - (пароль, спроби входу, бан)

if os.path.isfile('database.json'):
    with open('database.json', 'r') as fp:
        USERS = json.load(fp)
        print(USERS)
else:
    with open('database.json', 'w') as fp:
        json.dump(USERS, fp)


class User():
    def __init__(self, login):
        self.login = login

    def first_start(self, root): # перший запуск
        clear_window(root)
        root.title('First login')
        tk.Label(root, text=f'You are "{self.login}"').pack()
 
        tk.Label(root, text='Create password').pack(pady=(20,0))
        
        password1 = tk.StringVar()
        password1_label = ttk.Label(root, text=" password:")
        password1_label.pack(pady=10)
        password1_entry = ttk.Entry(root, width=25, textvariable=password1, show="*")
        password1_entry.pack()

        password2 = tk.StringVar()
        password2_label = ttk.Label(root, text="repeat password:")
        password2_label.pack(pady=10)
        password2_entry = ttk.Entry(root, width=25, textvariable=password2, show="*")
        password2_entry.pack()

        login_button = ttk.Button(root, text="Create", width=25, command=lambda: self.create_password(self.login, password1, password2))
        login_button.pack(pady=10) 

        login_button = ttk.Button(root, text="Exit", width=25, command=lambda: exit(root))
        login_button.pack(pady=10)

    def create_password(self, login, password1, password2):
        
        password1 = md5(password1.get().encode()).hexdigest()
        password2 = md5(password2.get().encode()).hexdigest()
        
        if password1 == password2:
            USERS[login][0] = password1
            with open('database.json', 'w') as fp:
                json.dump(USERS, fp)
            messagebox.showinfo("Good", f"You have created password for '{login}'")
            self.menu(root)
        else:
            messagebox.showerror("Error", "Passwords are different")

        print(login, password1)

    def change_my_password(self, root):
        clear_window(root)
        root.title('Change password')

        old_pass = tk.StringVar()
        tk.Label(root, text='Change my password').pack(pady=(20,0))
        old_pass_label = ttk.Label(root, text="old password:")
        old_pass_label.pack(pady=10)
        old_pass_entry = ttk.Entry(root, width=25, textvariable=old_pass, show="*")
        old_pass_entry.pack()
        old_pass_entry.focus()
        
        password1 = tk.StringVar()
        password1_label = ttk.Label(root, text="new password:")
        password1_label.pack(pady=10)
        password1_entry = ttk.Entry(root, width=25, textvariable=password1, show="*")
        password1_entry.pack()

        password2 = tk.StringVar()
        password2_label = ttk.Label(root, text="repeat new password:")
        password2_label.pack(pady=10)
        password2_entry = ttk.Entry(root, width=25, textvariable=password2, show="*")
        password2_entry.pack()

        login_button = ttk.Button(root, text="Change my password", width=25, command=lambda: self.change_password(old_pass, password1, password2))
        login_button.pack(pady=10)

        login_button = ttk.Button(root, text="Back to menu", width=25, command=lambda: self.menu(root))
        login_button.pack(pady=10)

    def change_password(self, old_pass, password1, password2):
        old_pass = md5(old_pass.get().encode()).hexdigest()
        password1 = md5(password1.get().encode()).hexdigest()
        password2 = md5(password2.get().encode()).hexdigest()
        
        if (USERS[self.login][0] == old_pass or USERS[self.login][0] == ""):
            if password1 == password2:
                USERS[self.login][0] = password1
                with open('database.json', 'w') as fp:
                    json.dump(USERS, fp)
                messagebox.showinfo("Good", f"You have changed password for '{self.login}'")
            else:
                messagebox.showerror("Error", "Passwords are different")
        else:
            messagebox.showerror("Error", "Wrong old password")

        print(self.login, password1)    

    def menu(self, root):
        clear_window(root)
        root.title('Menu')
        tk.Label(root, text=f'You are "{self.login}"').pack()
        
        login_button = ttk.Button(root, text="Change my password", width=25, command=lambda: self.change_my_password(root))
        login_button.pack(pady=10) 

        login_button = ttk.Button(root, text="Exit", width=25, command=lambda: exit(root))
        login_button.pack(pady=10)        

class Admin(User):
    def menu(self, root):
        clear_window(root)
        root.title('ADMIN')
        tk.Label(root, text=f'You are "{self.login}"').pack()
        
        login_button = ttk.Button(root, text="change my password", width=25, command=lambda: self.change_my_password(root))
        login_button.pack(pady=10)

        login_button = ttk.Button(root, text="User list", width=25, command=lambda: print())
        login_button.pack(pady=10)

        login_button = ttk.Button(root, text="Register an User", width=25, command=lambda: self.register(root))
        login_button.pack(pady=10)

        login_button = ttk.Button(root, text="Ban an User", width=25, command=lambda: print())
        login_button.pack(pady=10)

        login_button = ttk.Button(root, text="password settings", width=25, command=lambda: print())
        login_button.pack(pady=10)     

        login_button = ttk.Button(root, text="Exit", width=25, command=lambda: exit(root))
        login_button.pack(pady=10)

    def register(self, root):
        clear_window(root)
        root.title('ADMIN')
        tk.Label(root, text=f'Registration new User').pack()
    
        login = tk.StringVar()
        login_label = ttk.Label(root, text="login:")
        login_label.pack(pady=10)
        login_entry = ttk.Entry(root, width=25, textvariable=login)
        login_entry.pack()
        login_entry.focus()

        login_button = ttk.Button(root, text="register", width=25, command=lambda: register_user(login))
        login_button.pack(pady=10)

        login_button = ttk.Button(root, text="Back to menu", width=25, command=lambda: self.menu(root))
        login_button.pack(pady=10)                

def exit(root):
    clear_window(root)
    login_window(root)

def register_user(login):
    login = login.get()
    password = ''
    
    print(login, password)
    
    if (login not in USERS.keys()):
        USERS[login] = (password, 0, False)
        with open('database.json', 'w') as fp:
            json.dump(USERS, fp)
        messagebox.showinfo("Good", f"'{login}' was added to database")
    else:
        messagebox.showerror("Error", "Login already exists")

def change_pass(login, old_pass, password1, password2):
    old_pass = md5(old_pass.get().encode()).hexdigest()
    password1 = md5(password1.get().encode()).hexdigest()
    password2 = md5(password2.get().encode()).hexdigest()
    if login in USERS.keys():
            if (USERS[login][0] == old_pass or USERS[login][0] == ""):
                if password1 == password2:
                    USERS[login][0] = password1
                    with open('database.json', 'w') as fp:
                        json.dump(USERS, fp)
                    messagebox.showinfo("Good", f"You have changed password for '{login}'")
                else:
                    messagebox.showerror("Error", "Passwords are different")
            else:
                messagebox.showerror("Error", "Wrong old password")
    else:
        messagebox.showerror("Error", "Login doesn`t exist")
    print(login, password1)

def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def check_user(login, password):
    login = login.get()
    password = md5(password.get().encode()).hexdigest()
    if login in USERS.keys():
            if USERS[login][0] == password:
                #messagebox.showinfo("Good", f"You have signed in by'{login}'")
                #clear_window(root)
                if login == 'admin':
                    USER = Admin(login)
                else: USER = User(login)
                USER.menu(root)
            elif USERS[login][0] == "":
                if login == 'admin':
                    USER = Admin(login)
                else: USER = User(login)
                USER.first_start(root) 
            else:
                messagebox.showerror("Error", "Wrong password")
    else:
        messagebox.showerror("Error", "Login doesn`t exist")
    print(login, password)
    

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

    login_button = ttk.Button(root, text="Login", width=25, command=lambda: check_user(login, password))
    login_button.pack(pady=10)


    



root = tk.Tk()
login_window(root)

root.mainloop()

