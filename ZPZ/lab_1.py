import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

USERS = {'admin': ['', 0, False], 'settings': ['',[True, True, True], True]} # структура - (пароль, спроби входу, бан)

# загрузка даних з файлу, або створення
if os.path.isfile('database.json'):
    with open('database.json', 'r') as fp:
        USERS = json.load(fp)
        #print(USERS)
else:
    with open('database.json', 'w') as fp:
        json.dump(USERS, fp)


class User():
    def __init__(self, login):
        self.login = login

    def reset_attempts(self): 
        USERS[self.login][1] = 0
        with open('database.json', 'w') as fp:
            json.dump(USERS, fp)


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

        button = ttk.Button(root, text="Create", width=25, command=lambda: self.create_password(self.login, password1, password2))
        button.pack(pady=10) 

        button = ttk.Button(root, text="Exit", width=25, command=lambda: exit(root))
        button.pack(pady=10)

    def create_password(self, login, password1, password2):
        
        password1 = password1.get()
        password2 = password2.get()
        
        if password1 == password2:
            
            result = check_password(password1) # перевірка пароля згідно опцій

            if result[0] & result[1] & result[2]:
                USERS[login][0] = password1
                with open('database.json', 'w') as fp:
                    json.dump(USERS, fp)
                messagebox.showinfo("Good", f"You have created password for '{login}'")
                self.menu(root)
            else:
                if not result[0]: result[0] = 'lowercase letters'
                else: result[0] = ''
                if not result[1]: result[1] = 'Uppercase letters'
                else: result[1] = ''
                if not result[2]: result[2] = 'Digits'
                else: result[2] = ''
                error = f'Password has to contains {result[0]} {result[1]} {result[2]}'
                messagebox.showerror("Error", error)
        else:
            messagebox.showerror("Error", "Passwords are different")

        #print(login, password1)

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

        button = ttk.Button(root, text="Change my password", width=25, command=lambda: self.change_password(old_pass, password1, password2))
        button.pack(pady=10)

        button = ttk.Button(root, text="Back to menu", width=25, command=lambda: self.menu(root))
        button.pack(pady=10)

    def change_password(self, old_pass, password1, password2):
        old_pass = old_pass.get()
        password1 = password1.get()
        password2 = password2.get()
        
        if (USERS[self.login][0] == old_pass or USERS[self.login][0] == ""):
            if password1 == password2:

                result = check_password(password1)

                if result[0] & result[1] & result[2]:
                    USERS[self.login][0] = password1
                    with open('database.json', 'w') as fp:
                        json.dump(USERS, fp)
                    messagebox.showinfo("Good", f"You have changed password for '{self.login}'")
                else:
                    if not result[0]: result[0] = 'lowercase letters'
                    else: result[0] = ''
                    if not result[1]: result[1] = 'Uppercase letters'
                    else: result[1] = ''
                    if not result[2]: result[2] = 'Digits'
                    else: result[2] = ''
                    error = f'Password has to contains {result[0]} {result[1]} {result[2]}'
                    messagebox.showerror("Error", error)
            else:
                messagebox.showerror("Error", "Passwords are different")
        else:
            messagebox.showerror("Error", "Wrong old password")

        #print(self.login, password1)    

    def menu(self, root):
        clear_window(root)
        self.reset_attempts() # скидання спроб неправильного пароля, при вдалому вході
        root.title('Menu')
        tk.Label(root, text=f'You are "{self.login}"').pack()
        
        button = ttk.Button(root, text="Change my password", width=25, command=lambda: self.change_my_password(root))
        button.pack(pady=10) 

        button = ttk.Button(root, text="Exit", width=25, command=lambda: exit(root))
        button.pack(pady=10)        

class Admin(User):
    def menu(self, root):
        clear_window(root)
        root.title('ADMIN')
        tk.Label(root, text=f'You are "{self.login}"').pack()
        
        button = ttk.Button(root, text="change my password", width=25, command=lambda: self.change_my_password(root))
        button.pack(pady=10)

        button = ttk.Button(root, text="User list", width=25, command=lambda: self.get_user_list(root))
        button.pack(pady=10)

        button = ttk.Button(root, text="Register an User", width=25, command=lambda: self.register(root))
        button.pack(pady=10)

        button = ttk.Button(root, text="Ban an User", width=25, command=lambda: self.ban_user(root))
        button.pack(pady=10)

        button = ttk.Button(root, text="password settings", width=25, command=lambda: self.pass_settings(root))
        button.pack(pady=10)     

        button = ttk.Button(root, text="Exit", width=25, command=lambda: exit(root))
        button.pack(pady=10)

    def pass_settings(self, root):
        clear_window(root)
        root.title('ADMIN')
        tk.Label(root, text=f'Password settings').pack()

        var1 = tk.BooleanVar()
        var2 = tk.BooleanVar()
        var3 = tk.BooleanVar()

        def change_settings(var, index):
            var = var.get()
            USERS['settings'][1][index] = var
            with open('database.json', 'w') as fp:
                    json.dump(USERS, fp)

        checkbutton1 = tk.Checkbutton(root, text='Lowercase letters',variable=var1, onvalue=True, offvalue=False, command=lambda: change_settings(var1, 0))
        checkbutton1.pack()
        
        checkbutton2 = tk.Checkbutton(root, text='Uppercase letters',variable=var2, onvalue=True, offvalue=False, command=lambda: change_settings(var2, 1))
        checkbutton2.pack()

        checkbutton3 = tk.Checkbutton(root, text='Digits',variable=var3, onvalue=True, offvalue=False, command=lambda: change_settings(var3, 2))
        checkbutton3.pack()

        if USERS['settings'][1][0]: 
            checkbutton1.select()
        else: checkbutton1.deselect()

        if USERS['settings'][1][1]: 
            checkbutton2.select()
        else: checkbutton2.deselect()

        if USERS['settings'][1][2]: 
            checkbutton3.select()
        else: checkbutton3.deselect()

        button = ttk.Button(root, text="Back to menu", width=25, command=lambda: self.menu(root))
        button.pack(pady=10)

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

        button = ttk.Button(root, text="register", width=25, command=lambda: self.register_user(login))
        button.pack(pady=10)

        button = ttk.Button(root, text="Back to menu", width=25, command=lambda: self.menu(root))
        button.pack(pady=10)
    
    def register_user(self, login):
        login = login.get()
        password = ''
        
        #print(login, password)
        
        if (login not in USERS.keys()):
            USERS[login] = [password, 0, False]
            with open('database.json', 'w') as fp:
                json.dump(USERS, fp)
            messagebox.showinfo("Good", f"'{login}' was added to database")
        else:
            messagebox.showerror("Error", "Login already exists")

    def get_user_list(self, root):
        clear_window(root)
        root.title('ADMIN')
        tk.Label(root, text=f'User list').pack()

        table = ttk.Treeview(root)
        table['columns'] = ('Login', 'Password', 'Blocked')

        table.column("#0", width=0,  stretch='no')
        table.heading("#0",text="")

        table.column("Login", anchor='center', width=140)
        table.heading("Login",text="Login", anchor='center')

        table.column("Password", anchor='center', width=140)
        table.heading("Password",text="Password", anchor='center')

        table.column("Blocked", anchor='center', width=140)
        table.heading("Blocked",text="Blocked", anchor='center')
        i = 0
        for login in USERS.keys():
            if login == "settings": continue
            table.insert(parent='',index='end',iid=i,text='', values=(login,USERS[login][0],USERS[login][2]))
            i +=1
        table.pack()

        login_button = ttk.Button(root, text="Back to menu", width=25, command=lambda: self.menu(root))
        login_button.pack(pady=10)

    def ban_user(self, root):
        clear_window(root)
        root.title('ADMIN')
        tk.Label(root, text=f'Ban User').pack()

        login = tk.StringVar()
        login_label = ttk.Label(root, text="login:")
        login_label.pack(pady=10)
        login_entry = ttk.Entry(root, width=25, textvariable=login)
        login_entry.pack()
        login_entry.focus()

        button = ttk.Button(root, text="Ban", width=25, command=lambda: self.ban(login, True))
        button.pack(pady=10)
        
        button = ttk.Button(root, text="UnBan", width=25, command=lambda: self.ban(login, False))
        button.pack(pady=10)

        button = ttk.Button(root, text="Back to menu", width=25, command=lambda: self.menu(root))
        button.pack(pady=10)
    
    def ban(self, login, type):
        login = login.get()
        if (login in USERS.keys()):
            USERS[login][2] = type
            with open('database.json', 'w') as fp:
                json.dump(USERS, fp)
            if type: messagebox.showinfo("Good", f"'{login}' was banned")
            else:
                #print('kek')
                USERS[login][1] = 0
                with open('database.json', 'w') as fp:
                    json.dump(USERS, fp)
                messagebox.showinfo("Good", f"'{login}' was unbanned")
        else:
            messagebox.showerror("Error", "Login not found")

def exit(root): # виход з аккаунту
    clear_window(root)
    login_window(root)

def clear_window(root): # очищення вікна від елементів
    for widget in root.winfo_children():
        widget.destroy()

def check_password(password):
    result = [True, True, True]

    if USERS['settings'][1][0]:
        if re.search('[a-z]', password) == None:
            result[0] =  False

    if USERS['settings'][1][1]:
        if re.search('[A-Z]', password) == None:
            result[1] =  False

    if USERS['settings'][1][2]:
        if re.search('[0-9]', password) == None:
            result[2] =  False

    return result

def check_user(login, password):
    login = login.get()
    password = password.get()
    if login in USERS.keys():
            if USERS[login][2]:
                messagebox.showerror("Error", "This login is banned")
            elif USERS[login][0] == "":
                #messagebox.showinfo("Good", f"You have signed in by'{login}'")
                #clear_window(root)
                if login == 'admin':
                    USER = Admin(login)
                else: USER = User(login)
                USER.first_start(root) 
                
            elif USERS[login][0] == password:
                if login == 'admin':
                    USER = Admin(login)
                else: USER = User(login)
                USER.menu(root)
            else:
                if login != 'admin':
                    if USERS[login][1] >= 3:
                        USERS[login][2] = True
                        messagebox.showerror("Error", "Accout has been banned!")
                    else:
                        USERS[login][1] += 1
                        with open('database.json', 'w') as fp:
                            json.dump(USERS, fp)
                        messagebox.showerror("Error", f"Wrong password, Attemps:{3 - USERS[login][1]}")
                else:
                    messagebox.showerror("Error", "Wrong password")
    else:
        messagebox.showerror("Error", "Login doesn`t exist")
    #print(login, password)

def show_info(root): # довідка
    clear_window(root)
    root.title('Info')
    tk.Label(root, text=f'This program was created by Leonid Kurgan').pack()    
    tk.Label(root, text=f'Variant - 8').pack()    
    tk.Label(root, text=f'My Telegram: @l_kurgan').pack()    
    tk.Label(root, text=f'My instagram: @l_kurgan').pack()

    button = ttk.Button(root, text="Back to login", width=25, command=lambda: exit(root))
    button.pack(pady=10)     

def login_window(root):
    
    root.title('login')
    root.geometry('500x500')    
    
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

    button = ttk.Button(root, text="Login", width=25, command=lambda: check_user(login, password))
    button.pack(pady=10)
    button = ttk.Button(root, text="Info", width=25, command=lambda: show_info(root))
    button.pack(pady=40)

root = tk.Tk()
login_window(root)

root.mainloop()