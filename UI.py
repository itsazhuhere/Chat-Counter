'''
Created on Dec 29, 2015

@author: Andre
'''


import wx
import wx.lib.newevent
import backgroundmanager as bgm
import sizeandposition as sp
import TextParser as tp
from counterTest import USERNAME, PASSWORD
from cProfile import label
from PollStatisticsHandler import TopChoiceGraph



TUPLE_LENGTH = 3

MAIN_SIZE = wx.Size(600,600)
FORM_SIZE = wx.Size(600,400)
DISPLAY_SIZE = wx.Size(300,300)
GRAPH_SIZE = wx.Size(300,300)

NO_RESIZE = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN

MAX_OPTIONS = 500
DEFAULT_OPTIONS = 1
DEFAULT_CHOICES = ["League of Legends Champions", "Hearthstone Cards"]

FORM_RESULT_ID = wx.NewId()

USERNAME = "itsazhuhere"
PASSWORD = "oauth:diuyyk57s1dqv4xz31cmnnh40sewgb"
CHANNEL = "#" + "c9rush"


FormReturnEvent, EVT_RETURN_FORM = wx.lib.newevent.NewEvent()



class MainFrame(wx._windows.Frame):
    def __init__(self, parent, title):
        wx._windows.Frame.__init__(self, parent, title=title, size=MAIN_SIZE)
        self.create_menu()
        self.active_counter = False
        self.Show(True)
        
        
    def create_menu(self):
        self.CreateStatusBar()
        
        filemenu = wx.Menu()
        
        menu_about = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menu_about)
        
        filemenu.AppendSeparator()
        menu_new = filemenu.Append(wx.ID_NEW, "&New", "Create a new counter")
        self.Bind(wx.EVT_MENU, self.on_new, menu_new)
        
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "&Exit", "Terminate the program")
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        

        
        
    def OnAbout(self, event):
        pass
    
    def on_new(self, event):
        #if frame is already in form,if clean -> do nothing, else prompt for save if not saved
        #else check for save and prompt then change to form
        self.Bind(EVT_RETURN_FORM, self.on_return)
        self.counter_form = CounterForm(self, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, size = FORM_SIZE)
        self.counter_form.Show()

        
    def on_return(self, event):
        #TODO: instead pops up a new frame and changes parent frame to a way to control the display
        #this means that the frame will change size 
        #new frame should be always on top
        pass
        
class CounterFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(CounterFrame, self).__init__(*args, **kwargs)
        self.create_windows()
        self.set_sizers()
        
    def create_windows(self):
        self.labels = CounterLabels(self)
        self.display = CounterDisplay(self)
        
    def set_sizers(self):
        self.sizer = wx.FlexGridSizer(cols = 1)
        self.sizer.Add(self.labels)
        self.sizer.Add(self.display)
        self.SetSizer(self.sizer)
        
    def bind_events(self):
        self.Bind(bgm.EVT_COUNTER_UPDATE, self.on_update)
    
    def on_update(self,event):
        self.display.update(event.attr1)
    
class CounterLabels(wx.Window):
    #TODO: adjust positions and sizes (and maybe add the StaticText overflow option)
    def __init__(self, *args, **kwargs):
        super(CounterFrame, self).__init__(*args, **kwargs)
        wx.StaticText(self, label = "Name")
        wx.StaticText(self, label = "Count")


class CounterDisplay(wx.Window):
    #TODO: add correct headers, adjust initialization settings appropriately
    def __init__(self, *args, **kwargs):
        super(CounterDisplay, self).__init__(*args, **kwargs)
        self.line_list = []
        self.sizer = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)
        self.SetSizerAndFit(self.sizer)
        
    def update(self, info):
        #adjust number of shown lines to match needed
        difference = len(info) - len(self.line_list)
        if difference > 0:
            for i in range(difference):
                self._add_line()
        
        elif difference < 0:
            for i in range(difference,0):
                self._hide_line(i)
                
        for line in range(len(info)):
            self.line_list[line].SetLabel(str(info[line]))
            self.line_list[line].Show(True)
        self.sizer.Layout()

    def _add_line(self):
        number = len(self.line_list) + 1
        self.line_list.append(SingleLine(number))
        self.sizer.Add(self.line_list[-1])
            
    def _hide_line(self, index):
        self.line_list[index].Show(False)
            
class SingleLine(wx.Window):
    #TODO: adjust hgap and vgap
    def __init__(self, number, *args, **kwargs):
        super(SingleLine, self).__init__(*args, **kwargs)
        self.create_text(number)
        self.set_sizers()

    def create_text(self, number):
        self.number = wx.StaticText(self, label=str(number)+".")
        self.label = wx.StaticText(self)
        self.count = wx.StaticText(self)
        
    def set_sizers(self):
        self.sizer = wx.FlexGridSizer(cols = 3)
        self.sizer.Add(self.number)
        self.sizer.Add(self.label)
        self.sizer.Add(self.count)
        
        self.SetSizer(self.sizer)
    
    def change_labels(self, new_label, new_count):
        self.label.SetLabel(new_label)
        self.count.SetLabel(new_count)
    
    
            
class OptionEntry(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(OptionEntry, self).__init__(*args, **kwargs)
        self.Bind()#binds ok button event to a self.on_done method
        
        
    def on_done(self, event):
        self._check_duplicates(self.Get)
        
        #remove all instances of "\n"
        new_string = event.text.replace("\n", "")
        
        parsed_dict = self._list_to_dict(self._string_to_list(new_string))
        
        return parsed_dict #Post this somewhere
        
        
    def _check_duplicates(self):
        #This function will check for multiple 
        pass
    
    def _string_to_list(self, text):
        return [section.split(",") for section in text.split(";")]
    
    def _list_to_dict(self, list_list):
        #TODO: this function should be elsewhere
        all_options = {}
        for section in list_list:
            #multiple keys will point to a single Counter if that choice has multiple variations
            counter = tp.VoteCounter(section[0])
            for item in section:
                all_options[item] = counter
            #and them append counter somewhere accessible
        return all_options




class CounterForm(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(CounterForm, self).__init__(*args, **kwargs)
        self.grid_sizer = wx.FlexGridSizer(rows=1, cols=3, vgap=10, hgap=10)
        self.SetBackgroundColour("white")
        
        self.create_controls()
        self.bind_events()
        self.set_size_position()
        
        
        
    def create_controls(self):
        self.channel_text = wx.StaticText(self, label="Channel name: ")
        self.channel_textctrl = wx.TextCtrl(self)
        self.form_text = wx.StaticText(self, label="Enter choices manually : ")
        self.default_text = wx.StaticText(self, label="Choose from defaults: ", pos=sp.POSITION["defaults_text"])
        self.check_button = wx.Button(self, label="Check")
        self.options = OptionList(parent=self, style=wx.BORDER_SIMPLE|wx.VSCROLL)
        self.save_button = wx.Button(self, label="Save")
        self.cancel_button = wx.Button(self, label="Cancel")
        self.ok_button = wx.Button(self, label="Create")
        self.add_button = wx.Button(self, label="+")
        self.load_button = wx.Button(self, label="Load")
        self.defaults_combobox = wx.ComboBox(self, choices=DEFAULT_CHOICES, style=wx.CB_DROPDOWN)
        
        
    def bind_events(self):
        for control, event, handler in \
        [(self.save_button, wx.EVT_BUTTON, self.on_save),
         (self.cancel_button, wx.EVT_BUTTON, self.on_cancel),
         (self.ok_button, wx.EVT_BUTTON, self.on_ok),
         (self.add_button, wx.EVT_BUTTON, self.on_add),
         (self.load_button, wx.EVT_BUTTON, self.on_load),
         (self.defaults_combobox, wx.EVT_COMBOBOX, self.on_chosen)]:
            control.Bind(event, handler)
        
    def set_size_position(self):
        for ui_object in self.__dict__.keys():
            if ui_object in sp.SIZE:
                self.__dict__[ui_object].SetSize(sp.SIZE[ui_object])
            if ui_object in sp.POSITION:
                self.__dict__[ui_object].SetPosition(sp.POSITION[ui_object])
        
    def on_add(self, event):
        # if no more options raise error
        self.options.add_option()
        self.grid_sizer.Layout()
        
    
    def on_remove(self, event):
        pass

    def on_save(self, event):
        pass
    
    def on_cancel(self, event):
        #check if anything is filled in, if so then ask if user wants to save
        self.Destroy()
    
    def on_load(self, event):
        pass
    
    def on_chosen(self, event):
        pass


    def on_ok(self, event):
        #gather info from entries/combobox selection/loaded document
        #####should have separate confirms for separate types of poll creation
        #####ie and ok button under the manual and an ok button under the combobox
        #put them into a FormReturnEvent object
        #post event
        #destroy frame
        
        evt = FormReturnEvent(attr1= self.options.get_strings())
        wx.PostEvent(self.Parent, evt)
        self.Destroy()
        
    def delete_option(self, event):
        self
        

class OptionList(wx.Window):
    def __init__(self, *args, **kwargs):
        super(OptionList, self).__init__(*args, **kwargs)
        self.option_objects = [None for i in range(DEFAULT_OPTIONS - 1)]
        self.option_strings = ["" for i in range(DEFAULT_OPTIONS - 1)]
        self.grid_sizer = wx.FlexGridSizer(cols=3, vgap=0, hgap=0)
        
        self.Bind(EVT_OPTION_DELETE, self.delete_option)
        self.add_option()
        self.Fit()
        self.SetSizerAndFit(self.grid_sizer)
        
        
    def add_option(self):
        """
        Creates an option object and adds it to the list, then binds the object's textctrl
        to an event that occurs when the user switches focus from that textctrl.
        The objects are then added to the sizer for formatting.
        """
        self.option_objects.append(Option(position=len(self.option_objects), parent=self))
        self.option_objects[-1].get_textctrl().Bind(wx.EVT_KILL_FOCUS, self.on_filled)
        self.grid_sizer.Add(self.option_objects[-1].get_label(), **dict(flag=wx.EXPAND))
        self.grid_sizer.Add(self.option_objects[-1].get_textctrl(), **dict(flag=wx.ALL))
        self.grid_sizer.Add(self.option_objects[-1].get_remove(), **dict())
        
        self.option_strings.append("")
        
        self.grid_sizer.Layout()  # #check this if it does what i think it does


    def on_filled(self, event):
        position = self[event.GetId()].get_position()
        self.option_strings[position] = self.option_objects[position].get_textctrl().GetLineText(0)
        event.Skip()
        
    def get_strings(self):
        return self.option_strings
    
    def delete_option(self, event):
        del(self.option_strings[event.attr1])
        for i in range(3): #3 is the number of ui objects displayed in each Option object
            self.grid_sizer.Hide(event.attr1*3)
            self.grid_sizer.Detach(event.attr1*3)
        del(self.option_objects[event.attr1])
        self._redo_numbers()
        self.grid_sizer.Layout()
    
    def _redo_numbers(self):
        for i in range(len(self.option_objects)):
            self.option_objects[i].get_label().SetLabel(str(i+1)+".")
            self.option_objects[i].change_position(i)
    
    def __getitem__(self, index):
        for i in range(len(self.option_objects)):
            if self.option_objects[i] == index:  # the id of the textctrl
                return self.option_objects[i]
        raise NoOptionError
        
        
class Option:
    def __init__(self, position, style=wx.ALIGN_CENTRE_HORIZONTAL, *args, **kwargs):
        self.position = position
        self.text_ctrl = wx.TextCtrl(size=sp.SIZE["textctrl_size"],*args, **kwargs)
        self.name_label = wx.StaticText(label=str(self.position + 1) + ".", style=style,*args, **kwargs)
        self.remove_button = wx.Button(label= "X",size = sp.SIZE["remove_button"], style= wx.SIMPLE_BORDER, *args, **kwargs)
        self.remove_button.Bind(wx.EVT_BUTTON, self.remove)
        
        self.name_label.SetBackgroundColour("white")
        
    def change_position(self, position):
        self.position = position
    
    def get_position(self):
        return self.position
    
    def get_textctrl(self):
        return self.text_ctrl
    
    def get_label(self):
        return self.name_label
    
    def get_remove(self):
        return self.remove_button
    
    def get_both(self):
        return (self.position, self.name_label)
    
    def remove(self, event):
        evt = OptionDeleteEvent(attr1 = self.position)
        wx.PostEvent(self.text_ctrl.Parent, evt)
        
    def __eq__(self, right):
        if type(right) is not int:
            raise TypeError("Index is not of type int")
        return self.text_ctrl.GetId() == right
    
        

OptionDeleteEvent, EVT_OPTION_DELETE = wx.lib.newevent.NewEvent()











class NoOptionError(Exception):
    pass

def main():
    app = wx.App(False)
    frame = MainFrame(None, "Test Run")
    app.MainLoop()
    
if __name__ == "__main__":
    main()
