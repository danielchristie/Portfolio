
from Tkinter import *
#from Tkinter import tkMessageBox
import sqlite3

#Paint the GUI
root = Tk()
root.title("Database Demo")
root.minsize(width = 300,height = 300)
root.maxsize(width = 300, height = 300)

#=========================================================
# Connect to database
conn = sqlite3.connect('dbWebPages.db')

# Create table named webpages
conn.execute("CREATE TABLE if not exists tblWebContent( \
    ID INTEGER PRIMARY KEY AUTOINCREMENT, \
    colHead TEXT, \
    colBody TEXT \
    );")

### Add data to the table
##conn.execute("INSERT INTO tblWebContent \
##    (colHead, colBody) VALUES \
##    ('My First Header', 'This is a lot of fun body text')");
##
### Add data to the table
##conn.execute("INSERT INTO tblWebContent \
##    (colHead, colBody) VALUES \
##    ('My Second Header', 'This is still a lot of fun body text')");
##
### Add data to the table
##conn.execute("INSERT INTO tblWebContent \
##    (colHead, colBody) VALUES \
##    ('My Third Header', 'This body text is getting a bit stale now')");

# Save changes & close the database connection
conn.commit()
conn.close()
#=========================================================

#Select item in ListBox
def onSelect(event):
    w = event.widget #ListBox widget
    index = int(w.curselection()[0]) #Index for the highlighted item in the ListBox
    value = w.get(index)
    txtText1.delete (0, END)
    txtText1.insert (0, value)

#Define Listbox & Paint it
lstList1 = Listbox(root)
lstList1.bind('<<ListboxSelect>>', onSelect)
lstList1.pack()

#Define TextEntryBox & Paint it
varText1 = StringVar() #Corresponds with the Entry's txtvar value
txtText1 = Entry(root, textvariable = varText1, width = 200)
txtText1.pack()
varText1.set
varTemp = varText1.get()

#insert text function
def insert():
    varTemp = txtText1.get() 
    if varTemp != "":
        conn = sqlite3.connect('dbWebPages.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO colBody (colBody) VALUES (?)",[varTemp])
            lstList1.insert(END, varTemp)
        conn.close()

    #Error handle when entry widget is empty
    if txtText1.get().strip() == "":
        #messagebox.showerror("ERROR - Missing Data!","Text field is empty, please enter some text.")
        print("ERROR - Missing Data!", "Text field is empty, please enter some text.")
    
    #Delete entry field
    txtText1.delete(0, END)

#Populate the Listbox
conn = sqlite3.connect('dbWebPages.db')
with conn:
    cursor = conn.cursor()
    cursor.execute("SELECT colBody FROM tblWebContent")
    rows = cursor.fetchall()
    m = 0
    mi = 0
    for row in range(len(rows)):
        print("This is the total items in the array or (items in the tuple): {}".format(len(rows)))
        for x in rows:
            print("This is the item in the array or (item in the tuple): {}".format(x[0]))
            z = x[0]
            print("Print z: {}".format(z))
            z = str(z)
            print(type(z))
            varText1 = z
            #lstList1.insert[0, z]
            if m <= rows[row]:
                m = rows[row]
                mi = row
                #lstList1.insert(END, str())
                print("This is a tuple out of the array: {}".format(m))
                print(type(m))
                print("This is the index of the array: {}".format(row))
                print(type(row))
                for i in m:
                    print("This is data out of the tuple: {}".format(i))
                    print(type(i))
                    i = str(i)
                    print(type(i))
                    lstList1.insert(0, i)
                
conn.close()


root.mainloop()
