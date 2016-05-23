'''
Created on Jan 4, 2016

@author: Andre
'''

import threading
import TextParser as parser
import TwitchChatBot as bot
import UI
import wx
import wx.lib.newevent
from time import sleep


POLL_DEFAULTS = ["lol", "kappa", "na"]
RESULT_ID = wx.NewId()

class BackgroundManager(threading.Thread):
    def __init__(self, parent, channel, data, *args, **kwargs):
        super(BackgroundManager, self).__init__(*args, **kwargs)
        self.parent = parent
        poll = parser.Poll(data)
        self.counter = parser.ChatHandler([poll])
        self.chat_bot = bot.ChatBot(UI.USERNAME, UI.PASSWORD) #change to use event info
        self.chat_bot.connect_to_irc()
        self.chat_bot.connect_to_channel(channel)
        #self.daemon = True
        self.start()
        
    def run(self):
        while True:
            while True:
                try:
                    self.chat_bot.receive_data()
                    message_data = self.chat_bot.return_message()
                    break
                except bot.NoMessageError: #need to refine this so that when there are no users sending messages in the chat it will definitely loop back, for channels that have slow chats/submode
                    pass
                sleep(.1)
            for message in message_data:
                try:
                    self.counter.check_message(message[0], message[1])
                    update = self.counter.get_polls_info()
                    if update:
                        evt = CounterEvent(attr1=update)
                        wx.PostEvent(self.parent, evt)
                except UnicodeEncodeError:
                    pass
                
                
CounterEvent, EVT_COUNTER_UPDATE = wx.lib.newevent.NewEvent()
