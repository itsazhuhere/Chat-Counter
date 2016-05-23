import TextParser
import wx

class PollStatisticsHandler:
    def __init__(self):
        pass
    
    def get_voted_options(self, poll):
        """
        Takes a Poll object and returns the options that have a
        count greater than 0, both the label and count sorted by highest vote count first
        """
        voted_dict = dict()
        for vote in poll.get_vote_list():
            if vote.get_count() > 0:
                voted_dict[vote.get_label()]=vote.get_count()
        return sorted(voted_dict, key=voted_dict.items(),reverse=True)
    
    
    
    
    
    
    
class TopChoiceGraph(wx.Window):
    def __init__(self, *args, **kwargs):
        super(TopChoiceGraph, self).__init__(*args, **kwargs)
        self._setup_graph()
        
        
    def update(self, graph_info):
        self._update_numbers(graph_info)
        self._update_bars(graph_info)
        
        
    def _update_numbers(self, graph_info):
        pass
    
    def _update_bars(self, graph_info):     
        pass
        
    def _setup_graph(self):
        pass