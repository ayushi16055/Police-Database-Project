# missing person identification and database system

import random
import tkinter as tk
import smtplib
import PIL
from PIL import ImageTk
from tkinter.font import Font
from tkinter.messagebox import _show
import imghdr
from tkinter import *
from tkinter.filedialog import askopenfile
import os
import face_recognition
import cv2
import numpy as np
from csv import reader, writer
import os
from tkcalendar import Calendar, DateEntry
from tktimepicker import AnalogPicker, AnalogThemes, constants
from datetime import date

#main window
welcome = tk.Tk()

#authentication details
f=open('passwords.csv','r')
pw=reader(f)
user_pass=[]
for i in pw:
    user_pass.append(i)
user_pass.pop(0)
f.close()
registered_email = []
for i in user_pass:
    registered_email.append(i[-1])
sixdig_pass = str(random.randint(100000, 999999))

#creating variables
filepath = ''
found = False
newpath=""
MPINid=""
details=[]
searchid=""
ids=""
sc2 = ""
sc4=""
cal1=''
udate=''
time1=''
timelabel=''

#main functions
def person_found():
    global details
    sc3 = tk.Tk()
    sc3=tk.Toplevel()
    sc3.title("Details of person")
    sc3.geometry('888x584')
    sc3.configure(background='#F0F8FF')
    sc3.attributes('-topmost', True)

    heading = Font(
    family='Times New Roman',
    size=15,
    weight='bold',
    ) 
    text = Font(
    family='Times New Roman',
    size=14,
    weight='normal'
    )
    
    tk.Label(sc3, text="MPIN ID:", bg='#F0F8FF', font=(heading)).place(x=300, y=300)
    tk.Label(sc3, text=details[0], bg='#F0F8FF', font=(text)).place(x=500, y=300)
    tk.Label(sc3, text="Name:", bg='#F0F8FF', font=(heading)).place(x=300, y=330)
    tk.Label(sc3, text=details[1], bg='#F0F8FF', font=(text)).place(x=500, y=330)
    tk.Label(sc3, text="Last Seen(Time/Date):", bg='#F0F8FF', font=(heading)).place(x=300, y=360)
    tk.Label(sc3, text=details[2], bg='#F0F8FF', font=(text)).place(x=500, y=360)
    tk.Label(sc3, text="Last Seen(Place):", bg='#F0F8FF', font=(heading)).place(x=300, y=390)
    tk.Label(sc3, text=details[3], bg='#F0F8FF', font=(text)).place(x=500, y=390)
    tk.Label(sc3, text="Point of Contact:", bg='#F0F8FF', font=(heading)).place(x=300, y=420)
    tk.Label(sc3, text=details[4], bg='#F0F8FF', font=(text)).place(x=500, y=420)
    tk.Label(sc3, text="Additional Information:", bg='#F0F8FF', font=(heading)).place(x=300, y=450)
    tk.Label(sc3, text=details[5], bg='#F0F8FF', font=(text)).place(x=500, y=450)

    #load image of person
    img = PIL.Image.open(details[6])
    img.thumbnail((300, 250))
    height=img.height
    width=img.width
    img.save("imgresized.gif")
    imgcanvas= tk.Canvas(sc3, height=height, width=width)
    picture_file = tk.PhotoImage(file = 'imgresized.gif')
    imgcanvas.create_image(0, 0, anchor=NW, image=picture_file)
    imgcanvas.place(x=310, y=29)

    sc3.mainloop()


# image search
def img_search():
    root.attributes('-topmost', True)
    global sc2
    global filepath
    global details
    global found
    found = False
    uimg = face_recognition.load_image_file(filepath)
    try: u_encoding = face_recognition.face_encodings(uimg)[0]
    except IndexError:
        _show('ERROR.', 'NO FACE IDENTIFIED IN PICTURE')
    # open database
    f = open("policedatabase.csv", "r")
    rr = reader(f)
    # need to exclude headers while checking
    MPIN = 0
    for i in rr:
        if i!=[] and i[0] == 'MPIN':
            continue
        elif i!=[]:
            path = i[6]
            cimg = face_recognition.load_image_file(path)
            try:
                c_encoding = face_recognition.face_encodings(cimg)[0]
                result = face_recognition.compare_faces([c_encoding], u_encoding)
                # output of result is [boolean]
                if True in result:
                    root.attributes('-topmost', False)
                    found = True
                    MPIN = i[0]
                    details=i
                    break
            except IndexError:
                continue
    f.close()
    if found==True:
        person_found()
        #root.destroy()
    if found==False:
        _show('Search complete','Person not found in database')


def upload_search():
    uw = tk.Tk()
    uw.lift()
    uw.geometry("700x350")
    tk.Label(root, text="loading", bg='#F0F8FF', font=('arial', 15, 'normal')).pack()

    def open_file():
        global filepath, root
        file = tk.filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*')])
        if file:
            filepath = str(os.path.abspath(file.name))
            uw.destroy()
            tk.Label(root, text="hold on, searching", bg='#F0F8FF', font=('arial', 15, 'normal')).pack()
            img_search()


    l2 = tk.Label(uw, text="Upload picture", font=('Georgia 13'))
    l2.pack(pady=10)
    tk.Button(uw, text="Browse", command=open_file).pack(pady=20)
    uw.mainloop()
    


def camera_search():
    global filepath, root
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if not ret:
            _show('Error','Unable to capture image')
            break
        cv2.imshow("Capture an image", frame)

        key = cv2.waitKey(1)
        if key % 256 == 27:
            tk.Label(root, text="closed successfully", bg='#F0F8FF', font=('arial', 15, 'normal')).pack()
            # ESC pressed, closes the window--dont destroy previous window, overwrite it
            break
        elif key % 256 == 32:
            tk.Label(root, text="loading", bg='#F0F8FF', font=('arial', 15, 'normal')).pack()
            # SPACE pressed
            filepath = "temporary_image.jpg"
            cv2.imwrite(filepath, frame)
            break

    camera.release()
    cv2.destroyAllWindows()
    img_search()
    os.remove("temporary_image.jpg")
    tk.Label(root, text="hold on, searching", bg='#F0F8FF', font=('courier', 15, 'normal')).pack()
    root.destroy()

root = ''


# Search based on image window
def search_img():
    global root
    def dest():
        root.destroy()
    root = tk.Tk()
    root.lift()
    root.title("Search Window")
    root.geometry('890x580')
    root.configure(background='#F0F8FF')

    tk.Button(root, text='TAKE A PICTURE', bg='#00EEEE', font=('courier', 12, 'normal'), command=camera_search).place(
        x=107, y=63)

    tk.Button(root, text='UPLOAD A PICTURE', bg='#BCEE68', font=('courier', 12, 'normal'), command=upload_search).place(
        x=607, y=63)
    tk.Button(root, text='GO BACK', bg='#CD6600', font=('courier', 15, 'normal'), command=dest).place(x=387, y=273)
    
#calender for date
def calen():
    def grad_date():
        global udate
        udate = cal.get_date()
        dlist=udate.split("/")
        if dlist[2]>cdlist[2]:
            calen()
            _show('Error','Invalid date')
        elif (dlist[2]==cdlist[2] and dlist[0]>cdlist[0]) or (dlist[2]==cdlist[2] and dlist[0]==cdlist[0] and dlist[1]>cdlist[1]):
            calen()
            _show('Error','Invalid date')
        else:
            date_label=tk.Label(sc2, text=udate, bg='#F0F8FF', font=('verdana', 8, 'normal')).place(x=577, y=407)
        top1.destroy()
    today = date.today()
    d1 = today.strftime("%m/%d/%y")
    cdlist=d1.split("/")
    cdate=int(cdlist[1])
    cyear=int(cdlist[2])
    cmonth=int(cdlist[0])
    top1 = tk.Toplevel(sc2)
    cal = Calendar(top1, selectmode='day',year=cyear, month=cmonth,day=cdate)
    cal.pack(side=TOP)
    tk.Button(top1, text="Get Date",command=grad_date).pack(side=BOTTOM, pady=20)

#time
def timez():
    def updateTime():
        global time1
        time_tem=time_picker.time()
        top.destroy()
        for i in range(len(time_tem)):
            if i==0:
               time1+=str(time_tem[i])+":"
            else:
                time1+=str(time_tem[i])
        time_label=tk.Label(sc2, text=time1, bg='#F0F8FF', font=('verdana', 8, 'normal')).place(x=637, y=407)

    top = tk.Toplevel(sc2)

    time_picker = AnalogPicker(top, type=constants.HOURS12)
    time_picker.pack(expand=True, fill="both")
    theme = AnalogThemes(time_picker)
    theme.setDracula()
    #theme.setNavyBlue()
    #theme.setPurple() #to change theme
    ok_btn = tk.Button(top, text="ok", command=updateTime)
    ok_btn.pack()



# Database screen
def screen2():
    global filepath
    global newpath
    global MPINid
    global sc2


    def submit_id():
        global details
        found=False

        global ids,sc4
        searchid=ids.get()
        f = open("policedatabase.csv", "r")
        rr = reader(f)
        # need to exclude headers while checking
        #some logical error, not running
        for i in rr:
            if i!=[]:

                if str(i[0]).upper()==str(searchid).upper():
                        found = True
                        details=i
                        print("found")
                        break
        f.close()
        if found==True:
            person_found()

        if found==False:
            _show('Search complete','Person not found in database')


    def search_id():
        global ids,details,sc4
        sc4 = tk.Tk()
        sc4.title("Search based on MPIN")
        sc4.geometry('900x500')
        sc4.attributes('-topmost', True)
        sc4.configure(background='#F0F8FF')
        l1 = tk.Label(sc4, text="Tamilnadu Police Data Management System", font=font_head, foreground="Blue", width=1280)
        l1.pack()
        l2 = tk.Label(sc4, text="MISSING PERSONS' SEARCH SYSTEM", foreground="White", background="Red", font=font_subhead)
        l2.pack()
        tk.Label(sc4, text="ENTER MPIN id:", bg='#F0F8FF').place(x=300, y=257)
        ids = tk.Entry(sc4)
        ids.place(x=430, y=257)
        b2 = tk.Button(sc4, text='SUBMIT', bg='#00FFFF', font=('courier', 12, 'normal'), command=submit_id)
        b2.place(x=370, y=320)
        
        

    def upload_file():
        global MPINid, newpath,x
        file = tk.filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*')])
        if file:
            filepath = str(os.path.abspath(file.name))
            img = cv2.imread(filepath)
            f = open("policedatabase.csv", "r")
            rr = list(reader(f))
            for n in range(-1,-10,-1):
                if rr[n]!=[]:
                    refid = rr[n][0]
                    break
            idnum = int(refid[2:]) + 1
            MPINid = "TN" + str(idnum)
            newpath = "MPIN_pictures\\" + MPINid + ".jpg"
            cv2.imwrite(newpath, img)
            f.close()
            _show('IMAGE UPLOAD SUCCESSFUL', 'Please make a note of your MPIN ID-' + str(MPINid))
            x.destroy
    def new_report():

        def submit_missingreport():  # upon clicking submit
            sc2.state("zoomed")
            sc2.resizable(width=1, height=1)
            global name1, contacts, lastseenplace, info, MPINid, newpath, time1, udate, lastseentime
            lastseentime = str(time1)+" "+str(udate)
            name1, lastseentime, contacts, lastseenplace, info = name1.get(), lastseentime, contacts.get(), lastseenplace.get(), info.get()

            def confirm_submit():
                global date_label, time_label
                global name1, lastseentime, contacts, lastseenplace, info, MPINid, newpath
                f = open("policedatabase.csv", "a")
                wr = writer(f)
                wr.writerow([MPINid,name1,lastseentime,lastseenplace,contacts,info,newpath])
                f.close()
                _show("SUCCESS","You can close this window successfully.")

                new_report()



            frame = Frame(sc2)
            frame.pack(side=RIGHT)

            b4_ = tk.Label(frame, text="MPIN: "+MPINid, fg="green")
            b4_.pack(side=BOTTOM)

            b5_n = tk.Label(frame, text="NAME: "+name1, fg="green")
            b5_n.pack(side=BOTTOM)

            b6_ = tk.Label(frame, text="LAST SEEN: "+lastseenplace, fg="green")
            b6_.pack(side=BOTTOM)

            b7_b = tk.Label(frame, text="CONTACTS: "+contacts, fg="green")
            b7_b.pack(side=BOTTOM)

            b8_b = tk.Label(frame, text="ADDL.INFORMATION: "+info, fg="green")
            b8_b.pack(side=BOTTOM)


            t_b = tk.Label(frame, text="LAST SEEN DATE TIME: "+lastseentime, fg="green")
            t_b.pack(side=BOTTOM)

            tk.Button(frame, text='CONFIRM', bg='#0EF4DF', font=('verdana', 10, 'normal'), command=confirm_submit).pack(
                side=LEFT)
            tk.Button(frame, text='EDIT', bg='#0EF4DF', font=('verdana', 10, 'normal'), command=new_report).pack(
                side=LEFT)

        global name1, lastseentime, contacts, lastseenplace, info, time1
        name1 = tk.Entry(sc2)
        name1.place(x=397, y=367)
        tk.Button(sc2, text='OPEN CALENDER', bg='#7FFFD4', font=('courier', 9, 'normal'),command=calen).place(x=397, y=407)
        tk.Button(sc2, text='TIME', bg='#7FFFD4', font=('courier', 9, 'normal'), command=timez).place(x=527,y=407)
        contacts = tk.Entry(sc2)
        contacts.place(x=397, y=487)
        lastseenplace = tk.Entry(sc2)
        lastseenplace.place(x=397, y=567)
        info = tk.Entry(sc2)
        info.place(x=397, y=527)
        global x
        tk.Label(sc2, text='FULL NAME', bg='#F0F8FF', font=('verdana', 12, 'normal')).place(x=297, y=367)
        tk.Label(sc2, text='LAST SEEN DATE/TIME', bg='#F0F8FF', font=('verdana', 12, 'normal')).place(x=197, y=407)
        tk.Label(sc2, text='PICTURE', bg='#F0F8FF', font=('verdana', 12, 'normal')).place(x=307, y=447)
        tk.Label(sc2, text='CONTACT(S)', bg='#F0F8FF', font=('verdana', 12, 'normal')).place(x=287, y=487)
        tk.Label(sc2, text='ADDITIONAL DETAILS', bg='#F0F8FF', font=('verdana', 12, 'normal')).place(x=207, y=527)
        tk.Label(sc2, text='LAST SEEN PLACE', bg='#F0F8FF', font=('verdana', 12, 'normal')).place(x=207, y=567)
        tk.Button(sc2, text='SUBMIT', bg='#7FFFD4', font=('verdana', 15, 'normal'), command=submit_missingreport).place(x=662, y=447)
        x= tk.Button(sc2, text='UPLOAD IMAGE', bg='#0EF4DF', font=('verdana', 9, 'normal'), command=upload_file)
        x.place(x=397, y=447)


    sc2 = tk.Tk()
    welcome.destroy()
    sc2.title("Database Section")
    sc2.geometry('900x650')
    sc2.resizable(width=0, height=1)
    sc2.configure(background='#F0F8FF')
    l1 = tk.Label(sc2, text="Tamilnadu Police Data Management System", font=font_head, foreground="Blue", width=1280)
    l1.pack()
    l4 = tk.Label(sc2, text="MISSING PERSONS' SEARCH SYSTEM", foreground="White", background="Red", font=font_subhead)
    l4.pack()
    b2 = tk.Button(sc2, text='SEARCH BASED ON IMAGE', bg='#00FFFF', font=('courier', 12, 'normal'), command=search_img)
    b2.place(x=47, y=247)
    b3 = tk.Button(sc2, text='SEARCH BASED ON MPIN', bg='#00FFFF', font=('courier', 12, 'normal'),
                   command=search_id).place(x=357, y=247)
    b4 = tk.Button(sc2, text='FILE NEW REPORT', bg='#00FFFF', font=('courier', 12, 'normal'), command=new_report).place(
        x=667, y=247)
    name1, lastseentime, contacts, lastseenplace, info="","","","",""

    

# Password forgot dialogues
count = 2


def passwordreset():
    def reset():
        def check():
            def verify():
                global sixdig_pass, count
                ans = e3.get()
                if count == 0:
                    _show('Warning', 'Shutting down')
                    welcome.destroy()
                if ans == sixdig_pass:
                    screen2()
                if ans != sixdig_pass:
                    count -= 1
                    _show('Denied!', 'The answer is wrong. Attempts left: ' + str(count + 1))

            global registered_email, sixdig_pass
            z = e2.get()

            if z in registered_email:
                # creates SMTP session
                s = smtplib.SMTP('smtp.gmail.com', 587)
                # start TLS for security
                s.starttls()
                # Authentication
                s.login("policedtb.csproject@gmail.com", "iozseffpojvyhnwu")
                otp_pass=sixdig_pass+' is your OTP.'
                s.sendmail("policedtb.csproject@gmail.com", z, otp_pass)
                # terminating the session
                s.quit()

                l5 = tk.Label(text="Enter your 6 digit Verification-Code", bg="#5d8dac")
                l5.place(x=563, y=580)
                e3 = tk.Entry(welcome)
                e3.place(x=593, y=600)
                b3 = tk.Button(text="Enter Answer", command=verify, background="Grey", foreground="Blue")
                b3.place(x=614, y=625)
            else:
                global count
                count -= 1
                _show('Denied!', 'The answer is wrong. Attempts left: ' + str(count + 1))
                if count == 0:
                    _show('Warning', 'Shutting down')
                    welcome.destroy()

        l1 = tk.Label(welcome, text="Enter your REGISTERED EMAIL ID", bg="#5d8dac")
        l1.place(x=563, y=515)
        e2 = tk.Entry(welcome)
        e2.place(x=595, y=535)
        b2 = tk.Button(text="Enter Answer", command=check, background="Grey", foreground="Blue")
        b2.place(x=614, y=555)

    b1 = tk.Button(welcome, text="Forgot Username/Password?", command=reset, foreground="Blue")
    b1.place(x=576, y=480)


# Password authentication
def store():
    global user_pass
    loginsuccess='fail'
    user, passw = tb1.get(), tb2.get()
    for i in user_pass:
        if i[0]==user and i[1]==passw:
            usernam=i[2]
            _show('Welcome', 'Redirecting you now, ' + usernam)
            screen2()
            loginsuccess='success'
    if loginsuccess=='fail':
        _show('Unauthorized', 'Check the details you entered.')
        passwordreset()


# FONTS
font_head = Font(
    family='Garmond',
    size=30,
    weight='bold',
)

font_subhead = Font(
    family='Times New Roman',
    size=20,
    weight='bold',
)
u_name = Font(
    family='Century Gothic',
    size=15,
    weight='bold',
)
# IMAGES
bg_img = PIL.Image.open("background image.jpg")
size1 = (1920, 1280)
bg_img = bg_img.resize(size1)
bgimg = ImageTk.PhotoImage(bg_img)

# loginscreen
welcome.title("Police Data Management System - LOGIN")
welcome.state("zoomed")
limg = tk.Label(image=bgimg)
limg.pack()
l1 = tk.Label(welcome, text="Tamilnadu Police Data Management System", font=font_head, foreground="White",
              background="Red", width=1280)
l1.pack()
l4 = tk.Label(text="LOGIN", foreground='white', bg='blue', font=font_head, width=10)
l4.place(x=540, y=185)
l3 = tk.Label(text="USERNAME", foreground='green', bg="#5d8dac", font=u_name)
l3.place(x=602, y=285)
l3 = tk.Label(text="PASSWORD", foreground='green', bg="#5d8dac", font=u_name)
l3.place(x=602, y=345)
tb1 = tk.Entry()
tb1.place(x=595, y=315)
tb2 = tk.Entry(show="*")
tb2.place(x=595, y=375)
b1 = tk.Button(text="SUBMIT", command=store, foreground="green")
b1.place(x=631, y=410)
welcome.mainloop()

#END OF PROGRAM