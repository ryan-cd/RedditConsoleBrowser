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
        
    def _page_break(self):
        print('\n>>new page --------------------------')
        
    def _update_page(self):
        self.page = []
        try:
            for i in range(self.index_start, self.index_end):
                self.page.append(self.stories_list[i])
        except:
            print('\n$ There doesn\'t seem to be anything here.')
            self.previous_page()
        
    def set_object(self, obj):
        self.stories = obj

    def print_page(self):
        i = 1
        for stories in self.get_page():
            print(self.index_start + i, '::', str(stories))
            i = i + 1
            
    def next_page(self):
        self.index_start += self.amount_per_page
        self.index_end += self.amount_per_page
        self._update_page()
        self._page_break()

    def previous_page(self):
        if(self.index_start - self.amount_per_page >= 0):
            self.index_start -= self.amount_per_page
            self.index_end -= self.amount_per_page
            self._update_page()
            self._page_break()

    def get_page(self):
        return self.page

    def get_index_start(self):
        return self.index_start

    def get_amount_per_page(self):
        return self.amount_per_page

class Comments:
    def __init__(self, submission_id):
        self.submission = r.get_submission(submission_id = submission_id)
        self.forest_comments = submission.comments
        
        #post = r.get_submission(submission_id='2qnguy')
        #post.selftext
        #print(vars(post.comments[0]) to see the vars in a comment
        #str(post.comments[0].body)
        
        
def login():
    print('\nPlease login to Reddit')
    login_username = 'api_test1'#input('\nUsername: ')
    login_password = 'qWaszx1'#input('Password: ')
    try:
        r.login(login_username, login_password)
    except:
        print('Oops! The login was not recognized, please try again.')
        login()

def frontpage():
    print('$ Hang tight, fetching stories...')
    
    front_page = Stories(r.get_front_page(limit=200))

    while(True):
        front_page.print_page()
        choice = '!' # temporary flag, will be assigned by user
        while(choice != 'n' or choice != 'p' or choice != 'b'):
            choice = input('\nChoose an action: [#] view comments [n]ext, [p]rev, [b]ack: ')
            try:
                if(int(choice) >= front_page.get_index_start() + 1
                     and int(choice) < front_page.get_index_start() + front_page.get_amount_per_page() + 1):
                    print('comments requested')
                    continue
            except:
                pass
            
            if(choice == 'n'):
                front_page.print_page()
                front_page.next_page()
                break
            elif(choice == 'p'):
                front_page.previous_page()
                break
            elif(choice == 'b'):
                menu()
            else:
                print('$ Command not recognized, please try again')
                continue
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

