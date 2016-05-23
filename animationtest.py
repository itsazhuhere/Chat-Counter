'''
Created on Mar 3, 2016

@author: Andre
'''



import wx 
import wx.html2 

class MyBrowser(wx.Dialog): 
    def __init__(self, *args, **kwargs):
        #TODO: modify dialog to not show the top bar and instead have a custom close button, etc.
        wx.Dialog.__init__(self, *args, **kwargs) 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        self.browser = wx.html2.WebView.New(self) 
        sizer.Add(self.browser, 1, wx.EXPAND, 10) 
        self.SetSizer(sizer) 
        self.SetSize((700, 700)) 

if __name__ == '__main__': 
    app = wx.App() 
    dialog = MyBrowser(None, -1) 
    dialog.browser.LoadURL("http://www.google.com") 
    dialog.Show() 
    app.MainLoop() 