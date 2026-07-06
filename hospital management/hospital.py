import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import mysql.connector

class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1540x800+0+0")

        # ====== Variables ======
        self.NameofTablets = StringVar()
        self.ref = StringVar()
        self.Dose = StringVar()
        self.NumberofTablets = StringVar()
        self.IssueDate = StringVar()
        self.ExpDate = StringVar()
        self.DailyDose = StringVar()
        self.sideEffects = StringVar()
        self.FurtherInformation = StringVar()
        self.Bloodpressure = StringVar()
        self.PatientId = StringVar()
        self.nhsNumber = StringVar()
        self.PatientName = StringVar()
        self.DateOfBirth = StringVar()
        self.PatientAddress = StringVar()
      

        # ====== Title Label ======
        lbltitle = tk.Label(self.root, bd=20, relief=tk.RIDGE, text="HOSPITAL MANAGEMENT SYSTEM",
                            fg="red", bg="white", font=("times new roman", 40, "bold"))
        lbltitle.pack(side=tk.TOP, fill=tk.X)

        # ====== Main Frames ======
        Dataframe = Frame(self.root, bd=20, relief=RIDGE)
        Dataframe.place(x=0, y=130, width=1530, height=400)

        DataframeLeft = LabelFrame(Dataframe, bd=10, relief=RIDGE, padx=10,
                                   font=("times new roman", 14, "bold"), text="Patient Information")
        DataframeLeft.place(x=0, y=5, width=980, height=350)

        DataframeRight = LabelFrame(Dataframe, bd=10, relief=RIDGE, padx=10,
                                    font=("times new roman", 14, "bold"), text="Prescription")
        DataframeRight.place(x=990, y=5, width=460, height=350)

        Buttonframe = Frame(self.root, bd=20, relief=RIDGE)
        Buttonframe.place(x=0, y=530, width=1530, height=70)

        Detailsframe = Frame(self.root, bd=20, relief=RIDGE)
        Detailsframe.place(x=0, y=600, width=1530, height=190)

        # ====== DataframeLeft Inputs ======
        lblNameTablet = Label(DataframeLeft, font=("arial", 12, "bold"), text="Name Of Tablets", padx=2, pady=6)
        lblNameTablet.grid(row=0, column=0, sticky=W)

        comNameTablet = ttk.Combobox(DataframeLeft, textvariable=self.NameofTablets, state="readonly",
                                     font=("arial", 12, "bold"), width=33)
        comNameTablet["value"] = ("Nice", "Corona Vaccine", "Acetaminophen", "Adderall", "Amlodipine", "Ativan")
        comNameTablet.current(0)
        comNameTablet.grid(row=0, column=1)

        lblref = Label(DataframeLeft, font=("arial", 12, "bold"), text="Reference No:", padx=2)
        lblref.grid(row=1, column=0, sticky=W)
        txtref = Entry(DataframeLeft, font=("arial", 12, "bold"), textvariable=self.ref, width=35)
        txtref.grid(row=1, column=1)

        lblDose = Label(DataframeLeft, font=("arial", 12, "bold"), text="Dose:", padx=2, pady=4)
        lblDose.grid(row=2, column=0, sticky=W)
        txtDose = Entry(DataframeLeft, font=("arial", 12, "bold"), textvariable=self.Dose, width=35)
        txtDose.grid(row=2, column=1)

        lblNOOftablets = Label(DataframeLeft, font=("arial", 12, "bold"), text="No Of Tablets:", padx=2, pady=6)
        lblNOOftablets.grid(row=3, column=0, sticky=W)
        txtNOOftablets = Entry(DataframeLeft, font=("arial", 12, "bold"), textvariable=self.NumberofTablets, width=35)
        txtNOOftablets.grid(row=3, column=1)

        lblIssueDate = Label(DataframeLeft, font=("arial", 12, "bold"), text="Issue Date:", padx=2, pady=6)
        lblIssueDate.grid(row=4, column=0, sticky=W)
        txtIssueDate = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.IssueDate, width=35)
        txtIssueDate.grid(row=4, column=1)

        lblExpDate = Label(DataframeLeft, font=("arial", 12, "bold"), text="Exp Date:", padx=2, pady=6)
        lblExpDate.grid(row=5, column=0, sticky=W)
        txtExpDate = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.ExpDate, width=35)
        txtExpDate.grid(row=5, column=1)

        lblDailyDose = Label(DataframeLeft, font=("arial", 12, "bold"), text="Daily Dose:", padx=2, pady=4)
        lblDailyDose.grid(row=6, column=0, sticky=W)
        txtDailyDose = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.DailyDose, width=35)
        txtDailyDose.grid(row=6, column=1)

        lblSideEffect = Label(DataframeLeft, font=("arial", 12, "bold"), text="Side Effect:", padx=2, pady=6)
        lblSideEffect.grid(row=7, column=0, sticky=W)
        txtSideEffect = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.sideEffects, width=35)
        txtSideEffect.grid(row=7, column=1)
        
        lblFurtherInfo = Label(DataframeLeft, font=("arial", 12, "bold"), text="Further Information:", padx=2)
        lblFurtherInfo.grid(row=0, column=2, sticky=W)
        txtFurtherInfo = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.FurtherInformation, width=35)
        txtFurtherInfo.grid(row=0, column=3)

        lblBloodPressure = Label(DataframeLeft, font=("arial", 12, "bold"), text="Blood Pressure:", padx=2)
        lblBloodPressure.grid(row=1, column=2, sticky=W)
        txtBloodPressure = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.Bloodpressure, width=35)
        txtBloodPressure.grid(row=1, column=3)

        lblPatientId = Label(DataframeLeft, font=("arial", 12, "bold"), text="Patient Id:", padx=2, pady=6)
        lblPatientId.grid(row=2, column=2, sticky=W)
        txtPatientId = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.PatientId, width=35)
        txtPatientId.grid(row=2, column=3)

        lblNhsNumber = Label(DataframeLeft, font=("arial", 12, "bold"), text="NHS Number", padx=2, pady=6)
        lblNhsNumber.grid(row=3, column=2, sticky=W)
        txtNhsNumber = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.nhsNumber, width=35)
        txtNhsNumber.grid(row=3, column=3)
        
        lblPatientname = Label(DataframeLeft, font=("arial", 12, "bold"), text="Patient Name", padx=2, pady=6)
        lblPatientname.grid(row=4, column=2, sticky=W)
        txtPatientname = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.PatientName, width=35)
        txtPatientname.grid(row=4, column=3)
        
        lblDateOfBirth = Label(DataframeLeft, font=("arial", 12, "bold"), text="Date Of Birth", padx=2, pady=6)
        lblDateOfBirth.grid(row=5, column=2, sticky=W)
        txtDateOfBirth = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.DateOfBirth, width=35)
        txtDateOfBirth.grid(row=5, column=3)

        lblPatientAddress = Label(DataframeLeft, font=("arial", 12, "bold"), text="Patient Address", padx=2, pady=6)
        lblPatientAddress.grid(row=6, column=2, sticky=W)
        txtPatientAddress = Entry(DataframeLeft, font=("arial", 12, "bold"),textvariable=self.PatientAddress, width=35)
        txtPatientAddress.grid(row=6, column=3)

        #====================dataframe right=======================

        self.txtPrescription = Text(DataframeRight, font=("arial", 12, "bold"), width=45, height=16, padx=2, pady=6)
        self.txtPrescription.grid(row=0, column=0)

        # ===============================Buttons================================
        btnPrescription = Button(Buttonframe,command=self.iprescription,text="Prescription",bg="green",fg="white", font=("arial", 12, "bold"), width=23, height=1, padx=2, pady=6)
        btnPrescription.grid(row=0,column=0)
        
        btnPrescriptiondata= Button(Buttonframe,command=self.adddata, text="Add data",bg="green",fg="white", font=("arial", 12, "bold"), width=23, height=1, padx=2, pady=6)
        btnPrescriptiondata.grid(row=0,column=1)

        btnupdate = Button(Buttonframe, command=self.update,text="Update",bg="green",fg="white", font=("arial", 12, "bold"), width=23, height=1, padx=2, pady=6)
        btnupdate.grid(row=0,column=2)
      
        btndelete= Button(Buttonframe,command=self.idelete, text="Delete",bg="green",fg="white", font=("arial", 12, "bold"), width=23, height=1, padx=2, pady=6)
        btndelete.grid(row=0,column=3)

        btnclear = Button(Buttonframe,command=self.clear, text="Clear",bg="green",fg="white", font=("arial", 12, "bold"), width=23, height=1, padx=2, pady=6)
        btnclear.grid(row=0,column=4)
 
        btnExit = Button(Buttonframe,command=self.iExit, text="Exit",bg="green",fg="white", font=("arial", 12, "bold"), width=23, height=1, padx=2, pady=6)
        btnExit.grid(row=0,column=5)

        #=======================Table============================
        #=====================scrollbar==========================

       
        scroll_x = ttk.Scrollbar(Detailsframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Detailsframe, orient=VERTICAL)
        self.hospital_table = ttk.Treeview(Detailsframe, columns=("nameoftablets", "ref","dose","nooftablets","issuedate",
                                      "expdate","dailydose","nhsnumber","pname","dob","address"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)


        scroll_x=ttk.Scrollbar(Detailsframe, orient=HORIZONTAL, command=self.hospital_table.xview)
        scroll_y=ttk.Scrollbar(Detailsframe, orient=VERTICAL, command=self.hospital_table.yview)

        self.hospital_table.heading("nameoftablets",text="Name of tablets")
        self.hospital_table.heading("ref",text="Reference No.")
        self.hospital_table.heading("dose",text="Dose")
        self.hospital_table.heading("nooftablets",text="No of Tablets")
        self.hospital_table.heading("issuedate",text="Issue Date")
        self.hospital_table.heading("expdate",text="Exp Date")
        self.hospital_table.heading("dailydose",text="Daily dose")
        self.hospital_table.heading("nhsnumber",text="NHS Number")
        self.hospital_table.heading("pname",text="Patient Name")
        self.hospital_table.heading("dob",text="DOB")
        self.hospital_table.heading("address",text="Address")

        self.hospital_table["show"]="headings"

        self.hospital_table.column("nameoftablets",width=100)
        self.hospital_table.column("ref",width=100)
        self.hospital_table.column("dose",width=100)
        self.hospital_table.column("nooftablets",width=100)
        self.hospital_table.column("issuedate",width=100)
        self.hospital_table.column("expdate",width=100)
        self.hospital_table.column("dailydose",width=100)
        self.hospital_table.column("nhsnumber",width=100)
        self.hospital_table.column("pname",width=100)
        self.hospital_table.column("dob",width=100)
        self.hospital_table.column("address",width=100)

        self.hospital_table.pack(fill=BOTH,expand=1)
        self.hospital_table.bind("<ButtonRelease-1>", self.get_cursor)



        try:
            self.fetch_data()
        except Exception as e:
            messagebox.showwarning("Database Warning", f"Could not load data: {e}")

    #==========================Functionality Declaration=========================
    def adddata(self):
        required_fields = [
        self.NameofTablets.get(),
        self.ref.get(),
        self.NumberofTablets.get(),
        self.IssueDate.get(),
        self.ExpDate.get(),
        self.DailyDose.get(),
        self.nhsNumber.get(),
        self.PatientName.get(),
        self.DateOfBirth.get(),
         self.PatientAddress.get()
    ]
        if any(field == "" for field in required_fields):
            messagebox.showerror("Error","All fields are required")
        else: 
            conn=mysql.connector.connect(host="localhost",user="root",password="aman123",database="mydata")
            my_cursor=conn.cursor()
            my_cursor.execute("insert into hospital values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                                 self.NameofTablets.get(),
                                                                                                 self.ref.get(),
                                                                                                 self.Dose.get(),
                                                                                                 self.NumberofTablets.get(),
                                                                                                 self.IssueDate.get(),
                                                                                                 self.ExpDate.get(),
                                                                                                 self.DailyDose.get(),
                                                                                                 self.nhsNumber.get(),
                                                                                                 self.PatientName.get(),
                                                                                                 self.DateOfBirth.get(),
                                                                                                 self.PatientAddress.get()
                                                                                                 ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("success","Record has been inserted")

    def update(self):
        conn=mysql.connector.connect(host="localhost",user="root",password="aman123",database="mydata")
        my_cursor=conn.cursor()
        my_cursor.execute("update hospital set NameofTablets=%s,Dose=%s,NumberofTablets=%s,IssueDate=%s,ExpDate=%s,DailyDose=%s,nhsNumber=%s,PatientName=%s,DateOfBirth=%s,PatientAddress=%s where ref=%s",(
            self.NameofTablets.get(),
            self.Dose.get(),
            self.NumberofTablets.get(),
            self.IssueDate.get(),
            self.ExpDate.get(),
            self.DailyDose.get(),
            self.nhsNumber.get(),
            self.PatientName.get(),
            self.DateOfBirth.get(),
            self.PatientAddress.get(),
            self.ref.get()
        ))
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Update","Record has been updated successfully")



    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",user="root",password="aman123",database="mydata")
        my_cursor=conn.cursor()
        my_cursor.execute("SELECT * FROM mydata.hospital;")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.hospital_table.delete(*self.hospital_table.get_children())
            for i in rows:
                self.hospital_table.insert(" ",END,values=i)
            conn.commit()
        conn.close()    
            

    def get_cursor(self,event=""):
        cursor_row=self.hospital_table.focus()
        content=self.hospital_table.item(cursor_row)
        row=content["values"]
        self.NameofTablets.set(row[0])
        self.ref.set(row[1])
        self.Dose.set(row[2])
        self.NumberofTablets.set(row[3])
        self.IssueDate.set(row[4])
        self.ExpDate.set(row[5])
        self.DailyDose.set(row[6])
        self.nhsNumber.set(row[7])
        self.PatientName.set(row[8])
        self.DateOfBirth.set(row[9])
        self.PatientAddress.set(row[10])

    def iprescription(self):  
        self.txtPrescription.insert(END, "Name of Tablets:\t\t\t" + self.NameofTablets.get() + "\n")
        self.txtPrescription.insert(END, "Reference No:\t\t\t" + self.ref.get() + "\n")
        self.txtPrescription.insert(END, "Dose:\t\t\t" + self.Dose.get() + "\n")
        self.txtPrescription.insert(END, "Number of Tablets:\t\t\t" + self.NumberofTablets.get() + "\n")
        self.txtPrescription.insert(END, "Issue Date:\t\t\t" + self.IssueDate.get() + "\n")
        self.txtPrescription.insert(END, "Exp Date:\t\t\t" + self.ExpDate.get() + "\n")
        self.txtPrescription.insert(END, "Daily Dose:\t\t\t" + self.DailyDose.get() + "\n")
        self.txtPrescription.insert(END, "Side Effect:\t\t\t" + self.sideEffects.get() + "\n")
        self.txtPrescription.insert(END, "Further Information:\t\t\t" + self.FurtherInformation.get() + "\n")
        self.txtPrescription.insert(END, "Blood pressure:\t\t\t" + self.Bloodpressure.get() + "\n")
        self.txtPrescription.insert(END, "Patient Id:\t\t\t" + self.PatientId.get() + "\n")
        self.txtPrescription.insert(END, "NHS Number:\t\t\t" + self.nhsNumber.get() + "\n")
        self.txtPrescription.insert(END, "Patient Name:\t\t\t" + self.PatientName.get() + "\n")
        self.txtPrescription.insert(END, "Date Of Birth:\t\t\t" + self.DateOfBirth.get() + "\n")
        self.txtPrescription.insert(END, "Patient Address:\t\t\t" + self.PatientAddress.get() + "\n")

    def idelete(self):  
        conn=mysql.connector.connect(host="localhost",user="root",password="aman123",database="mydata")
        my_cursor=conn.cursor()
        query="Delete from hospital where  ref=%s" 
        value=(self.ref.get(),)
        my_cursor.execute(query,value)

        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Delete","patient has been deleted succesfully")

    def clear(self):
        self.NameofTablets.set("")
        self.ref.set("")
        self.Dose.set("")
        self.NumberofTablets.set("")
        self.IssueDate.set("")
        self.ExpDate.set("")
        self.DailyDose.set("")
        self.sideEffects.set("")
        self.FurtherInformation.set("")
        self.Bloodpressure.set("")
        self.PatientId.set("")
        self.nhsNumber.set("")
        self.PatientName.set("")
        self.DateOfBirth.set("")
        self.PatientAddress.set("")
        
        self.txtPrescription.delete("1.0", END)

    def iExit(self):
        iExit=messagebox.askyesno("Hospital management system","confirm you want to exit")  
        if iExit>0 :
            self.root.destroy()
            return                        



if __name__ == "__main__":
    root = tk.Tk()
    app = Hospital(root)
    root.mainloop()
