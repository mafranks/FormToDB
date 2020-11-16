from tkinter import *
import sqlite3
import datetime as dt
import os
import csv

class StatusReport:

    def __init__(self):
        
        self.root = Tk()
        self.root.geometry('500x500')
        self.root.title("Status Report")
        self.Selector = StringVar()
        self.Message = StringVar()
        self.Status = StringVar()
        self.Operator = StringVar()

    def clear_fields(self):
        self.Selector=StringVar()
        self.Message=StringVar()
        self.Status=StringVar()
        self.display_fields()

    def database(self):
        self.selector=self.Selector.get()
        self.message=self.Message.get()
        self.status=self.Status.get()
        self.operator=self.Operator.get()
        dateTime = dt.datetime.now().isoformat(timespec='seconds')
        with self.conn:
            self.cursor.execute('INSERT INTO Report_Items (DateTime,Selector,Message,Status,Operator) VALUES(?,?,?,?,?)',(dateTime,self.selector,self.message,self.status,self.operator,))
            self.conn.commit()

    def multi_function(self):
        self.database()
        self.clear_fields()

    def display_fields(self):
        entry_1 = Entry(self.root,textvar=self.Selector)
        entry_1.place(x=240,y=130)

        entry_2 = Entry(self.root,textvar=self.Message)
        entry_2.place(x=240,y=180)

        entry_3 = Entry(self.root,textvar=self.Status)
        entry_3.place(x=240,y=230)
        status_list = ['Successful', 'Failed', 'Client Error', 'Server Error']
        droplist_status = OptionMenu(self.root, self.Status, *status_list)
        droplist_status.config(width=15)
        self.Status.set("Select the Status")
        droplist_status.place(x=240,y=230)

        operator_list = ['Matt','Bill','Tom','Jerry','James','Brandon','Frank','Ronda']
        droplist_operator=OptionMenu(self.root,self.Operator, *operator_list)
        droplist_operator.config(width=15)
        self.Operator.set('Select the Operator') 
        droplist_operator.place(x=240,y=280)

    def export_db(self):
        with open('output.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['dateTime','Selector','Message','Status','Operator'])
            with self.conn as temp_conn:
                cursor = temp_conn.cursor()
                cursor.execute("SELECT * FROM Report_Items")
                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow(row)

    def main(self):
        self.conn = sqlite3.connect('StatusReport.db')
        with self.conn:
            self.cursor=self.conn.cursor()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS Report_Items (dateTime TEXT,Selector TEXT,Message TEXT,Status TEXT,Operator TEXT)')
        label_0 = Label(self.root, text="Status Report",width=20,font=("bold", 20))
        label_0.place(x=80,y=53)

        label_1 = Label(self.root, text="Selector",width=20,font=("bold", 10))
        label_1.place(x=80,y=130)

        label_2 = Label(self.root, text="Message",width=20,font=("bold", 10))
        label_2.place(x=82,y=180)

        label_3 = Label(self.root, text="Status",width=20,font=("bold", 10))
        label_3.place(x=74,y=230)

        label_4 = Label(self.root, text="Operator",width=20,font=("bold", 10))
        label_4.place(x=78,y=280)
        self.clear_fields()

        Button(self.root, text='Add to Database',width=20,bg='brown',fg='white',command=self.multi_function).place(x=80,y=380)
        Button(self.root, text='Export Database',width=20,bg='brown',fg='white',command=self.export_db).place(x=280,y=380)

        self.root.mainloop()


StatusReport().main()
