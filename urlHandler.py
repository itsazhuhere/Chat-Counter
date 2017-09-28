


import TextParser
from flask import request



class FormHandler:
    def __init__(self, form_data, chat_bot):
        self.form = self._to_tuples(form_data)
        self.chat_bot = chat_bot
        
        self._fill_counter_list()
        self._validate_form()
    
    def _validate_form(self):
        if not self.chat_bot.is_monitoring(self.form.channel):
            self.chat_bot.start_monitoring(self.form.channel)
        
        self._check_duplicates()
        
    def _to_tuples(self, form_data):
        
    
    
    def _fill_counter_list(self):
        self.counters = []
        for option in self.form.counter_options:
            self.counters.append(option)
    
    def _check_duplicates(self):
        self.duplicates = []
        
        #sort options by string then check for adjacent duplicates?
            
        if self.duplicates:
            raise DuplicateError
        
        
    def change_form(self, new_form):
        self.__init__(new_form, self.chat_bot)
        

class DuplicateError(Exception):
    pass

