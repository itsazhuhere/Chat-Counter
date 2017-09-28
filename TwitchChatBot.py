
import socket
import re
from time import sleep

SERVER_NAME = "irc.twitch.tv"
PORT = 6667



PING_MESSAGE = "PING :tmi.twitch.tv\r\n"
PONG_RESPONSE = "PONG :tmi.twitch.tv\r\n"

CHAT_MESSAGE = r":\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :"  #edit this to not include #channel, instead using #channel for multi-channel support

class ChatBot:
    """
    Currently has no multi-channel functionality, need to implement a way to differentiate
    which messages are coming from which channels to be able to.
    
    A bot that connects to a channel and obtains user messages to that channel; messages
    are identified by the global regex expression CHAT_MESSAGE.
    
    parameters:
    -username: string of the user's twitch username
    -password: string of the user's oauth pass, not the user's actual twitch password
    
    
    implement:
    -exceptions and checking of username and pw
    -possible containment of looping within the chat bot; not necessarily needed
    
    """
    MAX_CHANNELS_PER_BOT = 20
    def __init__(self, username, password):
        self.s = socket.socket()
        self.username = username
        self.password = password
        self.connected = False
        self.monitored = []
        self.connections = 0
        self.response = ""
        
    def receive_data(self):
        """
        Collects messages sent from the server and determines 
        whether or not they are messages sent from users.
        
        Ignores other messages, except for a ping message, which
        it responds with an appropriate pong to avoid disconnect.
        In the event of a disconnect attempts to reconnect. 
        """
        try:
            response = self.s.recv(1024).decode("utf-8")
        except UnicodeDecodeError:
            response = ""
        if response:
            if response == PING_MESSAGE:
                self.s.send(PONG_RESPONSE.encode("utf-8"))
            else:
                self.response = response

    
    
    def connect_to_irc(self):
        self.s.connect((SERVER_NAME, PORT))
        self.s.send("PASS {pw}\r\n".format(pw=self.password).encode("utf-8"))
        self.s.send("NICK {user}\r\n".format(user=self.username).encode("utf-8"))
        self.connected = True
        
        
    def connect_to_channel(self, channel):
        if not self.connected:
            self.connect_to_irc()
        if self.is_monitoring(channel):
            pass #do error stuff
        if len(self.monitored) > self.MAX_CHANNELS_PER_BOT:
            raise MaxChannelsError
        self.s.send("JOIN {ch}\r\n".format(ch=channel).encode("utf-8"))
        self.monitored.append(channel)
        self.connections += 1
        
    def disconnect_from_channel(self, channel):
        #check if connected
        self.s.send("PART {ch}\r\n".format(ch=channel).encode("utf-8"))
        #remove from monitored
        
    def is_monitoring(self, channel):
        return channel in self.monitored
        
    def found_message(self):
        return bool(self.response)
    
    def return_message(self):
        if self.response:
            to_return = message_gen(self.response)
            self.response = ""
            return to_return
        else:
            raise NoMessageError


def message_gen(response):
    for line in response.split("\r\n"):
        message = re.search(r"\w+", line)
        if message: #this is here because sometimes re.search() would return a NoneType object
            username = message.group(0)
            text = re.sub(CHAT_MESSAGE, "", line)
            if not re.match(CHAT_MESSAGE, text):
                yield (username, text)
            else:
                pass
        else:
            pass

        
class NoMessageError(Exception):
    pass

class MaxChannelsError(Exception):
    pass
        