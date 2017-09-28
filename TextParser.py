import operator

class VoteCounter:
    """
    A class to track the count for a single "vote," the vote being identified by
    the variable self.label, which is a string that matches lower case form of the
    chat message that it tracks.
    
    Notes/Plans:
    This class only has methods to add onto the vote count and reset the count, as
    there is currently no need to reduce the count; if in the future there is a need
    track only the votes within a certain period of time, ie in the past 5 minutes,
    then those functions will be added
    
    todo:
    -think of removing this class altogether
    -think of anything else needed in this class
    """
    def __init__(self, label):
        self.label = label
        self.count = 0
        
    def increment(self):
        self.count += 1
        return self.label
        
    def decrement(self):
        self.count -= 1
    
    def reset(self):
        self.count = 0
        
    def get_label(self):
        return self.label
    
    def get_count(self):
        return self.count
    
    def change_vote_name(self, newLabel):
        self.__init__(newLabel)
        
    def __add__(self, right):
        self.count += right
    
    def __sub__(self, right):
        self.count -= right
    
    def __eq__(self, right):
        return self.label == right
    
    def __len__(self):
        return len(self.label)
    
    def __str__(self):
        return "{0} : {1}".format(self.label, self.count)
    
    
class Poll:
    """
    A class to contain VoteCounter objects, with methods to increment/add onto the counts
    of these objects.  One can think of the VoteList object as a poll with the individual
    VoteCounter objects as poll options.
    """
    #TODO: change to use dict
    def __init__(self, new_vote_list):
        self.vote_list = [VoteCounter(vote) for vote in new_vote_list]
        self.next_position = len(new_vote_list)
        self.option_numbers = {new_vote_list[i]:i for i in range(self.next_position)}
        self.already_voted = dict()
        self.max_len_message = self._determine_max(self.vote_list)
        
    def add_vote_option(self, new_vote_option):
        if new_vote_option in self.vote_list:
            raise VoteExistsError
        self.vote_list.append(VoteCounter(new_vote_option))
        self.next_position += 1
    
    def delete_vote_option(self, vote_to_delete):
        if vote_to_delete not in self.vote_list:
            raise InvalidVoteError("Vote option {vote} does not exist in this instance of VoteList".format(vote = vote_to_delete))
        option_number = self._convert_to_int(vote_to_delete)
        self.vote_list[option_number] = ""
        for user in self.already_voted.keys():
            if self.already_voted[user] == option_number:
                del(self.already_voted[user])

        
        
    def count_new_vote(self, username, vote_to_count):
        ###consider moving checks outside of class
        #vote_int = convert_to_int(vote_to_inc)
        try:
            label = self[vote_to_count].increment()
            if username in self.already_voted:
                self.vote_list[self.already_voted[username]].decrement()
            self.already_voted[username] = self._convert_to_int(label)
        except InvalidVoteError: #should any logging be done? probably not
            pass

        
    def all_votes_reset(self):
        for vote in len(self.vote_list):
            self.vote_list[vote].reset()
    
    def contains_vote(self, vote_to_check):
        return (vote_to_check in self.vote_list)
    
    def get_vote_list(self):
        return self.vote_list
    
    def get_voted_options(self):
        """
        Takes a Poll object and returns the options that have a
        count greater than 0, both the label and count sorted by highest vote count first
        """
        voted_dict = dict()
        for vote in self.vote_list:
            if vote.get_count() > 0:
                voted_dict[vote.get_label()]=vote.get_count()
        return None if not voted_dict else sorted(voted_dict.items(), key=operator.itemgetter(1),reverse=True)

    
    def _convert_to_int(self, vote_string):
        return self.option_numbers[vote_string]
    
    def __len__(self):
        return self.max_len_message
    
    def _determine_max(self, vote_list):
        maxlen = len(vote_list[0])
        for vote in vote_list:
            if len(vote) > maxlen:
                maxlen = len(vote)
        return maxlen
        
    def __str__(self):
        return "".join(["{0}\n".format(str(option)) for option in self.vote_list])
    
    def __getitem__(self, index):
        for vote in range(len(self.vote_list)):
            if index[:len(self.vote_list[vote])] == self.vote_list[vote]:
                return self.vote_list[vote]
        raise InvalidVoteError
    

class ChatHandler:
    """
    Have globals in this class for determining when not to consider a chat message,
    most likely based on the longest vote option
    
    An object of the ChatHandler class is meant to handle all chat messages of a single
    channel, and subsequently all polls that are actively running in that channel
    
    ***should poll lifetimes be implemented here or in the Poll class?
    """
    def __init__(self, polls):
        self.polls_to_monitor = polls
        
    def add_poll(self, new_poll):
        self.polls_to_monitor.append(new_poll)
        
    def check_message(self, username, chat_message):
        formatted_message = self._format_text(chat_message)
        for poll in range(len(self.polls_to_monitor)):
            try: #overload in operator?
                self.polls_to_monitor[poll].count_new_vote(username, formatted_message)
            except InvalidVoteError:
                pass
                
    def get_polls_info(self):
        #return [poll.get_voted_options() for poll in self.polls_to_monitor]
        
        return self.polls_to_monitor[0].get_voted_options()
    
    def _format_text(self, message):
        message = message.strip()
        message = message.lower()
        return message


class InvalidVoteError(Exception):
    pass

class VoteExistsError(Exception):
    pass