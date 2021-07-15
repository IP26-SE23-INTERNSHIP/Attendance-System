# import module from tkinter for UI
from tkinter import *
from tkinter import messagebox
import os
import json
import webbrowser
import subprocess
import threading

global p


def serve():
    global p
    p = subprocess.Popen('start /wait py -m http.server 7800', shell=True)


def closeconnec():
    global p
    print(p.pid)
    os.system('netstat -ano | findstr :7800')
    # os.system('taskkill /PID '+str(p.pid)+' /F')
    subprocess.call('taskkill /F /T /PID %i' % p.pid)


def hellocallback():
    if e4.get() == 'pass':
        takephoto()
    else:
        messagebox.showerror('Error', 'Invalid Login')


# creating instance of TK
root = Tk()
root.configure(background="white")

p = open('user.json', 'rb')
try:
    users = json.load(p)
except:
    users={}
    pass

def function1():
    global f, e1, e2, e3, e4
    f = Tk()

    l1 = Label(f, text='Employee Code / Roll No : ', width=23, height=2)
    e1 = Entry(f, width=40)

    l2 = Label(f, text='Name : ', width=23, height=2)
    e2 = Entry(f, width=40)

    l3 = Label(f, text='Email id : ', width=23, height=2)
    e3 = Entry(f, width=40)

    l4 = Label(f, text='Password : ', width=23, height=2)
    e4 = Entry(f, width=40, show='*')

    b = Button(f, text='Submit', width=15, height=2, command=hellocallback, bg='blue', fg='white',
               activebackground='green', activeforeground='red')

    l1.grid(row=0, column=0)
    e1.grid(row=0, column=1)
    l2.grid(row=1, column=0)
    e2.grid(row=1, column=1)
    l3.grid(row=2, column=0)
    e3.grid(row=2, column=1)
    l4.grid(row=3, column=0)
    e4.grid(row=3, column=1)
    b.grid(row=4, column=0)

    f.mainloop()


def takephoto():
    userid = e1.get().strip()
    role = 1
    if userid.isnumeric():
        role = 0
    print(len(users))
    x = users.get(userid, {'id': len(users)})
    users[userid] = {'id': x['id'], \
                     'name': e2.get(), \
                     'email': e3.get(), \
                     'role': role}
    print(x, users, sep='\n')
    f.destroy()
    os.system("py training.py " + str(x['id']))
    with open('user.json', 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(users, indent=4))


def function3():
    os.system("py recognizer.py")


def function6():
    root.destroy()
    closeconnec()


def attend():
    # os.system("python custom_server.py 1")
    t = threading.Thread(target=serve)
    t.start()
    webbrowser.open('http://localhost:7800/attendance.html')


# stting title for the window
root.title("AUTOMATIC ATTENDANCE MANAGEMENT USING FACE RECOGNITION")

# creating a text label
Label(root, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=("times new roman", 20), fg="white", bg="maroon",
      height=2).grid(row=0, rowspan=2, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)

# creating first button
Button(root, text="Create Dataset", font=("times new roman", 20), bg="#0D47A1", fg='white', command=function1).grid(
    row=3, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)

# creating third button
Button(root, text="Recognize + Attendance", font=('times new roman', 20), bg="#0D47A1", fg="white",
       command=function3).grid(row=5, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)

# creating attendance button
Button(root, text="Attendance Download Website", font=('times new roman', 20), bg="#0D47A1", fg="white", command=attend).grid(
    row=6, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)

Button(root, text="Exit", font=('times new roman', 20), bg="maroon", fg="white", command=function6).grid(row=9,
                                                                                                         columnspan=2,
                                                                                                         sticky=N + E + W + S,
                                                                                                         padx=5, pady=5)

root.mainloop()
