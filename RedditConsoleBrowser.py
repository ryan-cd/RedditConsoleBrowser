from __future__ import print_function
import praw
import getpass
import textwrap
from colorama import init

#CLASSES
#
class fcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[39m'

    color_array = [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET]

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
        print(fcolors.GREEN + '\n>>new page --------------------------')
        print(fcolors.RESET)

    def _update_page(self):
        self.page = []
        try:
            for i in range(self.index_start, self.index_end):
                self.page.append(self.stories_list[i])
        except:
            print(fcolors.RED + '\n$ There doesn\'t seem to be anything here.')
            print(fcolors.RESET)
            self.previous_page()

    def set_object(self, obj):
        self.stories = obj

    def print_page(self):
        i = 1
        for stories in self.get_page():
            print(fcolors.YELLOW, self.index_start + i, fcolors.RESET+':: ', end="")
            try:
                print(str(stories))
            except:
                story_string = str(stories)
                for char in story_string:
                    try:
                        print(char, end="")
                    except:
                        print('[]', end="")
                print()
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
        print('$------------------------------------------------'
              '\n' + str(self.submission.title) +
              '\n$----------------------------------------------')
        print(self.submission.selftext)
        print('________________________')

    def print_comment_block(self):
        try:
            self.current_comment = self.forest_comments[self.current_comment_block]
            self.print_comment(self.current_comment, 0)
        except:
            pass

    def print_comment(self, comment, depth):
        self.current_comment = comment

        if(hasattr(self.current_comment, 'body')):
            prefix_length = 2*depth

            if(depth > 0):
                prefix = ((" ")*(depth)*2)+fcolors.color_array[depth] + "| " + fcolors.RESET
                prefix_length += 2
            else:
                prefix = ""

            wrapper = textwrap.TextWrapper(initial_indent=prefix, width=70, subsequent_indent=' '*prefix_length)

            heading = fcolors.CYAN+self.current_comment.author.name + fcolors.YELLOW + ' (' + str(self.current_comment.score) + ')' + fcolors.RESET
            print(wrapper.fill(heading))

            message = self.current_comment.body
            print(wrapper.fill(message))


            for i in range(0, len(self.current_comment.replies)):
                self.print_comment(self.current_comment.replies[i], depth+1)

    def next_comment_block(self):
        if(self.current_comment_block + 1 < len(self.forest_comments) - 1):
            self.current_comment_block = self.current_comment_block + 1

    def previous_comment_block(self):
        if (self.current_comment_block - 1 >= 0):
            self.current_comment_block = self.current_comment_block - 1


#FUNCTIONS
#

def login():
    init();
    print(fcolors.GREEN+ '\n$ Please login to Reddit')
    print(fcolors.WHITE)
    login_username = input('\nUsername: ')
    login_password = getpass.getpass('Password: ')
    try:
        r.login(login_username, login_password)
        print(fcolors.RESET)
    except:
        print(fcolors.RED + '$ Oops! The login was not recognized, please try again.')
        print(fcolors.RESET)
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
            print(fcolors.GREEN + '\n$ Choose an action: [n]ext comment, [p]rev comment, [b]ack: ' + fcolors.RESET, end="")
            choice = input()
            print(fcolors.RESET)
            if(choice == 'n'):
                submission_object.next_comment_block()
                break
            elif(choice == 'p'):
                submission_object.previous_comment_block()
                break
            elif(choice == 'b'):
                break
            else:
                print(choice, fcolors.RED + '$ Comment command not recognized, please try again')
                print(fcolors.RESET)
                continue
    #at this point the function is done and control will be handed back to the caller

def browse_pages(subreddit='!'):
    print(fcolors.GREEN + '$ Hang tight, fetching stories...')
    print(fcolors.RESET)
    if(subreddit == '!'):
        stories_object = Stories(r.get_front_page(limit=100))
    else:
        try:
            stories_object = Stories(r.get_subreddit(subreddit).get_hot(limit=100))
        except:
            print(fcolors.RED + '$ Subreddit not found, please try again')
            print(fcolors.RESET)
            menu()


    choice = '!' # temporary flag, will be assigned by user

    while(choice != 'b'):
        stories_object.print_page()

        while(choice != 'n' or choice != 'p' or choice != 'b'):
            print(fcolors.GREEN + '\n$ Choose an action: [#] view comments [n]ext, [p]rev, [b]ack: ' + fcolors.RESET, end="")
            choice = input()
            print(fcolors.RESET)
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
                print(fcolors.RED)
                print(choice, '$ Command not recognized, please try again')
                print(fcolors.RESET)
                continue
    menu()

def messaging():
    choice = '!'
    while(choice != 'b'):
        print(fcolors.GREEN + '\n$ Choose an action: [s]end a message, [b]ack: ' + fcolors.RESET, end="")
        choice = input()
        if(choice == 's'):
            user = ''
            print(fcolors.GREEN + '\n$ Enter the user to send to: ' + fcolors.RESET, end="")
            user = input()
            print(fcolors.GREEN + '\n$ Enter the subject: ' + fcolors.RESET, end="")
            subject = input()
            print(fcolors.GREEN + '\n$ Enter the message: ' + fcolors.RESET, end="")
            message = input()

            if(sendMessage(user, subject, message)):
                print(fcolors.GREEN + '\n$ Sent' + fcolors.RESET)
            else:
                print(fcolors.RED + '\n$ Send failed ' + fcolors.RESET)
        else:
            print(fcolors.RED)
            print(choice, '$ Command not recognized, please try again')
            print(fcolors.RESET)

    menu()

def sendMessage(user, subject, message):
    try:
        r.send_message(user, subject, message)
    except:
        return False

    return True


def menu():
    print(fcolors.GREEN + '$ What would you like to do? [f]rontpage, [s]ubreddits, [m]essaging: ' + fcolors.RESET, end ="")
    choice = input()
    print(fcolors.RESET)
    if(choice == 'f'):
        browse_pages()
    elif(choice == 's'):
        print(fcolors.GREEN + "Enter subreddit name: " + fcolors.RESET, end="")
        browse_pages(input())
    elif(choice == 'm'):
        messaging()
    else:
        print(fcolors.RED + '$ Command not recognized, please try again')
        print(fcolors.RESET)
        menu()

#main entry point
print('$ Welcome to Reddit Console Browser.')
r = praw.Reddit('Reddit console browser by /u/api_test1 v1.0')
login()
menu()
