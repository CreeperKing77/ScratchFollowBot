'''
CreeperKing77
4/29/24
Purpose: Automated scratch bot, with automated F4F

follows all users who give a profile notification
'''
import scratchattach as scratch3 #main python to scratch interface module | CREDIT: @TimMcCool (scratch and github)
import time #Used for delays between following, for avoiding bans and spam filters
import random #used to randomize follow delays, to help avoid bans better
import math #used for ceiling rounding in
import datetime #used to check if necessary to update the WIWO, and for timestamps

#logs into your account
session = scratch3.login("username", "password")
self = session.connect_user("username")


#OPTIONAL: Prints out your 10 most recent follows and followers
'''
print(f'Your most recent 10 followers: {self.follower_names(limit=10, offset=0)}\n')
print(f'Your most recent 10 follows: {self.following_names(limit=10, offset=0)}\n')
'''

#Tells you the amount of people you're following, and if your account has been banned
print(f'# of Followers: {self.follower_count()}')
print(f'Currently Banned: {session.banned}\n')

#follow loop func
def followLoop(self, startUser):
    #initialized required variables
    fUser = session.connect_user(startUser)
    UserCheck = str(fUser)
    safecount = 0
    saferand = random.randint(11,17)
    recFollowed = []
    
    while 1 == 1:
        #follows user
        UserCheck = str(fUser)
        if not self.is_following(UserCheck):
            safecount += 1
            fUser.follow()
            timestamp = str(datetime.datetime.now())[11:16]
            print(f'Just followed {fUser}. | Time: {timestamp}')

            #comments on users profile
            if not len(recFollowed) == 0:
                if random.randint(0,5) == 0:
                    f4fGreet = ['Hi,','Hello,','Hey,','Greetings!','Hi there,','Hello there,','do you wanna','']
                    f4fDef = ['do you want to', 'wanna','','would you like to','would you be interested in']
                    f4fRan = ['F4F?','F4F?','f4f?','F4F??','f4f??']

                    greetIndex = random.randint(0, len(f4fGreet) - 1)
                    defIndex = random.randint(0, len(f4fDef) - 1)
                    randIndex = random.randint(0, len(f4fRan) - 1)
                    
                    fUser.post_comment(f"{f4fGreet[greetIndex]} {f4fDef[defIndex]} {f4fRan[randIndex]}")
                    print(f'    Posted F4F comment to "{str(fUser)}" \'s profile')
            recFollowed.append(str(fUser))
            print(f'Followed: {len(recFollowed)} users so far')
        else:
            print(f'Follow aborted. {fUser} is already followed.')
            
        #checks for messages
        checkMsgFollow(self)
        #sets your bio to contain your most recent follower
        setBio(self)
        #starts the main follow loop
        timestamp = str(datetime.datetime.now())[11:16]
        print(f'Looking for users to follow... | Time: {timestamp}')
        fList = fUser.follower_names(limit=20, offset=0)
        check = fUser
        for name in fList:
            checkUser = session.connect_user(name)
            self = session.connect_user("F4F-Creeper")
            with open('F4F-Blacklist.txt','r') as infile:
                blacklist = [line.strip() for line in infile.readlines()]
                if not self.is_following(name) and not name in blacklist and not name == 'F4F-Creeper' and not str(name) in recFollowed and not checkUser.follower_count() < 3:
                    fUser = session.connect_user(name)
                    break
                #print follow select exceptions
                else:
                    if not name == 'F4F-Creeper':
                        if self.is_following(name)  or str(name) in recFollowed:
                            print(f'Follow select abort: User {name} already followed')
                        elif name in blacklist:
                            print(f'Follow select abort: User {name} is in blacklist')
                        else:
                            if random.randint(0,399) == 0:
                                #warp in starcraft reference
                                print(f'Follow select abort: User {name} has not enough minerals')
                            else:
                                print(f'Follow select abort: User {name} has not enough followers')
                    if name == fList[-1]:
                        print('No user possibilites')
        if fUser == check:
            recFollowed.append(fUser)
            print('Warning: Found recurring follow loop')
            print('Break attempt: Restarting with original input.')
            break
        else:
            num = random.randint(17,30)
            time.sleep(num)
            if safecount == saferand:
                safecount = 0
                saferand = random.randint(6,11)
                num = random.randint(180,300)
                time.sleep(num)


def screenShotStats(self):
    print('Checking if data save is necessary...')
    #gets the days date
    date = str(datetime.datetime.now())[:10]
    time = int(str(datetime.datetime.now())[11:16].replace(':',''))
    #checks if later in the day
    if time > 2100:
        print('Saving data...')
        #opens file and writes
        with open('FollowData.txt','a') as infile:
            infile.write(f'On {date} at {time}  >    You had {self.follower_count()} followers | You were following {self.following_count()} people\n')
            #infile.write(f'Your follow ratio was {(self.followers() / self.following()):.3f}')


def setBio(self):
    #gets the days date
    date = str(datetime.datetime.now())[:10]
    #opens the save data
    with open('POTD.txt','r') as infile:
        POTDs = infile.readlines()
    #checks for new day or not, if so saves data for new person
    with open('POTD.txt','a') as infile:
        datecheck = str(date) + '\n'
        if not datecheck in POTDs:
            print('Preparing to update WIWO...')
            follower = ''
            if int(date[-2:]) % 10 == 0:
                follower = 'CreeperKing777'
            else:
                while follower == '' or follower == POTDs[-2]:
                    follower = self.follower_names()[random.randint(0,(len(self.follower_names()) - 1))]
            infile.write(follower)
            infile.write('\n')
            infile.write(date)
            infile.write('\n')
            #set the WIWO
            print(f'Updating WIWO... {follower} is POTD')
            self.set_wiwo(f'Person of the Day to follow:\n@{follower}\n(See featured project)\n\nPFP is made by @The1ExE')
        followers = self.follower_names()

    #set the About Me
    self = session.connect_user("F4F-Creeper")
    self.set_bio(f'Just a creeper who loves F4F. If I follow you, please follow back :)\n\nMost recent follower:\n@{self.follower_names(limit=1, offset=0)[0]}')

def checkMsgFollow(self):
    fSelfs = self.following_names(limit=10000, offset=0)
    print(f'Checking messages | Messages: {session.message_count()}')
    if session.message_count() == 0:
        return

    #gets the full list of messages. scratchattach limits you to importing 40 at a time,
    #   to importing 40 at a time, so this imports your messages in "batches" of ten.
    msgs = int(session.message_count())
    messages = []
    counter = 0
    for i in range(math.ceil(msgs / 10)):
        mList = session.messages(limit=10, offset=(counter * 10))
        messages = messages + mList
        counter += 1



    stds = int(self.studio_count())
    studios = []
    counter = 0
    for i in range(math.ceil(stds / 10)):
        sList = self.studios(limit=10, offset=(counter * 10))
        studios = studios + sList
        counter += 1                   
    curating = []
    for studioid in studios:
        curating.append(str(studioid['id']))
        
    with open('F4F-Blacklist.txt','r') as infile:
        blacklist = [line.strip() for line in infile.readlines()]
        if session.message_count() > 0:
            #checks messages and follows users who give them to you
            for messageid in range(session.message_count()):
                if not messages[messageid]['type'] == 'studioactivity' and not messages[messageid]['actor_username'] in blacklist:
                    
                    print(f'receiving message: check {messageid + 1}')
                    if messages[messageid]['type'] == 'curatorinvite':
                        if not str(messages[messageid]['gallery_id']) in curating:
                            studio = session.connect_studio(messages[messageid]['gallery_id'])
                            #print(messages[messageid]['gallery_id'] in curating,'\n')
                            #print(messages[messageid]['gallery_id'],'\n')
                            #print(len(curating))
                            studio.accept_invite()
                            print(f'Joined studio {studio.title}')
                            curating.append(str(studio.id))
                        else:
                            print(f'Studio join abort: Already a member of studio "{studio.title}"')

                    
                    self.update()
                    if not str(messages[messageid]['actor_username']) in fSelfs:
                        target = messages[messageid]['actor_username']
                        target = session.connect_user(target)
                        target.follow()
                        print(f'Just followed {target} via message.')
                    elif not str(messages[messageid]['actor_username']) == 'F4F-Creeper':
                        target = messages[messageid]['actor_username']
                        target = session.connect_user(target)
                        print(f'Follow Message abort: User {str(target)} already followed')
                        
                elif messages[messageid]['actor_username'] in blacklist:
                    print('Message Follow Abort: User in blacklist')
            #checks if you have any new messages before clearing them
            if not int(session.message_count()) > msgs:
                session.clear_messages()
                print('Cleared messages')
            else:
                checkMsgFollow(self)
                session.clear_messages()

#auto reply to F4F request comments
def f4fReply(self, messages, messageid):
    if messages[messageid]['type'] == 'addcomment':
        print(f'Comment notifiaction from "{messages[messageid]["actor_username"]}": " {messages[messageid]["comment_fragment"]} "')
        if messages[messageid]['comment_obj_title'] == 'F4F-Creeper' and 'F4F' in messages[messageid]['comment_fragment'].upper():
            commentid = messages[messageid]['id']
            userid = messages[messageid]['actor_id']
            print('   Replied to F4F request')
            self.reply_comment("Sure", parent_id=commentid, commentee_id=userid)
                
#gets user's choice of whether to only check messages or to follow loop
def getInput():
    choice = input('Enter option\n1. Follow Loop\n2. Check messages loop\n')
    if choice == '1':
        start = input('Input first user: ')
        while 1 == 1:
            try:
                followLoop(self, start)
            except:
                print('      NETWORK EXCEPTION: Delaying and restarting  with original input')
                time.sleep(5)

    elif choice == '2':
        while 1 == 1:
            try:
                checkMsgFollow(self)
            except TimeoutError:
                print('      NETWORK EXCEPTION: Rebooting...')
            time.sleep(5)
            setBio(self)
            time.sleep(10)


screenShotStats(self)
getInput()

