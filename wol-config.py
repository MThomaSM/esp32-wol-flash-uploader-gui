import tkinter as tk
import tkinter.ttk as ttk
import json
import serial.tools.list_ports
import subprocess, sys


root = tk.Tk()
root.resizable(0,  0)
SIZE_X = 435
SIZE_Y = 290
root.title("ESP32 - WakeOnLan")

canvas = tk.Canvas(root, height=SIZE_Y, width=SIZE_X)
canvas.pack()
 

def MakeAndUploadFlash(uuid, wifiname, wifipassword, port):
    if (len(uuid) != 0 and len(wifiname) != 0 and len(wifipassword) != 0 and len(port) != 0):
        config = {"uuid": uuid, "wifi_name": wifiname, "wifi_password": wifipassword}
        with open('data/config.json', 'w') as outfile:
            json.dump(config, outfile)
        # -s 1507328 - veľkosť vysledneho image
        cmd = 'libs/mkspiffs.exe -c data -b 4096 -p 256 -s 1507328 spiffs.bin'
        # 0x00290000 - 2.5mb že image 1.5mb sa ma nahrať na adresu po 2.5mb čiže od 2.5mb do 4mb
        cmd_2 = 'libs/esptool.exe --chip esp32 --baud 921600 --port '+port+' --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x00290000 ./spiffs.bin'
        subprocess.Popen(cmd, close_fds=True) #If close_fds is true, all file descriptors except 0, 1 and 2 will be closed before the child process is executed. Otherwise when close_fds is false, file descriptors obey their inheritable flag as described in Inheritance of File Descriptors.
        subprocess.Popen(cmd_2, close_fds=True)


lblUuid = ttk.Label(root)
lblUuid.place(x=190, y=10, height=29, width=55)
lblUuid.configure(font="-family {Segoe UI} -size 14 -weight bold")
lblUuid.configure(relief="flat")
lblUuid.configure(anchor='w')
lblUuid.configure(justify='left')
lblUuid.configure(text='''UUID''')
lblUuid.configure(cursor="")


inputtUuid = ttk.Entry(root)
inputtUuid.place(x=190, y=40, relheight=0.076, relwidth=0.52)
inputtUuid.configure(font="-family {Segoe UI} -size 14")
inputtUuid.configure(takefocus="")
inputtUuid.configure(cursor="hand2")

lblWifiName = ttk.Label(root)
lblWifiName.place(x=190, y=80, height=29, width=116)
lblWifiName.configure(font="-family {Segoe UI} -size 14 -weight bold")
lblWifiName.configure(relief="flat")
lblWifiName.configure(anchor='w')
lblWifiName.configure(justify='left')
lblWifiName.configure(text='''Meno k WiFi''')

inputtWifiName = ttk.Entry(root)
inputtWifiName.place(x=190, y=110, relheight=0.076, relwidth=0.52)
inputtWifiName.configure(font="-family {Segoe UI} -size 14")
inputtWifiName.configure(takefocus="")
inputtWifiName.configure(cursor="hand2")

lblWifiPassword = ttk.Label(root)
lblWifiPassword.place(x=190, y=150, height=29, width=111)
lblWifiPassword.configure(font="-family {Segoe UI} -size 14 -weight bold")
lblWifiPassword.configure(relief="flat")
lblWifiPassword.configure(anchor='w')
lblWifiPassword.configure(justify='left')
lblWifiPassword.configure(text='''Heslo k Wifi''')

inputtWifiPassword = ttk.Entry(root)
inputtWifiPassword.place(x=190, y=180, relheight=0.076, relwidth=0.52)
inputtWifiPassword.configure(font="-family {Segoe UI} -size 14")
inputtWifiPassword.configure(takefocus="")
inputtWifiPassword.configure(cursor="hand2")

lblPorts = ttk.Label(root)
lblPorts.place(x=20, y=10, height=29, width=98)
lblPorts.configure(font="-family {Segoe UI} -size 14 -weight bold")
lblPorts.configure(relief="flat")
lblPorts.configure(anchor='w')
lblPorts.configure(justify='left')
lblPorts.configure(text='''Zariadenie''')

listPorts = tk.Listbox(root)
listPorts.place(x=20, y=40, height=164, width=154)
listPorts.configure(background="white")
listPorts.configure(disabledforeground="#a3a3a3")
listPorts.configure(font="-family {Courier New} -size 14")
listPorts.configure(foreground="#000000")
listPorts.configure(selectmode='SINGLE')
listPorts.configure(cursor="hand2")

i = 0
ports = serial.tools.list_ports.comports(include_links=False) #pridanie portov do zoznamu
for port in ports :
    if "COM" in port.device:
        i = i + 1
        listPorts.insert(i, port.device)

lblAd = ttk.Label(root)
lblAd.place(x=170, y=270, height=19, width=105)
lblAd.configure(font="TkDefaultFont")
lblAd.configure(relief="flat")
lblAd.configure(anchor='w')
lblAd.configure(justify='left')
lblAd.configure(text='''ESP32''')

btnSave = ttk.Button(root)
btnSave.place(x=20, y=220, height=45, width=400)
btnSave.configure(takefocus="")
btnSave.configure(text='''Uložiť''')
btnSave.configure(cursor="hand2")
btnSave.configure(command= lambda: MakeAndUploadFlash(inputtUuid.get(), inputtWifiName.get(), inputtWifiPassword.get(), listPorts.get(listPorts.curselection())))

root.mainloop()