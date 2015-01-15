import praw

#CLASSES
#

class Stories:
    def __init__(self, obj):
        self.amount_per_page = 15
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

    def get_submission(self, post_number):
        return self.stories_list[post_number-1].id

class Submission:
    def __init__(self, submission_id):
        self.submission = r.get_submission(submission_id=submission_id)
        try:
            self.forest_comments = self.submission.comments
            #self.flat_comments = praw.helpers.flatten_tree(self.submission.comments)
            self.current_comment_block = 0
            self.current_comment = self.forest_comments[self.current_comment_block]
            self.flat_comment_index = 0
        except:
            pass
        
    def show_post(self):
        print('$---------------------------------'
              '\n Viewing topic', self.submission.title, '. . .'
              '\n$---------------------------------')
        print(self.submission.url, '\nOP:', self.submission.selftext)
        print('________________________')
        print('________________________')
        
    def print_comment_block(self):
        try:
            self.current_comment = self.forest_comments[self.current_comment_block]
            print(self.current_comment.score, self.current_comment.body)
            for i in range(0, len(self.current_comment.replies)):
                if(hasattr(self.current_comment.replies[i], 'body')):
                    print('>>>', self.current_comment.replies[i].score, self.current_comment.replies[i].body)
        except:
            pass
        
    def next_comment_block(self):
        if(self.current_comment_block + 1 < len(self.forest_comments) - 1):
            self.current_comment_block = self.current_comment_block + 1    
        
    def previous_comment_block(self):
        if (self.current_comment_block - 1 >= 0):
            self.current_comment_block = self.current_comment_block - 1  
      

#FUNCTIONS
#
        
def login():
    print('\n$ Please login to Reddit')
    login_username = input('\nUsername: ')
    login_password = input('Password: ')
    try:
        r.login(login_username, login_password)
    except:
        print('Oops! The login was not recognized, please try again.')
        login()

def comments( submission_id ):
    submission_object = Submission(submission_id)
    submission_object.show_post()
    choice = '!' #temporary flag value
    
    while(choice != 'b'):
        try:
            submission_object.print_comment_block()
        except:
            pass
        
        while(choice != 'n' or choice != 'p' or choice != 'b'):
            choice = input('\n$ Choose an action: [n]ext comment, [p]rev comment, [b]ack: ')
            if(choice == 'n'):
                submission_object.next_comment_block()
                break
            elif(choice == 'p'):
                submission_object.previous_comment_block()
                break
            elif(choice == 'b'):
                break
            else:
                print(choice, '$ Comment command not recognized, please try again')
                continue
    #at this point the function is done and control will be handed back to the caller

def browse_pages(subreddit='!'):
    print('$ Hang tight, fetching stories...')
    if(subreddit == '!'):
        stories_object = Stories(r.get_front_page(limit=100))
    else:
        try:
            stories_object = Stories(r.get_subreddit(subreddit).get_hot(limit=100))
        except:
            print('$ Subreddit not found, please try again')
            menu()
        
        
    choice = '!' # temporary flag, will be assigned by user
          
    while(choice != 'b'):
        stories_object.print_page()
        
        while(choice != 'n' or choice != 'p' or choice != 'b'):
            choice = input('\n$ Choose an action: [#] view comments [n]ext, [p]rev, [b]ack: ')
            try:
                if(int(choice) >= stories_object.get_index_start() + 1
                     and int(choice) < stories_object.get_index_start() + stories_object.get_amount_per_page() + 1):
                    comments(stories_object.get_submission(int(choice)))
                    break
            except:
                pass
            
            if(choice == 'n'):
                stories_object.next_page()
                break
            elif(choice == 'p'):
                stories_object.previous_page()
                break
            elif(choice == 'b'):
                break
            else:
                print(choice, '$ Command not recognized, please try again')
                continue
    menu()
    
            
def menu():
    choice = input('$ What would you like to do? [f]rontpage, [s]ubreddits')
    if(choice == 'f'):
        browse_pages()
    elif(choice == 's'):
        browse_pages(input("Enter subreddit name"))
    else:
        print('$ Command not recognized, please try again')
        menu()

#main entry point
print('$ Welcome to Reddit Console Browser.')
r = praw.Reddit('Reddit console browser by /u/api_test1 v1.0')
login()
menu()

