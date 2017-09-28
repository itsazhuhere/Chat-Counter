'''
Created on Feb 21, 2016

@author: Andre
'''



import wx
import backgroundmanager as bgm



TUPLE_LENGTH = 3

class CounterFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        #set all style/size params here in the super().__init__()
        super(CounterFrame, self).__init__(*args, **kwargs)
        self.create_windows()
        self.bind_events()
        
        
    def create_windows(self):
        self.option_display = OptionDisplay(self)





class OptionDisplay(wx.Window):
    #TODO: add animation for changes
    def __init__(self, *args, **kwargs):
        super(OptionDisplay, self).__init__(*args, **kwargs)
        self.lines = []
        self.sizer = wx.FlexGridSizer(cols=1, hgap=5, vgap=5)
        self.SetSizerAndFit(self.sizer)
        
    def update(self, info):
        #adjusts number of shown lines to match needed
        print(self.lines)
        difference = len(info) - len(self.lines)
        if difference > 0:
            for i in range(difference):
                self._add_line()
        
        elif difference < 0:
            for i in range(difference,0):
                self._hide_line(i)
                
        for line in range(len(info)):
            self.lines[line].change_label(info[line][0], info[line][1])
        self.sizer.Layout()

    def _add_line(self):
        number = len(self.lines) + 1
        self.lines.append(OneLine(self).set_number(number))
        self.sizer.Add(self.lines[-1])
        self.sizer.Layout()
        
            
    def _hide_line(self, index):
        for i in range(TUPLE_LENGTH):
            self.line_list[index][i].Show(False)
            
            
class OneLine(wx.Window):
    def __init__(self, *args, **kwargs):
        super(OneLine, self).__init__(*args, **kwargs)
        self.create_windows()
        self.set_sizer()
        
    def create_windows(self):
        self.number = wx.StaticText(self)
        self.name = wx.StaticText(self)
        self.count = wx.StaticText(self)
        
    def set_sizer(self):
        self.sizer = wx.FlexGridSizer(cols=3)
        self.sizer.Add(self.number)
        self.sizer.Add(self.name)
        self.sizer.Add(self.count)
        self.SetSizer(self.sizer)
        
    def set_number(self, number):
        self.number.SetLabel(str(number) + ".")
        
    
    def change_label(self, name, count):
        self.name.SetLabel(name)
        self.count.SetLabel(str(count))
        
    def animate(self):
        #animate concept: flash (white) then immediate blue then fade to background color
        pass
