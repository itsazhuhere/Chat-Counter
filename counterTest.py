'''
Created on Dec 15, 2015

@author: Andre
'''

from TwitchChatBot import *
from TextParser import *

import os

USERNAME = "itsazhuhere"
PASSWORD = "oauth:diuyyk57s1dqv4xz31cmnnh40sewgb"
CHANNEL = "#" + "wingsofdeath"


clear = lambda: os.system("cls")

def main():
    chat_bot = ChatBot(USERNAME, PASSWORD)
    test_counter = Poll(["lol", "kappa", "rekt", "rip", "na"])
    test_handler = ChatHandler("Pobelter", [test_counter])
    try:
        print("Connecting to twitch")
        chat_bot.connect_to_irc()
    except:
        print("Could not connect to Twitch")
    
    try:
        print("Connecting to channel {0}".format(CHANNEL))
        chat_bot.connect_to_channel(CHANNEL)
    except:
        print("Could not connect to channel")
        
    while True:
        while True:
            try:
                chat_bot.receive_data()
                message_data = chat_bot.return_message()
                break
            except NoMessageError: #need to refine this so that when there are no users sending messages in the chat it will definitely loop back, for channels that have slow chats/submode
                pass
            sleep(.1)
        for message in message_data:
            try:
                test_handler.check_message(message[0], message[1])
                print(str(test_counter))
            except UnicodeEncodeError:
                pass
        
        
if __name__ == "__main__":
    main()
    
    