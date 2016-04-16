#!/usr/local/bin/python2
# Daniel A. Christie
# Purpose:  This script was created in an effort to learn a button roll-over
# effect with imeages. Took a little time to learn but as usual, worth it.

import wx

class BitmapButtonFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Bitmap Button Example', pos=(450, 250), size=(300, 180))
        panel = wx.Panel(self, -1)
        self.SetBackgroundColour("White")

        # save images to their variables
        pic1 = wx.Image("a.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        pic2 = wx.Image("b.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()

        #---------------Construct Button 1------------------
        # assign the image pic1 to a Bitmap Button widget
        self.button1 = wx.BitmapButton(panel, -1, pic1, pos=(80, 10), size=(118, 46))
        # assign button events when hover over, hover off, and pressed
        self.button1.Bind(wx.EVT_BUTTON, self.buttonClick, self.button1)
        self.button1.Bind(wx.EVT_ENTER_WINDOW, self.btn1MouseOver)

        # assigning button1 as the defualt focus
        self.button1.SetDefault()

        #---------------Construct Button 2-----------------
        # assign the image pic2 to a Bitmap Button widget
        self.button2 = wx.BitmapButton(panel, -1, pic2, pos=(80, 10), size=(118, 46))
        # assign button events when hover over, hover off, and pressed
        self.button2.Bind(wx.EVT_BUTTON, self.buttonClick, self.button2)
        self.button2.Bind(wx.EVT_LEAVE_WINDOW, self.btn2MouseLeave)
        # display a tooltip
        self.button2.SetToolTip(wx.ToolTip("Hovering over button 1"))

        #---------------Construct Button 3------------------
        # assign the image pic1 to a Bitmap Button widget
        self.button3 = wx.BitmapButton(panel, -1, pic1, pos=(80, 60), size=(118, 46))
        # assign button events when hover over, hover off, and pressed
        self.button3.Bind(wx.EVT_BUTTON, self.buttonClick, self.button3)
        self.button3.Bind(wx.EVT_ENTER_WINDOW, self.btn3MouseOver)

        #---------------Construct Button 4-----------------
        # assign the image pic2 to a Bitmap Button widget
        self.button4 = wx.BitmapButton(panel, -1, pic2, pos=(80, 60), size=(118, 46))
        # assign button events when hover over, hover off, and pressed
        self.button4.Bind(wx.EVT_BUTTON, self.buttonClick, self.button4)
        self.button4.Bind(wx.EVT_LEAVE_WINDOW, self.btn4MouseLeave)
        # display a tooltip
        self.button4.SetToolTip(wx.ToolTip("Hovering over button 2"))

    #--------------Hide and Show the Buttons---------------
    def btn1MouseOver(self,event):
        self.button1.Hide()
        self.button2.Show()
        self.SetTitle("Hover Over")

    def btn2MouseLeave(self,event):
        self.button2.Hide()
        self.button1.Show()
        self.SetTitle("Hover Off")

    def btn3MouseOver(self,event):
        self.button3.Hide()
        self.button4.Show()
        self.SetTitle("Hover Over")

    def btn4MouseLeave(self,event):
        self.button4.Hide()
        self.button3.Show()
        self.SetTitle("Hover Off")
        
    def buttonClick(self,event):
        self.Destroy()
        
app = wx.App()
frame = BitmapButtonFrame()
frame.Show()
app.MainLoop()
