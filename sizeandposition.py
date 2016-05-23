'''
Created on Jan 9, 2016

@author: Andre
'''

from wx import Point, Size



SIZE =        {"options": Size(220, 240),
               "channel_textctrl": Size(200, 24),
               "add_button": Size(30,30),
               "ok_button": Size(74, 25),
               "load_button": Size(74, 25),
               "save_button": Size(74, 25),
               "textctrl_size": Size(168,25),
               "remove_button": Size(15,15)
              }
#make these relative positions rather than absolute
POSITION =    {"save_button": Point(84,330),
              "cancel_button": Point(490, 330),
              "ok_button": Point(10, 330),
              "add_button": Point(231, 79),
              "load_button": Point(158,330),
              "defaults_combobox": Point(380, 80),
              "options": Point(11, 80),
              "channel_text": Point(100, 15),
              "channel_textctrl": Point(190, 11),
              "check_button": Point(400, 10),
              "form_text": Point(11, 60),
              "defaults_text": Point(380, 60)
              }