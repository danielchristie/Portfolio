#!/usr/bin/python3
#Author:    Daniel Christie
#Topic:     The Tech Academy - Python Course Drill Shutil.move
#Purpose:   Check a directory for instances of txt files created or modified within
#           a 24 hour period and move those files into another folder
#           Console application with Tkinter as the GUI. Version 2

from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst
import tkinter.messagebox
import shutil
import time
import sqlite3
from datetime import timedelta, datetime
from os import path
import os

# File locations
folders = {'Folder A':{'path':'C:\\A'},
                   'Folder B':{'path':'C:\\B'}}

# Setting the time now to the deadline time of 24 hours
now = datetime.now()
deadline = now + timedelta(hours=-24)

class Feedback:

    def __init__(self, master):

        # connecting to the already created database and table
        conn = sqlite3.connect('dbCheck.db')
        c = conn.cursor()

        # Create table if it does not already exist otherwise do nothing
        c.execute("CREATE TABLE IF NOT EXISTS dateCheck(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT)")
        
        # collecting data from when the last transfer was completed
        c.execute("SELECT COUNT (*) FROM dateCheck")
        row_count = c.fetchone()[0]
        print(row_count)
        if row_count <= 0:
            print("No record found, updating database with missing data")
            # setting parameters to retrieve the date and the time of when the transfer button is clicked
            current = time.time()

            # inserting retrieved time and date of when the transfer button was clicked
            c.execute("INSERT INTO dateCheck (date) VALUES (?)", [current])
            conn.commit()
        c.execute("SELECT (date) FROM dateCheck WHERE id=(SELECT MAX(id) FROM dateCheck)")
        lastDate = c.fetchone()[0]
        print(lastDate)
        lastDate = float(lastDate)
        legibleDate = (datetime.fromtimestamp(lastDate).strftime('%m/%d/%Y %H:%M:%S'))
        conn.commit()
        c.close()

#--------------------------------------------------------------------------

        master.title('Check For New Files...')
        master.resizable(False, False)

        # Instantiating the GUI and color settings
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#d9f3dc')
        self.style.configure('TLabel', background = '#c7f5e5', font = ('Arial', 11))
        self.style.configure('TLabelframe', bg = '000000', bd = 2, width = 40, height = 10)
        
        # window frame
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        # src label & dropdown
        ttk.Label(self.frame_content, text = 'Source Path:', style = 'TLabel').grid(row = 0, column = 0, padx = 10, pady = 2, sticky = 'NW')
        self.origin = ttk.Combobox(self.frame_content)
        self.origin.grid(row = 1, column = 0, padx = 10, sticky = 'NW')
        self.origin.config(values = list(folders.keys()))
    
        # dst label & dropdown
        ttk.Label(self.frame_content, text = 'Destination Path:', style = 'TLabel').grid(row = 2, column = 0, padx = 10, pady = 2, sticky = 'NW')
        self.destination = ttk.Combobox(self.frame_content)
        self.destination.grid(row = 3, column = 0, padx = 10, sticky = 'NW')
        self.destination.config(values = list(folders.keys()))

        # display the last check date of last successful file move 
        ttk.Label(self.frame_content, text = 'Recent File Check:', style = 'TLabel').grid(row = 0, column = 3, padx = 10, pady = 2, sticky = 'NE')
        last_entry = Listbox(self.frame_content, height = 1)
        last_entry.grid(row = 1, column = 3, padx = 10, sticky = 'NE')
        last_entry.insert(1, str(legibleDate))

        # show user of comfirmed file transfer
        self.transfer = ttk.Button(self.frame_content, text='Transfer', style='TButton')
        self.transfer.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'NE')
        self.transfer.bind("<Button-1>", self.transferButtonClicked)
        self.transfer.bind("<Button-1>", self.fileTransfer)
        self.style.configure('TButton', foreground = "#000000", background = '#83f18f')

    # transfer qualified files within a 24hour period
    def fileTransfer(self, event):
        # storing src and dst folders to variables
        self.origin.bind("<<ComboboxSelected>>")
        self.destination.bind("<<ComboboxSelected>>")
        value_of_origin = self.origin.get()
        print(value_of_origin)
        value_of_dest = self.destination.get()
        print(value_of_dest)
        if (value_of_origin == '') or (value_of_dest == ''):
            popupError = tkinter.messagebox.showinfo('Missing file path!', 'Please select both a source and destination path')
        else:
            # retrieve path of the dirs selected
            origin_path = folders[value_of_origin]['path']
            dest_path = folders[value_of_dest]['path'] 
            try:
                for root, dir, files in os.walk(origin_path):
                    # iterate through each file to retrieve the time stamp and pathname
                    for _file in files:
                        pathname = os.path.join(root, _file)
                        modified_time = datetime.fromtimestamp(os.path.getmtime(pathname))
                        # comparing modification time from deadline and moving if appropriate
                        if now >= modified_time >= deadline:
                            print('Files modified within the last 24hours: ' + pathname)
                            shutil.move(pathname, dest_path)
            except Exception as e:
                print(e)
            # console the error that has occured during the file transfer
            else:
                self.transferButtonClicked(event)
            
#---------------------------------------------------------------------------

    def transferButtonClicked(self, event):
        popupComplete = tkinter.messagebox.showinfo('Success!', 'Transfer Completed!')
        self.button_clicked_time = time.time()
        self.dataInsert()
        
#--------------------------------------------------------------------------

    def dataInsert(self):        
        current = time.time()

        conn = sqlite3.connect('dbCheck.db')
        c = conn.cursor()

        c.execute("INSERT INTO dateCheck (date) VALUES (?)", [current])
        conn.commit()

        c.close()
        conn.close()
        
#--------------------------------------------------------------------------
        
def main():
    root = Tk()
    feedback = Feedback(root)
    root.mainloop()

if __name__ == '__main__':
    main()
