# import module from tkinter for UI
from tkinter import *
import os
from datetime import datetime
import json
from datetime import date

# creating instance of TK
root = Tk()
root.configure(background="white")

p = open('user.json', 'rb')
users = json.load(p)

def function1():
    global f, e1, e2
    f = Tk()

    l1 = Label(f, text='Employee Code / Roll No : ', width=23, height=2)

    e1 = Entry(f, width=40)

    l2 = Label(f, text='Name : ', width=23, height=2)
    e2 = Entry(f, width=40)

    b = Button(f, text='Submit', width=15, height=2, command=takephoto, bg='blue', fg='white',
               activebackground='green', activeforeground='red')

    l1.grid(row=0, column=0)
    e1.grid(row=0, column=1)
    l2.grid(row=1, column=0)
    e2.grid(row=1, column=1)
    b.grid(row=2, column=0)

    f.mainloop()


def takephoto():
    userid = e1.get().strip()
    print(len(users))
    x = users.get(userid, len(users))
    users[userid] = {'id': x['id'],
                     'name': e2.get()}
    print(x, users, sep='\n')
    f.destroy()
    os.system("py 01_face_dataset.py " + str(users[userid]['id']))
    with open('user.json', 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(users, indent=4))

def function2():
    os.system("py training_dataset.py")


def function3():
    os.system("py recognizer.py")


def function5():
    os.startfile(os.getcwd() + "/developers/diet1frame1first.html");


def function6():
    root.destroy()


def attend():
    os.startfile(os.getcwd() + "/firebase/attendance_files/attendance" + str(datetime.now().date()) + '.xls')


# stting title for the window
root.title("AUTOMATIC ATTENDANCE MANAGEMENT USING FACE RECOGNITION")

# creating a text label
Label(root, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=("times new roman", 20), fg="white", bg="maroon",
      height=2).grid(row=0, rowspan=2, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)

# creating first button
Button(root, text="Create Dataset", font=("times new roman", 20), bg="#0D47A1", fg='white', command=function1).grid(
    row=3, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)

# creating second button
Button(root, text="Train Dataset", font=("times new roman", 20), bg="#0D47A1", fg='white', command=function2).grid(
    row=4, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)

# creating third button
Button(root, text="Recognize + Attendance", font=('times new roman', 20), bg="#0D47A1", fg="white",
       command=function3).grid(row=5, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)

# creating attendance button
Button(root, text="Attendance Sheet", font=('times new roman', 20), bg="#0D47A1", fg="white", command=attend).grid(
    row=6, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)

Button(root, text="Developers", font=('times new roman', 20), bg="#0D47A1", fg="white", command=function5).grid(row=8,
                                                                                                                columnspan=2,
                                                                                                                sticky=N + E + W + S,
                                                                                                                padx=5,
                                                                                                                pady=5)

Button(root, text="Exit", font=('times new roman', 20), bg="maroon", fg="white", command=function6).grid(row=9,
                                                                                                         columnspan=2,
                                                                                                         sticky=N + E + W + S,
                                                                                                         padx=5, pady=5)

root.mainloop()
