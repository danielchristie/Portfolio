#!/usr/bin/python3
#Author:    Daniel Christie
#Topic:     The Tech Academy - Python Course: Drill 68
#Purpose:   Check for all .txt files in source folder that have been created
#           or modified with a 24 hour period and move those files into their
#           destination folder.
#           Tkinter GUI with listboxes, file dialogs, and SQL database access.

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3


def dbConnect():
    # Connect to database
    conn = sqlite3.connect('dbFileCheck.db')

    # Create table named webpages
    conn.execute("CREATE TABLE if not exists tblFileCheck( \
        ID INTEGER PRIMARY KEY AUTOINCREMENT, \
        colDate FLOAT, \
        colFile TEXT \
        );")

    # Save changes & close the database connection
    conn.commit()
    conn.close()


def centerScreen():
    #Get the app's dimensions
    width = root.winfo_width()
    height = root.winfo_height()
    #Get user's screen dimensions and calculate from the app's dimensions
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    #Assign the return to the geometry manager
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))


#============================Paint the GUI=========================================
root = Tk()
root.title("File Check  &  Move Demo")
root.minsize(width = 450, height = 400)
#root.maxsize(width = 800, height = 800)

centerScreen()
#dbConnect()
    
    
#Adding Labels to the GUI
lblLast = Label(root, text = "Last Check Date:").grid(row = 0, column = 0, padx = 10, pady = 0, sticky = W+E)
lblDate = Label(root, text = "10/10/10 14:55").grid(row = 0, column = 1, columnspan = 3, padx = 10, pady = 0, sticky = W+E)
lblSrc = Label(root, text = "Source Path:").grid(row = 3, column = 0, padx = 10, pady = 1, sticky = W)
lblDst = Label(root, text = "Destination:").grid(row = 4, column = 0, padx = 10, pady = 1, sticky = W)

#Define the text boxes & Paint them
txtSrc = Entry(root, width = 40)
txtSrc.grid(row = 3, column = 1, columnspan = 2, padx = 0, pady = 0, sticky = W)
txtDst = Entry(root, width = 40)
txtDst.grid(row = 4, column = 1, columnspan = 2, padx = 0, pady = 0, sticky = W)


#Define the treeview with a scrollbar & paint them
scrollbar1 = Scrollbar(root, orient=VERTICAL)

tree1 = ttk.Treeview(root, yscrollcommand = scrollbar1.set)
tree1.bind('<<ListboxSelect>>')#, onSelect)
scrollbar1.config(command = tree1.yview)
scrollbar1.grid(row = 1, column = 4, rowspan = 2, columnspan = 1, padx = 0, pady = 0, sticky = N+S+W)
tree1.grid(row = 1, column = 0, rowspan = 2, columnspan = 3, padx = 15, pady = 10, sticky = N+E+S+W)

tree1.insert('', '0', 'column1', text = 'Dates:')


#Define buttons & paint them
btnConfig = Button(root, text = "Configure", width = 10, height = 2, command = "")
btnConfig.grid(row = 5, column = 0, padx = 10, pady = 15, sticky = W)
btnCheck = Button(root, text = "Check Files", width = 10, height = 2, command = "")
btnCheck.grid(row = 5, column = 1, padx = 10, pady = 15, sticky = W)
btnClose = Button(root, text = "       Close       ", width = 10, height = 2, command = "")
btnClose.grid(row = 5, column = 2, padx = 0, pady = 15, sticky = E)


#onRefresh()

root.mainloop()
