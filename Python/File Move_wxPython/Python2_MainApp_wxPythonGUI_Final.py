#!/usr/bin/python2
#Author:    Daniel Christie
#           Tech Academy Python Course, Drill 68
#Topic:     The Tech Academy - Python Course Drill Shutil.move
#Purpose:   Check a directory for instances of txt files created or modified within
#           a 24 hour period and move those files into another folder
#           Application with wxPython as the GUI

import os, time
import wx
import shutil
from datetime import datetime, timedelta
import sqlite3


class windowClass(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, **kwargs)

        self.mainGUI()

    def mainGUI(self):

        panel = wx.Panel(self)
        self.Centre

        # Create Menubar
        menuBar = wx.MenuBar() # Constructor for MenuBar
        
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT, "Quit Ctrl+Q")
        helpItem = helpMenu.Append(wx.ID_HELP, "Help")
        fileItem = menuBar.Append(fileMenu, "File")
        helpItem = menuBar.Append(helpMenu, "Help")

        self.SetMenuBar(menuBar) # Mounting MenuBar to the parent window named frame at the bottom
        menuBar.Bind(wx.EVT_MENU, self.close, exitItem) # Bind events to the frame at the bottom

        # Source & Destination Directory Buttons
        btnSrc = wx.Button(panel, label='Source...', pos=(423, 30), size=(80, 25))
        btnDst = wx.Button(panel, label='Destination...', pos=(423, 70), size=(80, 25))

        # Create StaticBox for the Check File & Close Buttons
        btnCheck = wx.Button(panel, label="Check Files", pos=(320, 305), size=(80, 25))
        btnClose = wx.Button(panel, label='Close', pos=(423, 305), size=(80, 25))

        # Bind Buttons
        btnSrc.Bind(wx.EVT_BUTTON, lambda event: self.selectDir(self.txtSrc)) #Passing in variable
        btnDst.Bind(wx.EVT_BUTTON, lambda event: self.selectDir(self.txtDst)) #Passing in variable
        btnCheck.Bind(wx.EVT_BUTTON, self.OnButton2)
        btnClose.Bind(wx.EVT_BUTTON, self.close)

        # Create StaticBox for the Directory Selection
        box1 = wx.StaticBox(panel, label='    Select the source and destination:', pos=(20, 10), size=(500, 100))

        # TextControls to display the file paths
        self.txtSrc = wx.TextCtrl(panel, pos=(40, 30), size=(360, 25))
        self.txtDst = wx.TextCtrl(panel, pos=(40, 70), size=(360, 25))

        # Create the List Control
        self.listCtrl = wx.ListCtrl(panel, pos=(20,120), size=(500,165), style=wx.LC_REPORT |wx.BORDER_SUNKEN)

        # Create StaticBox & Text Control for the last check date
        box2 = wx.StaticBox(panel, label='    Last Check Date:', pos=(20, 285), size=(190, 51), style=wx.BORDER_NONE)
        txtTimestamp = wx.TextCtrl(panel, pos=(40, 305), size=(150, 22))

        self.Show(True)
        #self.Show(True) Will still load window but "False" will not display the window

        #---------Accessing Database---------
        #connecting to db.db or create it if it does not exist
        db = sqlite3.connect("db.db")

        #Create table if it does not already exist otherwise do nothing
        db.execute('CREATE TABLE IF NOT EXISTS table_name (column_date TEXT)')
        #Get row count to ensure that there is at least one entry, if not, make the first entry otherwise we will update later
        cursor = db.execute("SELECT COUNT (*) FROM table_name")
        row_count = cursor.fetchone()[0]
        if row_count < 1:
            print("No record found, updating database with missing data")
            now = time.time()
            db.execute("INSERT INTO table_name (column_date) VALUES (?)", [now])
        else:
            print("Record found.")
        db.commit()

        cursor = db.execute("SELECT column_date FROM table_name")
        lastDate = cursor.fetchone()[0]
        lastDate = float(lastDate)
        legibleDate = datetime.fromtimestamp(lastDate).strftime('%m/%d/%Y %H:%M:%S')
        report = (legibleDate)
        txtTimestamp.SetValue(report)

        db.close()
        #---------Closing Database---------


    def selectDir(self,out):
        selection = wx.DirDialog(self, "Select a directory:", defaultPath="C:\\", style=wx.DD_DEFAULT_STYLE |
                               wx.DD_NEW_DIR_BUTTON | wx.DD_DIR_MUST_EXIST)
        if selection.ShowModal() == wx.ID_OK:
            out.SetValue(selection.GetPath())
        selection.Destroy()


    def OnButton2(self, event):
        src = self.txtSrc.GetValue() #Passing in variable
        dst = self.txtDst.GetValue() #Passing in variable
        if (len(src) == 0) or (len(dst) == 0):
            missingDir = wx.MessageDialog(self, caption = "Error - Missing Directories!", \
                                      message = "Missing a directory. Please specify the source and destination directories.", style = wx.OK)
            missingDir.ShowModal()
            return  
        count = 0
        for files in os.listdir(src):
            if files.endswith(".txt"):
                source = (os.path.join(src, files))
                destination = (os.path.join(dst, files))
                mtime = (os.path.getmtime(source))
                timeDiff = time.time() - mtime #Difference from time of file creation or midification until current time 
                _24hrsAgo = time.time() - (24 *60 *60) #Epoc time for a 24hr period is 86400 seconds
                last24hrs = time.time() - _24hrsAgo #Seconds that have occured within the last 24 hr period
                if timeDiff < last24hrs: #Seconds that have passed since file creation or modification from last 24 hrs
                    count = count + 1
                    print('File detected: {}'.format(files))
                    print('File moved to: {}'.format(destination))
                    shutil.move(source,destination) #Move the qualified files into the destination directory

        if (count > 1):
            done = wx.MessageDialog(self, caption = "Success!", \
                                      message = "{} files have been moved into their destination folder...".format(count), style = wx.OK)
        elif (count == 1):
            done = wx.MessageDialog(self, caption = "Success!", \
                                      message = "1 file has been moved into the destination folder...", style = wx.OK)
        else:
            done = wx.MessageDialog(self, caption = "No more files to move!", \
                                      message = "There are no more files to be moved at this time.", style = wx.OK)    

        done.ShowModal()
                    
        #---------Accessing Database---------
        #Update the current date into the database to become the new lastDate accessed
        db = sqlite3.connect("db.db")
        now = time.time()
        report = datetime.fromtimestamp(now).strftime('%m/%d/%Y %H:%M:%S')
        db.execute("UPDATE table_name SET column_date=(?) WHERE rowid = 1", [now])
        db.commit()
        db.close()
        #---------Closing Database---------

    def close(self, event):
        self.Destroy()

def main():
    app = wx.App()
    frame = windowClass(None, wx.ID_ANY, "Check for newly created & modified files", size=(555,400), style = wx.SYSTEM_MENU | \
                          wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.CAPTION)
    app.MainLoop()
		
if __name__ == '__main__':
	main()
