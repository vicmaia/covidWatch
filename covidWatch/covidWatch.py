# Multi-frame tkinter application v2.3
import tkinter as tk
from typing import Any
from twilio.rest import Client
import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import webbrowser
import requests
from datetime import datetime, timedelta
import requests
import json
from urllib.request import urlopen
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sys
from PIL import ImageTk,Image
import io

class CovidApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Login)
        self.configure(background="#002366")
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', lambda e: self.destroy())

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class Login(tk.Frame):
    global reg
    reg = False
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, background="#002366")

        self.master = master

        # Create all required texts
        mainText = "Welcome to COVID Watch! \n Please, log in using two-step verification: "
        infoText = "For more information about COVID-19,\n vaccination, and testing, visit: \nhttps://www.cdc.gov/"
        vaxInfo = "Find COVID-19 vaccines:\n https://www.vaccines.gov/"
        testInfo = "Need COVID-19 testing? Visit CVS to \n schedule an appointment or contact your local area\n for more information."

        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(8, weight=1)

        def percentage(part):
            return 100 * float(part) / float(1250)

        filler1 = tk.Label(self, text="            ", bg="#002366").grid(row=0, column=3, pady=percentage(650))

        # Create label for main text
        mainLabel = tk.Label(self, fg="white", bg="#002366", text=mainText, font=("Playfair 24 bold"))
        mainLabel.grid(row=1, column=3, sticky=tk.S, pady=percentage(650))

        # Create username label
        userNameLabel = tk.Label(self, fg="white", bg="#002366", text="Username: ", font=("Playfair 24"))
        userNameLabel.grid(row=2, column=3, sticky=tk.NW)

        # Create username input box
        global Login_UserName
        Login_UserName = tk.StringVar()
        self.userName = tk.Entry(self, bd=5, bg="white", width=45, textvariable=Login_UserName)
        self.userName.grid(row=2, column=3, sticky='e')

        # Create passoword label
        passwordLabel = tk.Label(self, fg="white", bg="#002366", text="Password: ", font=("Playfair 24"))
        passwordLabel.grid(row=4, column=3, sticky='w')

        # Create password input box
        self.password = tk.Entry(self, bd=5, bg="white", width=45, show="*")
        self.password.grid(row=4, column=3, sticky='e', pady=50)

        # Create continue button
        self.continueButton = tk.Button(self, bg="#008000", fg="white", font=("Playfair", 20, 'bold'), width=20,
                                       text="Continue", command= self.completed)
        self.continueButton.grid(row=5, column=3, sticky='')

        self.password.bind("<Return>", lambda e: self.completed())

        # Create click here button
        clickHere = tk.Button(self, bg='#002366', fg='white', text="Click Here to Register for an Account",
                              font='Playfair 12 underline',
                              command=lambda: master.switch_frame(Register))
        clickHere.grid(row=6, column=3, pady=20)

        # Create Label for vax info
        vaxLabel = tk.Label(self, fg="white", bg="#002366", text=vaxInfo, font=("Playfair 12"))
        vaxLabel.grid(row=8, column=3, pady=50)

        # Create labels for info texts
        infoLabel = tk.Label(self, fg="white", bg="#002366", text=infoText, font=("Playfair 12"))
        infoLabel.grid(row=8, column=0)

        # Create labels for test info
        testLabel = tk.Label(self, fg="white", bg="#002366", text=testInfo, font=("Playfair 12"))
        testLabel.grid(row=8, column=4)

    #Function to test if a username and password are within the database.
    def NameInUse(self,user,password):
        data = list(sqlite3.connect('verifyNumber.db').cursor().execute('SELECT * FROM accounts WHERE userName = ? AND password = ?', (user,password,)))
        return bool(data)

    # check to see if input is complete
    def completed(self):
        name = self.userName.get()
        userPass = self.password.get()
        inUse = self.NameInUse(name, userPass)

        if len(self.userName.get()) == 0 or len(self.password.get()) == 0:
            messagebox.showinfo("Error", "Oops! Please complete all required fields.")
        elif not inUse:
            messagebox.showinfo("Error", "Your username or password is incorrect, please try again.")
        elif self.password.get() and self.userName.get():
            self.password.config(state='disabled')
            self.userName.config(state='disabled')
            self.master.switch_frame(TwoStep)

        
class Register(tk.Frame):
    reg = False
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, background="#002366")

        def percentage(part):
            return 100 * float(part) / float(1250)

        filler1 = tk.Label(self, text="           ", bg="#002366")
        filler1.grid(row=0, column=0, pady=percentage(650))

        # Create an account label
        createAccountLabel = tk.Label(self, fg="white", bg="#002366", text="Create an account: ",
                                      font=("Playfair 40 bold"))
        createAccountLabel.grid(row=1, column=2, columnspan=2, sticky=tk.S, pady=percentage(650))

        # Create first name label
        firstNameLabel = tk.Label(self, fg="white", bg="#002366", text="First Name: ", font=("Playfair 28"))
        firstNameLabel.grid(row=2, column=2, sticky=tk.W, pady=25)

        # Creat last name label
        lastLabel = tk.Label(self, fg="white", bg="#002366", text="Last Name: ", font=("Playfair 28"))
        lastLabel.grid(row=3, column=2, sticky=tk.W)

        # Create email label.
        userNameLabel = tk.Label(self, fg="white", bg="#002366", text="Username: ", font=("Playfair 28"))
        userNameLabel.grid(row=4, column=2, sticky=tk.W, pady=25)

        # Create phone number label
        phoneLabel = tk.Label(self, fg="white", bg="#002366", text="Phone Number: ", font=("Playfair 28"))
        phoneLabel.grid(row=5, column=2, sticky=tk.W)

        # Create password label
        passwordLabel = tk.Label(self, fg="white", bg="#002366", text="Password: ", font=("Playfair 28"))
        passwordLabel.grid(row=6, column=2, sticky=tk.W, pady=25)

        # Create fist name input box
        self.firstName = tk.Entry(self, bd=5, bg="white", width=45)
        self.firstName.grid(row=2, column=3, sticky=tk.W, pady=25)

        # Create lastname input box
        self.lastName = tk.Entry(self, bd=5, bg="white", width=45)
        self.lastName.grid(row=3, column=3, sticky=tk.W)

        # Create username input box
        global Register_UserName
        Register_UserName = tk.StringVar()
        self.userName = tk.Entry(self, bd=5, bg="white", width=45, textvariable=Register_UserName)
        self.userName.grid(row=4, column=3, sticky=tk.W, pady=25)

        # Create phone number input box
        self.phone = tk.Entry(self, bd=5, bg="white", width=45)
        self.phone.grid(row=5, column=3, sticky=tk.W)

        # Create passoword input box
        self.password = tk.Entry(self, bd=5, bg="white", width=45)
        self.password.grid(row=6, column=3, sticky=tk.W, pady=25)

        # Create next button
        self.nextButton = tk.Button(self, bg="green", fg="white", font=("Playfair", 20, 'bold'), width=15, text="Next",
                                    command=self.completed)
        self.nextButton.grid(row=7, column=3, sticky=tk.E)

        # Create "back" button
        self.backButton = tk.Button(self, bg="red", fg="white", font=("Playfair", 20, 'bold'), width=15, text="Back",
                                    command=lambda: master.switch_frame(Login))
        self.backButton.grid(row=7, column=2, sticky=tk.W)

        # Create "cancel" button
        self.cancelButton = tk.Button(self, bg="#0277bd", fg="white", font=("Playfair", 15, 'bold'), width=15,
                                      text="Back to Login",
                                      command=lambda: master.switch_frame(Login))

        # Create continue button
        self.continueButton = tk.Button(self, bg="green", fg="white", font=("Playfair", 20, 'bold'), width=15,
                                        text="Continue",
                                        command=lambda: master.switch_frame(TwoStep))

    #Function to test if a username is already being used within the database.
    def NameInUse(self,user):
            data = list(sqlite3.connect('verifyNumber.db').cursor().execute('SELECT * FROM accounts WHERE userName = ?', (user,)))
            return bool(data)

    # check to see if input is complete
    def completed(self):
        name = Register_UserName.get()
        inUse = self.NameInUse(name)
        if inUse:
            messagebox.showinfo("Error", "That username is already in use. Please try a different one.")
        elif self.password.get() and self.phone.get() and self.userName.get() and self.lastName.get() and self.firstName.get():
            self.password.config(state='disabled')
            self.phone.config(state='disabled')
            self.userName.config(state='disabled')
            self.lastName.config(state='disabled')
            self.firstName.config(state='disabled')
            self.nextButton.destroy()
            self.backButton.destroy()
            self.cancelButton.grid(row=8, column=2, columnspan=2, sticky=tk.S, pady=25)
            self.continueButton.grid(row=7, column=2, columnspan=2, sticky=tk.S)
            #Set reg to True to indicate that a user has just registered.
            global reg
            reg = True

            #Connect to a database
            conn = sqlite3.connect('verifyNumber.db')
            # Create cursor
            c = conn.cursor()
            #Insert record into database
            c.execute("INSERT INTO accounts VALUES (:first_name, :last_name, :userName, :phoneNum, :password, :vaxCard)",
                      {
                          'first_name': self.firstName.get(),
                          'last_name': self.lastName.get(),
                          'userName': self.userName.get(),
                          'phoneNum': self.phone.get(),
                          'password': self.password.get(),
                          'vaxCard' : None
                      })
            
            conn.commit()  
        else:
            messagebox.showinfo("Error", "Oops! Please complete all required fields.")


class TwoStep(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, background="#002366")
        # Generate random 6-digit number
        self.n = random.randint(100000, 999999)


        global UserPhoneNumber
        
        #if user has just registred an account, get their registration username
        if reg:
            RegisterUserName = Register_UserName.get()
            record = self.NameInUse(RegisterUserName)

        #otherwise, get login username
        else:
            LoginUserName = Login_UserName.get()
            record = self.NameInUse(LoginUserName)

        UserPhoneNumber = "+1" + record[3]

        
        #Connect to Twilio API
        self.client = Client("AC1a73645c62739a7e87d5871b52663b7f", "1542717052f64084f312e8c8ae6a85fb")
        self.client.messages.create(to=[UserPhoneNumber],
                                    from_="+19167948115",
                                    body=self.n)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)

        def percentage(part):
            return 100 * float(part) / float(1250)

        filler1 = tk.Label(self, text="            ", bg="#002366").grid(row=0, column=1, pady=percentage(1000))

        # Create Label & place it with grid
        self.Login_Title = tk.Label(self, text="Please enter your 6-digit OTP", bg="#002366", fg='#ffffff',
                                    font=("Playfair", 24, 'bold'))
        self.Login_Title.grid(row=1, column=1, sticky=tk.S, pady=percentage(600))

        # Create text input field & place it with grid
        global otp
        otp = tk.StringVar()
        self.verification = tk.Entry(self, borderwidth=2, width=30, font=("Playfair", 20), textvariable=otp)
        self.verification.grid(row=2, column=1, sticky=tk.N)
        
        self.verification.bind('<Return>', lambda e: self.checkOTP())

        filler = tk.Label(self, text="            ", bg="#002366").grid(row=3, column=1, pady=15)

        # Create check OTP button
        self.checkOTPButton = tk.Button(self, text="Check OTP", padx=50, pady=5, border=0, command= self.checkOTP,
                                      bg="white", fg="black", font=("Playfair", 15, 'bold'), width = 10)
        self.checkOTPButton.grid(row=4, column=1, sticky=tk.S)

        # Create Continue button
        self.continueButton = tk.Button(self, text = "Continue", bg="green", fg="white", font=("Playfair", 20, 'bold'), width = 15, command = lambda: [master.destroy(), HomePage()])

        #Create cancel button
        self.cancelButton = tk.Button(self, bg="red", fg="white", text = "Cancel", command = self.canceled, font=("Playfair", 12, 'bold'))
        self.cancelButton.grid(row = 10, column=1, sticky=tk.S, pady = 25)

        self.master = master


    #Function called if User selects cancel button
    def canceled(self):
        global reg

        #If the user has just registered an account and selects cancel button on 2-step, delete that record from DB and go to Login Page
        if reg:
            reg = False
            RegisterUserName = Register_UserName.get() 
            #Connect to a database
            conn = sqlite3.connect('verifyNumber.db')
            # Create cursor
            c = conn.cursor()
            #Insert record into database
            c.execute("""DELETE FROM accounts WHERE userName = :user""", {
                     'user': RegisterUserName
                    })
            conn.commit() 
            self.master.switch_frame(Login)
        else: #If user has logged in, and selects cancel at 2-step, just go back to login page
            self.master.switch_frame(Login)

    #Function to return a single record from the database matching a username
    def NameInUse(self,user):
            data = list(sqlite3.connect('verifyNumber.db').cursor().execute('SELECT * FROM accounts WHERE userName = ?', (user,)))
            return data[0]

    #Function to check user OTP input.
    def checkOTP(self):
        if len(otp.get()) == 0:
            messagebox.showinfo("Error", "INVALID OTP")
        else:
            # User inputs a 6-digit number
            #self.userInput = int(self.verification.get(1.0, "end-1c"))
            self.userInput = int(otp.get())
            # User input matches generated number
            if self.userInput == self.n:
                self.verification.config(state='disabled')
                self.checkOTPButton.destroy()
                self.continueButton.grid(row=4, column=1, sticky=tk.S)
            # incorrect OTP
            else:
                messagebox.showinfo("Error", "Wrong OTP")



class HomePage(Tk):
    def __init__(self):
        super().__init__()
        self.configure(background="#002366")
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', lambda e: self.destroy())

        #Configure rows and columns
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight= 1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        #create covid watch header label
        covidWatchLabel = tk.Label(self, fg = 'green', bg = '#002366', text = 'CovidWatch', font = ("Playfair 32 bold"))
        covidWatchLabel.grid(row =0, column=0, sticky='nw')

        canvas = Canvas(self, width = 100000, height=10, bg='green')
        canvas.grid(row=0, column=0, columnspan=4)

    

        #Create the buttons
        HomeButton = tk.Button(self, fg= "white", bg = "green", text = "Home", font = ("Playfair 16 bold"), width=16, command = self.homePage)
        HomeButton.grid(row =0, column= 0, sticky = 's')

        VaxTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Vaccination Tracker", font = ("Playfair 16 bold"), command = self.vaxLookUp)
        VaxTrackButton.grid(row =0, column= 1, sticky  = 's')

        VaxCardButton = tk.Button(self, fg= "white", bg = "green", text = "Upload Vaccination Card", font = ("Playfair 16 bold"), command = self.uploadPage)
        VaxCardButton.grid(row =0, column= 2, sticky= 's') 

        DataTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Covid-19 Data Tracker", font = ("Playfair 16 bold"), command = self.covidDataLookup)
        DataTrackButton.grid(row =0, column= 3, sticky='s')

        #create the photos
        photo = Image.open("vaccineImg.jpg")
        photoResize = photo.resize((300,300))
        image_one = ImageTk.PhotoImage(photoResize)
        imageLabel = tk.Label(self, image=image_one)
        imageLabel.photo = image_one

        photo2 = Image.open("covid_test.jpg")
        photoResize2 = photo2.resize((300,300))
        image_two = ImageTk.PhotoImage(photoResize2)
        imageLabel2 = tk.Label(self, image=image_two)
        imageLabel2.photo = image_two

        photo3 = Image.open("gen_info.jpg")
        photoResize3 = photo3.resize((300,300))
        image_three = ImageTk.PhotoImage(photoResize3)
        imageLabel3 = tk.Label(self, image=image_three)
        imageLabel3.photo = image_three
        
        img3Button = tk.Button(self, image = image_three, bd=0)
        img3Button.grid(row=2, column=3, columnspan=3, sticky='e', padx=40)


        #create the labels and hyperlinks
        vaccineLabel = tk.Label(self, text = "Click Here to schedule your COVID-19 vaccine", font=('playfair 11 underline bold' ), bg='#002366', fg = 'green')
        vaccineLabel.grid(row=3, column=0, sticky= 'nw', columnspan=2, padx=40)
        vaccineLabel.bind("<Button-1>", lambda e: self.webpage("https://vaccines.gov"))

        testText = tk.Label(self, text = 'Click Here to schedule a COVID-19 test', font='playfair 11 underline bold', background='#002366', fg = 'green' )
        testText.grid(row=3, column=1, columnspan=2, sticky='n')
        testText.bind("<Button-1>", lambda e: self.webpage("https://www.cvs.com/minuteclinic/covid-19-testing"))

        genInfoText = tk.Label(self, text= "Click Here for information on COVID-19", font= 'Playfair 11 bold underline', background = '#002366', fg = 'green')
        genInfoText.grid(row=3, column = 3, sticky='ne', padx=40)
        genInfoText.bind("<Button-1>", lambda e: self.webpage("https://www.cdc.gov/coronavirus/2019-ncov/travelers/travel-during-covid19.html"))

        imgButton = tk.Button(self, image = image_one, bd=0)
        imgButton.grid(row=2, column =0, columnspan=2, sticky='w', padx=40)

        imgButton2 = tk.Button(self, image = image_two, bd=0)
        imgButton2.grid(row=2, column= 1, columnspan=2)

        #if user has just registred an account, get their registration username
        if reg:
            global RegisterUserName
            RegisterUserName = Register_UserName.get()

        else: #otherwise, get login username
            global LoginUserName
            LoginUserName = Login_UserName.get()

    #Function to open webpage
    def webpage(self,url):
        webbrowser.open_new_tab(url)

    #Home page function
    def homePage(self):
        #destroy previous page widgets
        for widgets in self.winfo_children():
            widgets.destroy()


        #create covid watch header label
        covidWatchLabel = tk.Label(self, fg = 'green', bg = '#002366', text = 'CovidWatch', font = ("Playfair 32 bold"))
        covidWatchLabel.grid(row =0, column=0, sticky='nw')

        canvas = Canvas(self, width = 100000, height=10, bg='green')
        canvas.grid(row=0, column=0, columnspan=4)

    

        #create buttons
        HomeButton = tk.Button(self, fg= "white", bg = "green", text = "Home", font = ("Playfair 16 bold"), width=16, command = self.homePage)
        HomeButton.grid(row =0, column= 0, sticky = 's')

        VaxTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Vaccination Tracker", font = ("Playfair 16 bold"), command = self.vaxLookUp)
        VaxTrackButton.grid(row =0, column= 1, sticky  = 's')

        VaxCardButton = tk.Button(self, fg= "white", bg = "green", text = "Upload Vaccination Card", font = ("Playfair 16 bold"), command = self.uploadPage)
        VaxCardButton.grid(row =0, column= 2, sticky= 's') 

        DataTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Covid-19 Data Tracker", font = ("Playfair 16 bold"), command = self.covidDataLookup)
        DataTrackButton.grid(row =0, column= 3, sticky='s')


        #create images
        photo = Image.open("vaccineImg.jpg")
        photoResize = photo.resize((300,300))
        image_one = ImageTk.PhotoImage(photoResize)
        imageLabel = tk.Label(self, image=image_one)
        imageLabel.photo = image_one

        photo2 = Image.open("covid_test.jpg")
        photoResize2 = photo2.resize((300,300))
        image_two = ImageTk.PhotoImage(photoResize2)
        imageLabel2 = tk.Label(self, image=image_two)
        imageLabel2.photo = image_two

        photo3 = Image.open("gen_info.jpg")
        photoResize3 = photo3.resize((300,300))
        image_three = ImageTk.PhotoImage(photoResize3)
        imageLabel3 = tk.Label(self, image=image_three)
        imageLabel3.photo = image_three
        
        
        img3Button = tk.Button(self, image = image_three, bd=0)
        img3Button.grid(row=2, column=3, columnspan=3, sticky='e', padx=40)


        #create labels and hyperlinks
        vaccineLabel = tk.Label(self, text = "Click Here to schedule your COVID-19 vaccine", font=('playfair 11 underline bold' ), bg='#002366', fg = 'green')
        vaccineLabel.grid(row=3, column=0, sticky= 'nw', columnspan=2, padx=40)
        vaccineLabel.bind("<Button-1>", lambda e: self.webpage("https://vaccines.gov"))

        testText = tk.Label(self, text = 'Click Here to schedule a COVID-19 test', font='playfair 11 underline bold', background='#002366', fg = 'green' )
        testText.grid(row=3, column=1, columnspan=2, sticky='n')
        testText.bind("<Button-1>", lambda e: self.webpage("https://www.cvs.com/minuteclinic/covid-19-testing"))

        genInfoText = tk.Label(self, text= "Click Here for information on COVID-19", font= 'Playfair 11 bold underline', background = '#002366', fg = 'green')
        genInfoText.grid(row=3, column = 3, sticky='ne', padx=40)
        genInfoText.bind("<Button-1>", lambda e: self.webpage("https://www.cdc.gov/coronavirus/2019-ncov/travelers/travel-during-covid19.html"))

        imgButton = tk.Button(self, image = image_one, bd=0)
        imgButton.grid(row=2, column =0, columnspan=2, sticky='w', padx=40)

        imgButton2 = tk.Button(self, image = image_two, bd=0)
        imgButton2.grid(row=2, column= 1, columnspan=2)

        #if user has just registred an account, get their registration username
        if reg:
            global RegisterUserName
            RegisterUserName = Register_UserName.get()

        else: #otherwise, get login username
            global LoginUserName
            LoginUserName = Login_UserName.get()


    #File dialog to select files
    def filedialogs(self):
        global get_image
        get_image = filedialog.askopenfilenames()


    #Image needs to be converted into binary before insert into database
    def convert_image_into_binary(self,filename):
        with open(filename, 'rb') as file:
            photo_image = file.read()
        return photo_image

    #insert image into database
    def insert_image(self):

        image_database = sqlite3.connect("verifyNumber.db")
        data = image_database.cursor()

       
        if reg:  # if user uploads vaccination card after registration
            for image in get_image:
               self.insert_photo   = self.convert_image_into_binary(image)
               data.execute("""UPDATE accounts SET
                            vaxCard = :vaccineCard
                            WHERE userName = :user""",
                    {
                    'vaccineCard': self.insert_photo,
                     'user': RegisterUserName
                    })
        else: # if user uploads vaccination card after login
            for image in get_image:
               self.insert_photo   = self.convert_image_into_binary(image)
               data.execute("""UPDATE accounts SET
                            vaxCard = :vaccineCard
                            WHERE userName = :user""",
                    {
                    'vaccineCard': self.insert_photo,
                     'user': LoginUserName
                    })
           

        image_database.commit()
        image_database.close()

        #connect to database
        conn = sqlite3.connect("verifyNumber.db")
        cur = conn.cursor()
        #Query database for specific record to find vax card
        fetch_blob = """SELECT vaxCard FROM accounts WHERE userName =?"""

        if reg: # if user uploads vaccination card after registration
            self.uploadText.destroy()
            cur.execute(fetch_blob, (RegisterUserName,))
            record = cur.fetchone()
            photo = record[0]
            conn.close()
            #Convert image
            img = Image.open(io.BytesIO(photo))
            imgResize = img.resize((350,280))
            vaxImage = ImageTk.PhotoImage(imgResize)

            #Display image to page.
            label = tk.Label(self, image=vaxImage)
            label.photo = vaxImage
            label.grid(row = 2, column =1, columnspan =2, sticky='s')
        else: #if user has just logged in
            self.uploadText.destroy()
            cur.execute(fetch_blob, (LoginUserName,))
            record = cur.fetchone()
            photo = record[0]
            conn.close()
            #Convert image
            img = Image.open(io.BytesIO(photo))
            imgResize = img.resize((350,280))
            vaxImage = ImageTk.PhotoImage(imgResize)
            #Display image to page.
            label = tk.Label(self, image=vaxImage)
            label.photo = vaxImage
            label.grid(row = 2, column =1, columnspan =2, sticky='s')

    #Function to upload vaccination card.
    def uploadPage(self):
        self.bind('<Escape>', lambda e: [self.destroy(), sys.exit()])
        #destroy previous page widgets
        for widget in self.winfo_children():
            widget.destroy()


        #Create Home page button and place it on page.
        HomeButton = tk.Button(self, fg= "white", bg = "green", text = "Home", font = ("Playfair 16 bold"), width=16, command = self.homePage)
        HomeButton.grid(row =0, column= 0)

        #Create vaccination tracker page button and place it on page.
        VaxTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Vaccination Tracker", font = ("Playfair 16 bold"), command= self.vaxLookUp)
        VaxTrackButton.grid(row =0, column= 1)

        #Create vaccination card upload page button and place it on page.
        VaxCardButton = tk.Button(self, fg= "white", bg = "green", text = "Upload Vaccination Card", font = ("Playfair 16 bold"), command = self.uploadPage)
        VaxCardButton.grid(row =0, column= 2) 

        #Create covid data tracker page button and place it on page.
        DataTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Covid-19 Data Tracker", font = ("Playfair 16 bold"), command = self.covidDataLookup)
        DataTrackButton.grid(row =0, column= 3)

        #Label instructing to upload vaccine card
        self.uploadText = tk.Label(self, fg= 'white', bg = '#002366', text = "Please upload your vaccine card below:", font = ("Playfair 24 bold"))
        self.uploadText.grid(row = 2, column =1, columnspan =2, sticky='s')

        #Button to upload vax card
        uploadButton = tk.Button(self, bg = 'grey', fg = 'white', text = "Choose File", font = ("Playfair 20 "), command = self.filedialogs)
        uploadButton.grid(row =3, column =1, columnspan = 2)

        #Button to submit photo to database
        saveButton = tk.Button(self, bg='grey', fg='white', text="Submit", font=("Playfair 20 "),command= self.insert_image)
        saveButton.grid(row=5, column=1, columnspan=2)

        #Connect to database
        conn = sqlite3.connect("verifyNumber.db")
        cur = conn.cursor()
        fetch_blob = """SELECT vaxCard FROM accounts WHERE userName =?"""


        # if user uploads vaccination card after registration
        if reg:
            #If database record exists, display vaxcard... Else do nothing.
            var = self.NameInUse(RegisterUserName)
            result = isinstance(var, bytes)
            if result:
                self.uploadText.destroy()
                cur.execute(fetch_blob, (RegisterUserName,))
                record = cur.fetchone()
                photo = record[0]
                conn.close()

                img = Image.open(io.BytesIO(photo))
                imgResize = img.resize((350,280))
                vaxImage = ImageTk.PhotoImage(imgResize)

                label = tk.Label(self, image=vaxImage)
                label.photo = vaxImage
                label.grid(row = 2, column =1, columnspan =2, sticky='s')
        else: #user has logged in
            #If database record exists, display vaxcard... Else do nothing.
            var = self.NameInUse(LoginUserName)
            result = isinstance(var, bytes)
            if result:
                self.uploadText.destroy()
                cur.execute(fetch_blob, (LoginUserName,))
                record = cur.fetchone()
                photo = record[0]
                conn.close()

                img = Image.open(io.BytesIO(photo))
                imgResize = img.resize((350,280))
                vaxImage = ImageTk.PhotoImage(imgResize)

                label = tk.Label(self, image=vaxImage)
                label.photo = vaxImage
                label.grid(row = 2, column =1, columnspan =2, sticky='s')
    
    def NameInUse(self, user):
        data = list(sqlite3.connect('verifyNumber.db').cursor().execute('SELECT * FROM accounts WHERE userName = ?', (user,)))
        return data[0][5]


    #Function to search covid data by State and County.   
    def covidDataLookup(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(background="#002366")

            
        HomeButton = tk.Button(self, fg= "white", bg = "green", text = "Home", font = ("Playfair 16 bold"), width=16, command = self.homePage)
        HomeButton.grid(row =0, column= 0)

        VaxTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Vaccination Tracker", font = ("Playfair 16 bold"), command= self.vaxLookUp)
        VaxTrackButton.grid(row =0, column= 1)

        VaxCardButton = tk.Button(self, fg= "white", bg = "green", text = "Upload Vaccination Card", font = ("Playfair 16 bold"), command = self.uploadPage)
        VaxCardButton.grid(row =0, column= 2) 

        DataTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Covid-19 Data Tracker", font = ("Playfair 16 bold"))
        DataTrackButton.grid(row =0, column= 3)

        #Create State selectable option
        global StateClicked
        StateClicked = StringVar()
        StateClicked.set( "Select State" )
        
        States = ['Alabama','Alaska', 'Arizona','Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
            'Hawaii','Idaho', 'Illinois','Indiana','Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine','Maryland','Massachusetts',
            'Michigan', 'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina', 'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico',
            'Nevada', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
            'Utah', 'Virginia', 'Vermont', 'Washington', 'Wisconsin', 'West Virginia', 'Wyoming']
        
        global StateSelections
        StateSelections = ttk.Combobox(self, value = States, textvariable=StateClicked, width = 25, font="Playfair 18", state="readonly") 
        StateSelections.grid(row =2, column=0, sticky=tk.E)
        StateSelections.bind("<<ComboboxSelected>>", self.pick_state)


        #Create selectable county
        CountyClicked = StringVar()
        CountyClicked.set("Select County")

        global CountySelections
        CountySelections = ttk.Combobox(self, value=[" "], textvariable=CountyClicked, width = 25, font="Playfair 18", state="readonly") 
        CountySelections.grid(row =2, column=2, sticky= tk.W)

    
        #Button to load data based on State and County input.
        checkDataButton = tk.Button(self, fg= "white", bg = "green", text = "Get \n Covid Data", font = ("Playfair 12 bold"), command= lambda: [self.dataPage(CountyClicked, StateClicked), 
                        CountySelections.destroy(), StateSelections.destroy(), checkDataButton.destroy()])
        checkDataButton.grid(row =2, column=3, sticky = tk.W, columnspan=2)
    
    #Pull list of counties from DB dependent on state selected
    def pick_state(self, e):
        if StateClicked.get() == "Alabama" or StateClicked.get() == "AL":
            sql = """SELECT * FROM Alabama"""

        elif StateClicked.get() == "Alaska" or StateClicked.get() == 'AK':
            sql = """SELECT * FROM Alaska"""

        elif StateClicked.get() == "Arizona" or StateClicked.get() == "AZ":
            sql = """SELECT * FROM Arizona"""

        elif StateClicked.get() == "Arkansas" or StateClicked.get() == "AR":
            sql = """SELECT * FROM Arkansas"""
            
        elif StateClicked.get() == "California" or StateClicked.get() == "CA":
            sql = """SELECT * FROM California"""

        elif StateClicked.get() == "Colorado" or StateClicked.get() == "CO":
            sql = """SELECT * FROM Colorado"""

        elif StateClicked.get() == "Connecticut" or StateClicked.get() == "CT":
            sql = """SELECT * FROM Connecticut"""

        elif StateClicked.get() == "Delaware" or StateClicked.get() == "DE":
            sql = """SELECT * FROM Delaware"""

        elif StateClicked.get() == "Florida" or StateClicked.get() == "FL":
            sql = """SELECT * FROM Florida"""

        elif StateClicked.get() == "Georgia" or StateClicked.get() == "GA":
            sql = """SELECT * FROM Georgia"""

        elif StateClicked.get() == "Hawaii" or StateClicked.get() == "HI":
            sql = """SELECT * FROM Hawaii"""

        elif StateClicked.get() == "Idaho" or StateClicked.get() == "ID":
            sql = """SELECT * FROM Idaho"""

        elif StateClicked.get() == "Illinois" or StateClicked.get() == "IL":
            sql = """SELECT * FROM Illinois"""
        
        elif StateClicked.get() == "Indiana" or StateClicked.get() == "IN":
            sql = """SELECT * FROM Indiana"""

        elif StateClicked.get() == "Iowa" or StateClicked.get() == "IA":
            sql = """SELECT * FROM Iowa"""

        elif StateClicked.get() == "Kansas" or StateClicked.get() == "KS":
            sql = """SELECT * FROM Kansas"""

        elif StateClicked.get() == "Kentucky" or StateClicked.get() == "KY":
            sql = """SELECT * FROM Kentucky"""
    
        elif StateClicked.get() == "Louisiana" or StateClicked.get() == "LA":
            sql = """SELECT * FROM Louisiana"""

        elif StateClicked.get() == "Maine" or StateClicked.get() == "ME":
            sql = """SELECT * FROM Maine"""

        elif StateClicked.get() == "Maryland" or StateClicked.get() == "MD":
            sql = """SELECT * FROM Maryland"""

        elif StateClicked.get() == "Massachusetts" or StateClicked.get() == "MA":
            sql = """SELECT * FROM Massachusetts"""

        elif StateClicked.get() == "Michigan" or StateClicked.get() == "MI":
            sql = """SELECT * FROM Michigan"""

        elif StateClicked.get() == "Minnesota" or StateClicked.get() == "MN":
            sql = """SELECT * FROM Minnesota"""

        elif StateClicked.get() == "Mississippi" or StateClicked.get() == "MS":
            sql = """SELECT * FROM Mississippi"""

        elif StateClicked.get() == "Missouri" or StateClicked.get() == "MO":
            sql = """SELECT * FROM Missouri"""

        elif StateClicked.get() == "Montana" or StateClicked.get() == "MT":
            sql = """SELECT * FROM Montana"""
        
        elif StateClicked.get() == "Nebraska" or StateClicked.get() == "NE":
            sql = """SELECT * FROM Nebraska"""
        
        elif StateClicked.get() == "Nevada" or StateClicked.get() == "NV":
            sql = """SELECT * FROM Nevada"""
        
        elif StateClicked.get() == "New Hampshire" or StateClicked.get() == "NH":
            sql = """SELECT * FROM 'New Hampshire'"""
        
        elif StateClicked.get() == "New Jersey" or StateClicked.get() == "NJ":
            sql = """SELECT * FROM 'New Jersey'"""
        
        elif StateClicked.get() == "New Mexico" or StateClicked.get() == "NM":
            sql = """SELECT * FROM 'New Mexico'"""
        
        elif StateClicked.get() == "New York" or StateClicked.get() == "NY":
            sql = """SELECT * FROM 'New York'"""
        
        elif StateClicked.get() == "North Carolina" or StateClicked.get() == "NC":
            sql = """SELECT * FROM 'North Carolina'"""
        
        elif StateClicked.get() == "North Dakota" or StateClicked.get() == "ND":
            sql = """SELECT * FROM 'North Dakota'"""
        
        elif StateClicked.get() == "Ohio" or StateClicked.get() == "OH":
            sql = """SELECT * FROM Ohio"""
        
        elif StateClicked.get() == "Oklahoma" or StateClicked.get() == "OK":
            sql = """SELECT * FROM Oklahoma"""
        
        elif StateClicked.get() == "Oregon" or StateClicked.get() == "OR":
            sql = """SELECT * FROM Oregon"""
        
        elif StateClicked.get() == "Pennsylvania" or StateClicked.get() == "PA":
            sql = """SELECT * FROM Pennsylvania"""
        
        elif StateClicked.get() == "Rhode Island" or StateClicked.get() == "RI":
            sql = """SELECT * FROM 'Rhode Island'"""

        elif StateClicked.get() == "South Carolina" or StateClicked.get() == "SC":
            sql = """SELECT * FROM 'South Carolina'"""
        
        elif StateClicked.get() == "South Dakota" or StateClicked.get() == "SD":
            sql = """SELECT * FROM 'South Dakota'"""
        
        elif StateClicked.get() == "Tennessee" or StateClicked.get() == "TN":
            sql = """SELECT * FROM Tennessee"""
        
        elif StateClicked.get() == "Texas" or StateClicked.get() == "TX":
            sql = """SELECT * FROM Texas"""
        
        elif StateClicked.get() == "Utah" or StateClicked.get() == "UT":
            sql = """SELECT * FROM Utah"""
        
        elif StateClicked.get() == "Vermont" or StateClicked.get() == "VT":
            sql = """SELECT * FROM Vermont"""
        
        elif StateClicked.get() == "Virginia" or StateClicked.get() == "VA":
            sql = """SELECT * FROM Virginia"""
        
        elif StateClicked.get() == "Washington" or StateClicked.get() == "WA":
            sql = """SELECT * FROM Washington"""
        
        elif StateClicked.get() == "West Virginia" or StateClicked.get() == "WV":
            sql = """SELECT * FROM 'West Virginia'"""
        
        elif StateClicked.get() == "Wisconsin" or StateClicked.get() == "WI":
            sql = """SELECT * FROM Wisconsin"""
        
        elif StateClicked.get() == "Wyoming" or StateClicked.get() == "WY":
            sql = """SELECT * FROM Wyoming"""

        #Connect to db and set selectable county list to counties based on state.
        conn = sqlite3.connect("Counties.db")
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()
        cur.execute(sql)   
        result = cur.fetchall()
        CountySelections.config(value=result)
        

    #Function to display Covid data.
    def dataPage(self, county, state):
        self.bind('<Escape>', lambda e: [self.destroy(), sys.exit()])
        State = state.get()
        County = county.get()
        #Create reset search button
        resetButton = Button(self, text = "Reset Search",  font = ("Playfair 12 bold"), command= self.covidDataLookup)
        resetButton.grid(row=4, column=0, columnspan=4)

        #Pull from CDC.gov for covid data of the previous day.
        try:
            api_request = requests.get(
                #this gets the state, county, and the data of the previous date. This will make it easier to locate a specific data.
                # CDC website always uses the previous date as the most recent data.
                # The date will change automatically.
                "https://data.cdc.gov/resource/8396-v7yb.json?$where=(county_name%20=%20%27" + County +"%27)%20AND%20state_name%20=%20%27"+ State +"%27%20AND%20report_date=%27" + (datetime.now() - timedelta(1)).strftime('%Y-%m-%d') + "%27")

            api = json.loads(api_request.content)
            record = api[0]

            global cases
            cases = DoubleVar(self, name = "double")

            #to filter the search, we use index zero to locate one item of the API.
            state = api[0]['state_name']
            county = api[0]['county_name']
            casesNum = api[0]['cases_per_100k_7_day_count']
            self.setvar(name = "double", value = casesNum)
            community_transmission = api[0]['community_transmission_level']

            if 'percent_test_results_reported' in record:
                percent = api[0]['percent_test_results_reported']
                percent = "%" + percent
            else:
                percent = "Not reported"

            #Set transmission color based on CDC trasmission level    
            if community_transmission == "high":
                transmission_color = "#eb4034" #red
            elif community_transmission == "substantial":
                transmission_color = "#eb9334" #orange
            elif community_transmission == "moderate":
                transmission_color = "#ebd034" #yellow
            elif community_transmission == "low":
                transmission_color = "#34b7eb" #blue

        except Exception as e:
                api = "Error..."

        #Pull from CDC.gov for covid data of the previous week
        try:
            api_request2 = requests.get(
                "https://data.cdc.gov/resource/8396-v7yb.json?$where=(county_name%20=%20%27" + County +"%27)%20AND%20state_name%20=%20%27"+ State +"%27%20AND%20report_date=%27" + (datetime.now() - timedelta(8)).strftime('%Y-%m-%d') + "%27")
            api2 = json.loads(api_request2.content)

            global casesMinus1Week
            casesMinus1Week = DoubleVar(self, name = "double2")
            casesNum_minus1Week = api2[0]['cases_per_100k_7_day_count']
            self.setvar(name = "double2", value = casesNum_minus1Week)

        
        except Exception as e:
            api = "Error..."
        #Pull from CDC.gov for covid data from 2 previous weeks
        try:
            api_request3 = requests.get(
                "https://data.cdc.gov/resource/8396-v7yb.json?$where=(county_name%20=%20%27" + County +"%27)%20AND%20state_name%20=%20%27"+ State +"%27%20AND%20report_date=%27" + (datetime.now() - timedelta(15)).strftime('%Y-%m-%d') + "%27")
            api3 = json.loads(api_request3.content)

            global casesMinus2Weeks
            casesMinus2Weeks = DoubleVar(self, name = "double3")
            casesNum_minus2Week = api3[0]['cases_per_100k_7_day_count']
            self.setvar(name = "double3", value = casesNum_minus2Week)
            

        except Exception as e:
            api = "Error..."

        #Pull from CDC.gov for covid data from 3 previous weeks
        try:
            api_request4 = requests.get(
                "https://data.cdc.gov/resource/8396-v7yb.json?$where=(county_name%20=%20%27" + County +"%27)%20AND%20state_name%20=%20%27"+ State +"%27%20AND%20report_date=%27" + (datetime.now() - timedelta(22)).strftime('%Y-%m-%d') + "%27")
            api4 = json.loads(api_request4.content)

            has_content = bool(api4)

            #Check if api has content.  If not, messagebox pop-up
            if not has_content:
                messagebox.showinfo("Error", "Oops! Looks like you forgot to enter a state or county. \nPlease try again.")
                self.after(10, lambda: self.covidDataLookup())
            else:
                global casesMinus3Weeks
                casesMinus3Weeks = DoubleVar(self, name = "double4")
                casesNum_minus3Week = api4[0]['cases_per_100k_7_day_count']
                self.setvar(name = "double4", value = casesNum_minus3Week)

                #If cases reported are 0 or suppressed display message pop-up
                if (casesNum == 'suppressed' or casesNum == "0.000") or (casesNum_minus1Week == 'suppressed' or casesNum_minus1Week =="0.000") or (casesNum_minus2Week == 'suppressed' or casesNum_minus2Week =="0.000") or (casesNum_minus3Week == 'suppressed' or casesNum_minus3Week == "0.000"):
                    messagebox.showinfo("Error", "Sorry, there is no data for that county. \nCovid positive cases are suppressed in that area.\nPlease search a different area.")
                    self.after(10, lambda: self.covidDataLookup())
                else:
                    #Create frame that sets the background color to the community transmision level color.
                    frame1 = Frame(self, bg=transmission_color, width=1000, height=750)
                    frame1.grid(row =3, column=0, columnspan=4)
                    frame1.grid_propagate(False)
                    
                    #output to user.
                    myLabel = tk.Label(frame1, text= "Community Transmission is: " + str(community_transmission) + "\nPercent Positivity: " + str(percent), 
                                            font=("Playfair", 16), background= "white", borderwidth=2, relief="solid")
                    myLabel.place(relx=0.5, rely=0.06, anchor=CENTER)
                    

                    #Create figure
                    fig = plt.figure(figsize=(8,6), dpi=100, facecolor= transmission_color)

                    #Data includes dates:pos cases per 100k
                    data = {(datetime.now() - timedelta(22)).strftime('%Y-%m-%d'):casesMinus3Weeks.get(), (datetime.now() - timedelta(15)).strftime('%Y-%m-%d'): casesMinus2Weeks.get(),
                    (datetime.now() - timedelta(8)).strftime('%Y-%m-%d'):casesMinus1Week.get(), (datetime.now() - timedelta(1)).strftime('%Y-%m-%d'):cases.get()}

                    dates = list(data.keys())
                    posCases = list(data.values())

                    #Display number of cases above each bar per week.
                    for index, datapoints in enumerate(posCases):
                        plt.text(x=index, y=datapoints, s=f"{datapoints}", fontdict=dict(fontsize =10), ha = 'center', va='bottom')

                    #Create Bar Graph
                    plt.bar(dates, posCases, width= 0.6, color=['#afafaf','#c7bbc9','#c0c2ce','#a2d2df'])
                    plt.xticks(rotation=30, horizontalalignment = "center", weight='bold')
                    plt.yticks(weight='bold')
                    plt.ylabel("Number of cases per 100k in 7 days", weight='bold')

                    #Place graph on page
                    canvasbar = FigureCanvasTkAgg(fig, master = self)
                    canvasbar.draw()
                    canvasbar.get_tk_widget().grid(row =3, column=0, columnspan=4)

                    #Create a legend for the background color - indicating community transmission            
                    frame = Frame(self, bg="white", width=170, height=215)
                    frame.grid(row =3, column=3, padx=30, sticky=tk.E)
                    frame.grid_propagate(False)

                    label = Label(frame, text = "Community Transmission", font=("Arial 10 bold"), bg="white")
                    label.grid(row =0, column=0, columnspan= 2, pady=5, sticky=tk.EW)

                    frame2 = Frame(frame, bg="#eb4034", width=25, height=25, highlightbackground="black", highlightthickness=2)
                    frame2.grid(row =1, column=0, sticky=tk.W, pady=10, padx=10)
                    frame2.grid_propagate(False)

                    label2 = Label(frame, text = "High", font=("Arial 10 bold"), bg="white")
                    label2.grid(row =1, column=1, sticky=tk.W)

                    frame3 = Frame(frame, bg="#eb9334", width=25, height=25, highlightbackground="black", highlightthickness=2)
                    frame3.grid(row =2, column=0,  sticky=tk.W, padx=10)
                    frame3.grid_propagate(False)

                    label3 = Label(frame, text = "Substantial", font=("Arial 10 bold"), bg="white")
                    label3.grid(row =2, column=1, sticky=tk.W)

                    frame4 = Frame(frame, bg="#ebd034", width=25, height=25, highlightbackground="black", highlightthickness=2)
                    frame4.grid(row =3, column=0, sticky=tk.W, pady=10, padx=10)
                    frame4.grid_propagate(False)

                    label4 = Label(frame, text = "Moderate", font=("Arial 10 bold"), bg="white")
                    label4.grid(row =3, column=1, sticky=tk.W)

                    frame5 = Frame(frame, bg="#34b7eb", width=25, height=25, highlightbackground="black", highlightthickness=2)
                    frame5.grid(row =4, column=0, sticky=tk.W, padx=10)
                    frame5.grid_propagate(False)

                    label5 = Label(frame, text = "Low", font=("Arial 10 bold"), bg="white")
                    label5.grid(row =4, column=1, sticky=tk.W)
                    
                    
        except Exception as e:
            api = "Error..."


    def vaxLookUp(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(background="#002366")

        HomeButton = tk.Button(self, fg= "white", bg = "green", text = "Home", font = ("Playfair 16 bold"), width=16, command = self.homePage)
        HomeButton.grid(row =0, column= 0)

        VaxTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Vaccination Tracker", font = ("Playfair 16 bold"))
        VaxTrackButton.grid(row =0, column= 1)

        VaxCardButton = tk.Button(self, fg= "white", bg = "green", text = "Upload Vaccination Card", font = ("Playfair 16 bold"), command = self.uploadPage)
        VaxCardButton.grid(row =0, column= 2) 

        DataTrackButton = tk.Button(self, fg= "white", bg = "green", text = "Covid-19 Data Tracker", font = ("Playfair 16 bold"), command = self.covidDataLookup)
        DataTrackButton.grid(row =0, column= 3)


        #Create State selectable option
        global StateClicked
        StateClicked = StringVar()
        StateClicked.set( "Select State" )

        States =['AL','AK', 'AZ','AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI','ID', 'IL','IN','IA', 'KS', 'KY', 'LA', 'ME','MD','MA',
            'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
            'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
            'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
        
        global StateSelections
        StateSelections = ttk.Combobox(self, value = States, textvariable=StateClicked, width = 25, font="Playfair 18", state="readonly") 
        StateSelections.grid(row =2, column=0, sticky=tk.E)
        StateSelections.bind("<<ComboboxSelected>>", self.pick_state)

        #Create County selectable option
        CountyClicked = StringVar()
        CountyClicked.set("Select County")

        global CountySelections
        CountySelections = ttk.Combobox(self, value=[" "], textvariable=CountyClicked, width = 25, font="Playfair 18", state="readonly") 
        CountySelections.grid(row =2, column=2, sticky= tk.W)
        
        #Button to load data based on State and County input.
        checkVaxButton = Button(self, fg= "white", bg = "green", text = "Check \n Vaccination \n Rate", font = ("Playfair 12 bold"), command= lambda: [self.vaxData(StateClicked,CountyClicked), 
                 CountySelections.destroy(), StateSelections.destroy(), checkVaxButton.destroy()])
        checkVaxButton.grid(row =2, column=3, sticky = tk.W, columnspan=2)


    def vaxData(self, state, county):
        self.bind('<Escape>', lambda e: [self.destroy(), sys.exit()])
        #Create reset search button
        resetButton = Button(self, text = "Reset Search",  font = ("Playfair 12 bold"),command= self.vaxLookUp)
        resetButton.grid(row=4, column=0, columnspan=4)
        State = state.get()
        County = county.get()
        #Pull from CDC.gov for vaccination data of the previous day.
        try:
            api_request = requests.get(
                #this gets the state, county, and the data of the previous date. This will make it easier to locate a specific data.
                # CDC website always uses the previous date as the most recent data.
                # The date will change automatically.
                "https://data.cdc.gov/resource/8xkx-amqh.json?$where=(recip_county%20=%20%27" + County +"%27)%20AND%20recip_state%20=%20%27" + State + "%27%20AND%20date%20=%20%27" + (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')+"%27")
            api = json.loads(api_request.content)

            has_content = bool(api)

            #Check if api has content.  If not, messagebox pop-up
            if not has_content:
                messagebox.showinfo("Error", "Oops! Looks like you forgot to enter a state or county. \nPlease try again.")
                self.after(10, lambda: self.vaxLookUp())
            else:
                global seriesCompletePercent
                seriesCompletePercent = DoubleVar(self, name = "double")
                global firstDosePercent
                firstDosePercent = DoubleVar(self, name = "double2")
                global boosterReceivedPercent
                boosterReceivedPercent = DoubleVar(self, name = "double3")

                #to filter the search, we use index zero to locate one item of the API.
                state = api[0]['recip_state']
                county = api[0]['recip_county']

                #Dose 1 Received
                firstVax_pct = api[0]['administered_dose1_pop_pct']
                self.setvar(name = "double2", value = firstVax_pct)

                #2 Doses completed
                seriesComplete_pct = api[0]['series_complete_pop_pct']
                self.setvar(name = "double", value = seriesComplete_pct)

                #Booster dose received
                boosterVaxNum_pct = api[0]['booster_doses_vax_pct']
                self.setvar(name = "double3", value = boosterVaxNum_pct)


                #Set background variable color based on CDC fully vaccinated
                if seriesComplete_pct >= str(70.0):
                    vax_color = "#00008b" #navy blue
                elif seriesComplete_pct == str(69.9):
                    vax_color = "#187BDC" #blue
                elif seriesComplete_pct > str(49.9) and seriesComplete_pct < str(69.9):
                    vax_color = "#187BDC"  # blue
                elif seriesComplete_pct == str(49.9):
                    vax_color = "#89D5D2" #light teal
                elif seriesComplete_pct > str(39.9) and seriesComplete_pct < str(49.9):
                    vax_color = "#89D5D2" #light teal
                elif seriesComplete_pct == str(39.9):
                    vax_color = "#C1E1C1" #pastel green
                elif seriesComplete_pct > str(29.9) and seriesComplete_pct < str(39.9):
                    vax_color = "#C1E1C1" #pastel green
                elif seriesComplete_pct == str(29.9):
                    vax_color = "#FFFAF1" #off white
                elif seriesComplete_pct < str(29.9):
                    vax_color = "#FFFAF1" #off white
                
                #Create a legend for the background color - indicating percent of county fully vaccinated           
                frame = Frame(self, bg="white", width=150, height=250)
                frame.grid(row =3, column=3, padx=30, sticky=tk.E)
                frame.grid_propagate(False)

                label = Label(frame, text = " % of Population Fully \n Vaccinated", font=("Arial 10 bold"), bg="white")
                label.grid(row =0, column=0, columnspan= 2, pady=5, sticky=tk.EW)

                frame2 = Frame(frame, bg="#00008b", width=25, height=25, highlightbackground="black", highlightthickness=2)
                frame2.grid(row =1, column=0, sticky=tk.W, pady=10, padx=10)
                frame2.grid_propagate(False)

                label2 = Label(frame, text = "70%+", font=("Arial 10 bold"), bg="white")
                label2.grid(row =1, column=1, sticky=tk.W)

                frame3 = Frame(frame, bg="#187BDC", width=25, height=25, highlightbackground="black", highlightthickness=2)
                frame3.grid(row =2, column=0,  sticky=tk.W, padx=10)
                frame3.grid_propagate(False)

                label3 = Label(frame, text = "50-69.9%", font=("Arial 10 bold"), bg="white")
                label3.grid(row =2, column=1, sticky=tk.W)

                frame4 = Frame(frame, bg="#89D5D2", width=25, height=25, highlightbackground="black", highlightthickness=2)
                frame4.grid(row =3, column=0, sticky=tk.W, pady=10, padx=10)
                frame4.grid_propagate(False)

                label4 = Label(frame, text = "40-49.9%", font=("Arial 10 bold"), bg="white")
                label4.grid(row =3, column=1, sticky=tk.W)

                frame5 = Frame(frame, bg="#C1E1C1", width=25, height=25, highlightbackground="black", highlightthickness=2)
                frame5.grid(row =4, column=0, sticky=tk.W, padx=10)
                frame5.grid_propagate(False)

                label5 = Label(frame, text = "30-39.9%", font=("Arial 10 bold"), bg="white")
                label5.grid(row =4, column=1, sticky=tk.W)
                
                frame6 = Frame(frame, bg="#FFFAF1", width=25, height=25, highlightbackground="black", highlightthickness=2)
                frame6.grid(row =5, column=0, sticky=tk.W, pady=10, padx=10)
                frame6.grid_propagate(False)

                label6 = Label(frame, text = "0-29.9%", font=("Arial 10 bold"), bg="white")
                label6.grid(row =5, column=1, sticky=tk.W)


                #Create Pie Chart
                data = {'2 Doses Administered': seriesCompletePercent.get(),'Only 1 Dose \nAdministered':(firstDosePercent.get() - seriesCompletePercent.get()), '0 Doses Administered': (100 - firstDosePercent.get())}

                labels = list(data.keys())
                percentData = list(data.values())
                            #green,    orange,      red
                colors = ("#04d142",  "#db8c04", "#db3604")
                #Create figure
                fig, ax = plt.subplots(figsize=(7,5), facecolor= vax_color)
                ax.pie(percentData, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90, textprops = dict(weight='bold'), colors=colors)
                #Place pie chart on screen
                canvasbar = FigureCanvasTkAgg(fig, master = self)
                canvasbar.draw()
                canvasbar.get_tk_widget().grid(row =3, column=0, columnspan=2)



                #Create Bar Chart
                fig2, ax2 = plt.subplots(figsize=(7,5), dpi=100, facecolor= vax_color)
                data2 = {'Booster Dose Administered':boosterReceivedPercent.get()}

                labels2 = list(data2.keys())
                percentData2 = list(data2.values())
                #Display percent of population recieved booster dose above bar
                for index, datapoints in enumerate(percentData2):
                    plt.text(x=index, y=datapoints, s=f"{datapoints}", fontdict=dict(fontsize =10), ha = 'center', va='bottom')
                #Create figure
                ax2.bar(labels2, percentData2, width= 0.6, color= '#262626')
                ax2.set_xlim(-1,1)
                plt.xticks( horizontalalignment = "center", weight='bold')
                plt.yticks(weight='bold')
                plt.ylabel("Percent of the Population", weight='bold')
                #Place bar chart on screen
                canvasbar2 = FigureCanvasTkAgg(fig2, master = self)
                canvasbar2.draw()
                canvasbar2.get_tk_widget().grid(row =3, column=2, columnspan=2, sticky=tk.W)

        except Exception as e:
            api = "Error..."

        
if __name__ == "__main__":
    app = CovidApp()
    app.mainloop()
