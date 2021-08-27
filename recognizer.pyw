import cv2
import json
from datetime import date, datetime
from pathlib import Path
from tkinter import *
from tkinter import messagebox
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msgbox = Tk()
msgbox.withdraw()

p = open('user.json', 'r')
users = json.load(p)

names = []
roll=[]
dct = {}


for k, v in users.items():
    names.append(v['name'].split()[0])
    roll.append(k)

recognizer = cv2.face.FisherFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
# names = [ 'Nimish', 'Bhumi','Heramba']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

xyz=-1
ctr=0
while True:

    ret, img = cam.read()
    # img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )


    for (x, y, w, h) in faces:

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        id, confidence = recognizer.predict(cv2.resize(gray[y:y + h, x:x + w], (250, 250)), )


        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 600):

            if xyz==id:
                ctr+=1
            else :
                ctr=0
            xyz=id
            id = names[id]
            confidence = "  {0}%".format(round(confidence))
            print(ctr)

            if ctr>100:
                myfile = Path('./attendance/' + str(date.today()) + '.json')
                myfile.touch(exist_ok=True)
                try :
                    jsonf = open('./attendance/'+str(date.today())+'.json', 'r', encoding='utf-8')
                    jsonfcheck=json.load(jsonf)
                    if roll[xyz] not in jsonfcheck.keys():
                        jsonfcheck[roll[xyz]]=users[roll[xyz]]
                        jsonfcheck[roll[xyz]]['time'] = str(datetime.now())
                        jsonf = open('./attendance/'+str(date.today())+'.json', 'w', encoding='utf-8')
                        jsonf.write(json.dumps(jsonfcheck, indent=4))
                        jsonf.close()
                        f1 = open('./csv/' + str(date.today()) + '.csv', 'w')
                        print('Roll No,Name,Email,TimeStamp', file=f1)
                        for k, v in jsonfcheck.items():
                            print(k, jsonfcheck[k]['name'], jsonfcheck[k]['email'], jsonfcheck[k]['time'], sep=',', file=f1)
                        f1.close()
                        df_new = pd.read_csv('./csv/' + str(date.today()) + '.csv')
                        GFG = pd.ExcelWriter('./excel/' + str(date.today()) + '.xlsx')
                        df_new.to_excel(GFG, index=False)
                        GFG.save()
                        # instance of MIMEMultipart
                        msg = MIMEMultipart()

                        # storing the senders email address
                        msg['From'] = 'samant.nimish@gmail.com'

                        # storing the receivers email address
                        msg['To'] = jsonfcheck[roll[xyz]]['email']

                        # storing the subject
                        msg['Subject'] = "Attendance accepted"

                        # string to store the body of the mail
                        body = 'Your attendance has been marked for ' + str(jsonfcheck[roll[xyz]]['time'])

                        # attach the body with the msg instance
                        msg.attach(MIMEText(body, 'plain'))

                        # creates SMTP session
                        s = smtplib.SMTP('smtp.gmail.com', 587)

                        # start TLS for security
                        s.starttls()

                        # Authentication
                        s.login('samant.nimish@gmail.com', 'wmmcumuubicxieiq')

                        # Converts the Multipart msg into a string
                        text = msg.as_string()

                        # sending the mail
                        s.sendmail('samant.nimish@gmail.com', jsonfcheck[roll[xyz]]['email'], text)

                        # terminating the session
                        s.quit()
                        messagebox.showinfo('Attendance Confirmation', 'Attendace for '+jsonfcheck[roll[xyz]]['name']+' is taken')
                    else:
                        messagebox.showinfo('Attendance Confirmation', 'Attendace for '+jsonfcheck[roll[xyz]]['name']+' already taken')

                except json.decoder.JSONDecodeError:
                    dct[roll[xyz]] = users[roll[xyz]]
                    dct[roll[xyz]]['time'] = str(datetime.now())
                    jsonf = open('./attendance/' + str(date.today()) + '.json', 'w', encoding='utf-8')
                    jsonf.write(json.dumps(dct, indent=4))
                    jsonf.close()
                    f1 = open('./csv/' + str(date.today()) + '.csv', 'w')
                    print('Roll No,Name,Email,TimeStamp', file=f1)
                    print(roll[xyz], dct[roll[xyz]]['name'], dct[roll[xyz]]['email'], dct[roll[xyz]]['time'], sep=',', file=f1)
                    f1.close()
                    df_new = pd.read_csv('./csv/' + str(date.today()) + '.csv')
                    GFG = pd.ExcelWriter('./excel/' + str(date.today()) + '.xlsx')
                    df_new.to_excel(GFG, index=False)
                    GFG.save()
                    # instance of MIMEMultipart
                    msg = MIMEMultipart()

                    # storing the senders email address
                    msg['From'] = 'samant.nimish@gmail.com'

                    # storing the receivers email address
                    msg['To'] = dct[roll[xyz]]['email']

                    # storing the subject
                    msg['Subject'] = "Attendance accepted"

                    # string to store the body of the mail
                    body = 'Your attendance has been marked for ' + str(dct[roll[xyz]]['time'])

                    # attach the body with the msg instance
                    msg.attach(MIMEText(body, 'plain'))

                    # creates SMTP session
                    s = smtplib.SMTP('smtp.gmail.com', 587)

                    # start TLS for security
                    s.starttls()

                    # Authentication
                    s.login('samant.nimish@gmail.com', 'wmmcumuubicxieiq')

                    # Converts the Multipart msg into a string
                    text = msg.as_string()

                    # sending the mail
                    s.sendmail('samant.nimish@gmail.com', dct[roll[xyz]]['email'], text)

                    # terminating the session
                    s.quit()
                    messagebox.showinfo('Attendance Confirmation', 'Attendace for '+dct[roll[xyz]]['name']+' is taken')
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(confidence))

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")

cam.release()
cv2.destroyAllWindows()
