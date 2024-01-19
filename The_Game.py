# Run the following commands in mysql command line to make this script work
# create database gamedb;
# use gamedb;
# create table userdb(username varchar(20) primary key, password varchar(100) not null, money float not null, admin varchar(1) default 'F', banned date default NULL);
# create table usermsgs(sender varchar(20) not null,recipient varchar(20) not null, message varchar(1024) not null, IsRead varchar(1) default 'F', MsgTimeStamp datetime default current_timestamp, foreign key (sender) references userdb (username),foreign key (recipient) references userdb (username));
# insert into userdb values('admin','admin123',1.175494351E+38,'T',null);
# Also enter you password in the following variable:
MYSQLPASSWORD=""
# Also, make sure you have the following packages installed
import pymysql as p
import random
import datetime
mydb=p.connect(host='localhost',user='root',password=MYSQLPASSWORD,database='gamedb')
cur=mydb.cursor()
user=False
def curdate():
    cur.execute("SELECT CURRENT_DATE()")
    for i in cur:
        break
    return (i[0])
def update():
    cur.execute(f"update userdb set money = {str(user[2])} where username = '{user[0]}'")
    mydb.commit()
def users():
    cur.execute("select * from userdb")
    temp2={}
    for i in cur:
        temp2[i[0]]=[i[1],i[2],i[3],i[4]]
    global userdict
    userdict=temp2
    return temp2
def display(s):
    s=s.replace("\n","\n\t")
    print(">\t",end="")
    print(s)
horses=['Damascus','Lawyer Ron','Lava Man','Exterminator','Arrogate','Game On Dude','Tabasco Cat','Havre De Grace','Blushing Groom','Bricks And Mortar','Thunder Gulch','Genuine Risk','Gun Runner','Gallant Fox','Runhappy','Raise A Native','Seeking The Gold','Shanghai Bobby','Hail To Reason','Big Brown','Tonalist','Eight Belles','Street Sense','Animal Kingdom','Bernardini','Lady Eli','Omaha Beach','Ferdinand','Pulpit','Graydar','Mineshaft','War Emblem','Storm Cat','Conquistador Cielo','Go For Wand','Skip Away','Tiznow','Sir Barton','Key To The Mint','Palace Malice','Rachel Alexandra','Foolish Pleasure','Regret','Ghostzapper','Assault','Personal Ensign','Afleet Alex','Curlin','Point Given','Wise Dan','Silver Charm','Easy Goer','Lexington','Round Table','Riva Ridge','John Henry']
userhelp="""commands: \t\t cmd
register: \t\t register USERNAME PASSWORD
login: \t\t\t login USERNAME PASSWORD
logout: \t\t logout
message: \t\t msg USER MESSAGE
inbox: \t\t\t inbox
history: \t\t history [USER]
send money: \t\t send USER AMOUNT
gamble: \t\t gamble AMOUNT
horserace: \t\t horserace AMOUNT
work: \t\t\t work
"""
adminhelp="""commands: \t\t cmd
register: \t\t register USERNAME PASSWORD
login: \t\t\t login USERNAME PASSWORD
logout: \t\t logout
message: \t\t msg USER MESSAGE
inbox: \t\t\t inbox
history: \t\t history [USER]
send money: \t\t send USER AMOUNT
gamble: \t\t gamble AMOUNT
horserace: \t\t horserace AMOUNT
work: \t\t\t work
==Admin Commands==
display details: \t display [USERNAME]
update: \t\t update USERNAME AMOUNT
ban: \t\t\t ban USERNAME DAYS
unban: \t\t\t unban USERNAME
"""
cmdlist=["cmd","register","login","logout","msg","inbox","history","send","gamble","horserace","work","display","update","ban","unban"]
instructions=userhelp
display("Hello! This is 'The Game'. Following are the commands you can use.")
display(instructions)
display("CAPITAL words represent arguments. You have to put your own values in place of these. Arguments inside [SQUARE BRACKETS] are optional arguments.")
while True:
    cmd=input()
    if "'" in cmd:
        display("Command cannot contain \"'\"")
        continue
    if cmd=="" or cmd.isspace():
        continue
    if cmd.split()[0].lower() not in cmdlist:
        display("Enter a valid command")
        display(instructions)
        continue
    if cmd.lower()=="cmd":                      #Commands
        display(instructions)
        continue
    if cmd.split()[0].lower()=="register":      #Register
        if len(cmd.split())!=3:
            display("register takes 2 arguments")
            display(instructions)
            continue        
        username=cmd.split()[1].lower()
        password=cmd.split()[2]
        if len(username) > 20:
            display("Username cannot be more than 20 characters")
            continue 
        if len(password)<8:
            display("Password needs to be atleast 8 characters")
            continue
        if len(password)>100:
            display("Password cannot be more than 100 characters")
            continue
        users()
        if username in userdict:
            display("Username taken")
            continue
        display("Confirm Password")
        pswd=input()
        if pswd==password:
            cur.execute(f"insert into userdb (username,password,money) VALUES('{username}','{password}',1000)")
            mydb.commit()
            display("Account Registered. Congratulations!")
        else:
            display("Passwords do not match")
        continue
    if cmd.split()[0].lower()=="login":         #Login
        if len(cmd.split())!=3:
            display("login takes 2 arguments")
            display(instructions)
            continue
        username=cmd.split()[1].lower()
        password=cmd.split()[2]
        users()
        if username in userdict:
            if password==userdict[username][0]:
                if userdict[username][3] is None or userdict[username][3]<curdate():
                    user=[username,userdict[username][0],userdict[username][1],userdict[username][2]]
                    display(f"Login successful! You have ${user[2]}")
                    if user[3]=='T':
                        instructions=adminhelp
                    else:
                        instructions=userhelp
                else:
                    display(f"You are banned till {userdict[username][3]}")
                    continue
            else:
                display("Password Incorrect")
                continue
        else:
            display("User does not exist")
            continue
        continue
    if cmd.lower()=="exit":                     #Exit
        break
    #LOGIN MANDATORY COMMANDS
    if not user:
        display("Login first")
        display(instructions)
        continue
    if cmd.lower()=="logout":                   #Logout
        user=False
        instructions=userhelp
        display("logout successful")
        continue
    if cmd.split()[0].lower()=="msg":           #Message
        if len(cmd.split())<3:
            display("msg takes 2 arguments")
            display(instructions)
            continue
        if len(cmd.partition(cmd.split()[1])[2]) > 1024:
            display("Message cannot be more that 1024 characters")
            continue
        users()
        if cmd.split()[1].lower() not in userdict:
            display("User you are trying to message does not exists")
            continue
        cur.execute(f"insert into usermsgs(sender,recipient,message) values('{user[0]}','{cmd.split()[1]}', '{cmd.partition(cmd.split()[1])[2]}')")
        mydb.commit()
        display("Message sent")
    if cmd.split()[0].lower()=="inbox":         #Inbox
        cur.execute(f"select msgtimestamp,Sender,message from usermsgs where recipient='{user[0]}' and isread='F' order by msgtimestamp desc")
        if cur.rowcount==0:
            display("You have no new messages")
        else:
            display("Here are your messages:")
            for i in cur:
                display(f"|{i[0]}|\t>{i[1]}: {i[2]}")
        cur.execute(f"update usermsgs set isread = 'T' where recipient='{user[0]}'")
    if cmd.split()[0].lower()=="history":         #History
        if len(cmd.split())==1:
            cur.execute(f"select msgtimestamp,Sender,message from usermsgs where recipient='{user[0]}' order by msgtimestamp desc")
            if cur.rowcount==0:
                display("You have no messages")
            else:
                display("Here are your messages:")
                for i in cur:
                    display(f"|{i[0]}|\t>{i[1]}: {i[2]}")
        elif len(cmd.split())==2:
            users()
            if cmd.split()[1] not in userdict:
                display("User does not exist")
            else:
                cur.execute(f"select msgtimestamp,Sender,message from usermsgs where recipient='{user[0]}' and sender='{cmd.split()[1]}' order by msgtimestamp desc")
                if cur.rowcount==0:
                    display("You have no messages from this user")
                else:
                    display("Here are your messages:")
                    for i in cur:
                        display(f"|{i[0]}|\t>{i[1]}: {i[2]}")                
        else:
            display("History takes at max 1 argument")
        continue
    if cmd.split()[0].lower()=="send":          #Send
        if len(cmd.split())!=3:
            display("send takes 2 arguments")
            display(instructions)
            continue
        if not cmd.split()[2].isnumeric():
            display("Enter a valid amount")
            continue
        if int(cmd.split()[2])>user[2]:
            display(f"Not enough funds, need ${str(int(cmd.split()[2])-int(user[2]))} more")
            continue
        users()
        if cmd.split()[1].lower() not in userdict:
            display("User you are trying to send money to does not exists")
            continue
        cur.execute(f"select money from userdb where username = '{cmd.split()[1]}'")
        for i in cur:
            cur.execute(f"update userdb set money = {i[0]+int(cmd.split()[2])} where username = '{cmd.split()[1]}'")
            break
        user[2]-=int(cmd.split()[2])
        update()
        display(f"Money sent. You now have ${user[2]}")
    if cmd.split()[0].lower()=="gamble":        #Gamble
        if len(cmd.split())!=2:
            display("gamble takes 1 arguments")
            display(instructions)
            continue
        if not cmd.split()[1].isnumeric():
            display("Enter a valid amount")
            continue
        if int(cmd.split()[1])>user[2]:
            display(f"Not enough funds, need ${str(int(cmd.split()[1])-int(user[2]))} more")
            continue
        gamblelist=random.sample(range(1,11),3)
        display("Choose a number between 1 and 10")
        while True:
            unum=input()
            if unum.isnumeric():
                unum=int(unum)
                break
            else:
                display("Enter a valid number")
        if unum in gamblelist:
            display(f"YOU WIN\nYou won ${cmd.split()[1]}")
            user[2]+=int(cmd.split()[1])
        else:
            display(f"\nYOU LOST\nThe numbers were {gamblelist}\nYou lost ${cmd.split()[1]}")
            user[2]-=int(cmd.split()[1])
        update()
        display(f"You now have ${str(user[2])}")
        continue
    if cmd.split()[0].lower()=="horserace":     #Horserace
        if len(cmd.split())!=2:
            display("horserace takes 1 arguments")
            display(instructions)
            continue
        if not cmd.split()[1].isnumeric():
            display("Enter a valid amount")
            continue
        if int(cmd.split()[1])>user[2]:
            display(f"Not enough funds, need ${str(int(cmd.split()[1])-int(user[2]))} more")
            continue
        temp=random.sample(horses,5)
        temp2=""
        for i in temp:
            temp2+=f"{i}\n"
        display(temp2)
        display("Which horse would you like to bet on?")
        while True:
            userhorse=input()
            if userhorse.title() in temp:
                break
            else:
                display("Enter a valid hosre name")
        random.shuffle(temp)
        display("The results of the race are")
        temp2=""
        for i in range(len(temp)):
            temp2+=f"{i+1}. {temp[i]}\n"
        display(temp2)
        ndx=temp.index(userhorse.title())
        if ndx==0:
            user[2]+=2*int(cmd.split()[1])
            update()
            display(f"You won ${2*int(cmd.split()[1])}. You now have ${user[2]}")
        elif ndx==1:
            user[2]+=int(cmd.split()[1])
            display(f"You won ${int(cmd.split()[1])}. You now have ${user[2]}")
        elif ndx==2:
            display(f"Draw. You now have ${user[2]}")
        elif ndx==3 or ndx==4:
            user[2]-=int(cmd.split()[1])
            display(f"YOU LOST! You now have ${user[2]}")
        continue
    if cmd.split()[0].lower()=="work":          #Work
        temp=random.choices(range(50),k=4)
        ans=temp[0]+temp[1]*temp[2]-temp[3]
        display(f"What is {temp[0]} + {temp[1]} x {temp[2]} - {temp[3]}")
        while True:
            uans=input()
            if uans.isnumeric():
                if int(uans)==ans:
                    user[2]+=50
                    update()
                    display("CORRECT! You earned $50")
                else:
                    display(f"INCORRECT! The correct answer was {ans}")
                break
            else:
                display("Enter a valid number")
    #ADMIN MANDATORY COMMANDS
    if user[3]=='T':
        if cmd.split()[0].lower()=="update":    #Update
            if len(cmd.split())!=3:
                display("You need to add 2 arguements after update; the username and the new amount.")
                display(instructions)
                continue
            users()
            if cmd.split()[1].lower() not in userdict:
                display("User does not exist")
                continue
            if not cmd.split()[2].isnumeric():
                display("Enter a valid amount of money")
                continue
            cur.execute(f"update userdb set money={str(cmd.split()[2])} where username ='{cmd.split()[1].lower()}'")
            mydb.commit()
            display("Money successfully updated.")
            continue
        if cmd.split()[0].lower()=="display":   #Display
            if len(cmd.split())!=2 and len(cmd.split())!=1:
                display("Display takes 1 argument at max")
                display(instructions)
                continue
            users()
            if len(cmd.split())==1:
                print("Username,Password,Money,Admin,Banned")
                for i in userdict:
                    print(f"{i},{userdict[i][0]},{userdict[i][1]},{userdict[i][2]},{userdict[i][3]}")
            if len(cmd.split())==2:
                if cmd.split()[1].lower() not in userdict:
                    display("User does not exist")
                    continue
                display(f"Username: {cmd.split()[1].lower()}\nPassword: {userdict[cmd.split()[1].lower()][0]}\nMoney: ${userdict[cmd.split()[1].lower()][1]}\nAdmin Status: {userdict[cmd.split()[1].lower()][2]}")
            continue
        if cmd.split()[0].lower()=="ban":       #Ban
            if len(cmd.split())!=3:
                display("Ban takes 2 arguments;")
                display(instructions)
                continue
            if not cmd.split()[2].isnumeric():
                display("Enter a valid amount of days")
                continue
            users()
            if cmd.split()[1].lower() not in userdict:
                display("User does not exist")
                continue
            cur.execute(f"update userdb set banned='{curdate()+datetime.timedelta(days=int(cmd.split()[2]))}' where username ='{cmd.split()[1].lower()}'")
            mydb.commit()
            display("User banned")
            continue
        if cmd.split()[0].lower()=="unban":     #Unban
            if len(cmd.split())!=2:
                display("Unban takes 1 arguments;")
                display(instructions)
                continue
            users()
            if cmd.split()[1].lower() not in userdict:
                display("User does not exist")
                continue
            cur.execute(f"update userdb set banned=NULL where username ='{cmd.split()[1].lower()}'")
            mydb.commit()
            display("User unbanned")
            continue
mydb.close()
