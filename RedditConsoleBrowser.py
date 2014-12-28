import praw
import time
import pprint
from itertools import islice

class Stories:
    def __init__(self, obj):
        self.amount_per_page = 15
        #self.stories = obj
        self.stories_list = []
        for o in obj:
            self.stories_list.append(o)
        self.index_start = 0
        self.index_end = self.amount_per_page
        self._update_page()

    def _update_page(self):
        #self.page = list(islice(self.stories, self.index_start, self.index_end, 1))
        self.page = []
        for i in range(self.index_start, self.index_end):
            self.page.append(self.stories_list[i])
        #print(self.index_start)
        
    def set_object(self, obj):
        self.stories = obj

    def next_page(self):
        self.index_start += self.amount_per_page
        self.index_end += self.amount_per_page
        self._update_page()

    def previous_page(self):
        if(self.index_start - self.amount_per_page >= 0):
            self.index_start -= self.amount_per_page
            self.index_end -= self.amount_per_page
            self._update_page()

    def get_page(self):
        return self.page

    def get_start_index(self):
        return self.start_index

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
    
    front_page = Stories(r.get_front_page(limit=150))

    while(True):
        for stories in front_page.get_page():
            print(str(stories))
        choice = '!' # temporary flag, will be assigned by user
        while(choice != 'n' or choice != 'p' or choice != 'b'):
            choice = input('Choose an action: [n]ext, [p]rev, [b]ack: ')
            if(choice == 'n'):
                print('BEFORE NEXT')
                for stories in front_page.get_page():
                    print(str(stories))
                front_page.next_page()
                
                break
            elif(choice == 'p'):
                front_page.previous_page()
                break
            elif(choice == 'b'):
                menu()
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

