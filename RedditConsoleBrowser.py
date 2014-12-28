import praw
import time
import pprint
from itertools import islice

class Stories:
    def __init__(self, obj):
        self.amount_per_page = 20
        self.stories = obj
        self.index_start = 0
        self.index_end = self.amount_per_page
        self._update_page()

    def _update_page(self):
        self.page = list(islice(self.stories, self.index_start, self.index_end))
        
    def set_object(self, obj):
        self.stories = obj

    def next_page(self):
        self.index_start += self.amount_per_page
        self.index_end += self.amount_per_page
        self._update_page()

    def previous_page(self):
        self.index_start -= self.amount_per_page
        self.index_end -= self.amount_per_page
        self._update_page()

    def get_page(self):
        return self.page

def login():
    print('\nPlease login to Reddit')
    login_username = input('\nUsername: ')
    login_password = input('Password: ')
    try:
        r.login(login_username, login_password)
    except:
        print('Oops! The login was not recognized, please try again.')
        login()

def frontpage():
    print('Hang tight, fetching stories...')
    
    front_page = Stories(r.get_front_page(limit=None))

    
    for stories in front_page.get_page():
        print(str(stories))
    #front_page.next_page()
    menu()
    
            
def menu():
    choice = input('What would you like to do? [f]rontpage, [s]ubreddits, [m]ail: ')
    if(choice == 'f'):
        frontpage()
    #elif(choice == 's'):
        
    #elif(choice == 'm'):

#main entry point
print('Welcome to Reddit Console Browser.')
r = praw.Reddit('Reddit console browser by /u/api_test1 v1.0')
login()
menu()

