'''
Created on Jan 2, 2016

@author: Andre
'''
import wx

class Prototype(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, None, size=(550,300))

        self.InitUI()
        self.Centre()
        self.Show()
    #define User Interface
    def InitUI(self):
        self.panel1 = wx.Panel(self, -1)

        #Static Text
        s_text1 = wx.StaticText(self.panel1, -1, "Hello World!", (10,5)) #top text
        self.s_text2 = wx.TextCtrl(self.panel1, style=wx.TE_READONLY | wx.NO_BORDER, pos=(300,10)) #top text
        self.s_text2.AppendText("gray")
        self.s_text2.SetBackgroundColour("gray")
if __name__ == '__main__':
    app = wx.App()
    Prototype(None, title='')
    app.MainLoop()