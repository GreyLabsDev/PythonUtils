### TODO - Test parseSudo funcs
### If your system can`t find termcolor run "sudo pip install termcolor"

### IMPORTS

import os
import sys
import stat
import socket
import pwd
import grp

from termcolor import colored
from pwd import getpwnam  

### VARIABLES

# version description
# 1st number - full-functionally working status <- change it if script is STABLE AND RUN ALL ITS FEATURES 
# 2nd number - count functional changes f.e. work with OS to catch 
#              file permissions, controlling features of some Application, reading from file or generating .html reports

appInfo = ["PMatrix", "v0.8"]
helpCommands = ["show help", "-h", "h", "help", "?", "-?"]
permissions = {
          '7' : 'RWX',
          '6' : 'RW-',
          '5' : 'R-X',
          '4' : 'R--',
          '3' : '-WX',
          '2' : '-W-',
          '1' : '--X',
          '0' : '---',
     }

### FUNCTIONS

def title():
    os.system('clear')
    print colored("\n /------------|  " + appInfo[0]+ "  |------------\ ", 'red', attrs=['blink'])
    print colored(" \____________|  " + appInfo[1] + "     |____________/ ", 'red', attrs=['blink'])

def showTitle():
    print("\n-------------|_O_|-------------")
    print("-------------|__O|-------------")
    print("-------------|OOO|-------------")

def getUserInput():
    return raw_input("\n" + appInfo[0] + "(" + appInfo[1] + ")" + ": ")

def showHelp():
    print colored("\nHelp information:", 'white')
    print colored("\n1. To view the banner use 'show banner' command.", 'white')
    print colored("2. To view help file use 'show help', '-h', 'help', '-?', '?' command.", 'white')
    print colored("3. To check current directory type 'show directory' command.", 'white')
    print colored("4. To check 'os.get' possibilities type 'check user' command.", 'white')
    print colored("5. To check access of some user to some file or dir type 'check permissions <user> <dir/file>' command.", 'white')
    print colored("6. To check access of users list to some list of files or dirs type 'check permissions <list_of_users.txt> <list_of_objects.txt>'  command*.\n\n   *Txt files must contain user names (one user per row) \n    and full paths to objects (one per row)", 'white')

def checkCwd():
    #print colored('os.get_exec_path ' + os.get_exec_path(), 'cyan')
    print colored('\nos.getcwd   - ' + os.getcwd(), 'cyan')
    #print colored('os.getenv ' + os.getenv(), 'cyan')
    print colored('os.getlogin - ' + os.getlogin(), 'cyan')
    #print colored('os.getpid ' + os.getpid(), 'cyan')

def checkAccess(inputLine):
    user = inputLine.split(" ")[0]
    userGroup = getpwnam(user)[3]
    directory = inputLine.split(" ")[1]
    dirStats = os.stat(directory)
    owner = dirStats.st_uid
    ownerName = pwd.getpwuid(owner).pw_name
    ownerGroup = dirStats.st_gid
    directoryPermissions = str(oct(dirStats[0])[-6:])
    userPermissions = 'null'
    
    #compare user and owner names, if user is owner -> user get all Permissions of owner 
    #need to finalize this func
    if ownerName == user:
        userIsOwner = True
    else:
        userIsOwner = False
    
    #need to compare user and owner groups to get Permissions data if user in owner group
    #need to finalize this func
    if ownerGroup == userGroup:
        userInOwnerGroup = True
    else:
        userInOwnerGroup = False

    print colored("\nuser - " + user, 'cyan')
    print colored("user group - " + str(getpwnam(user)[3]), 'cyan')
    print colored("directory - " + directory, 'cyan')
    #print colored("\nuser stats (verbose)- " + str(getpwnam(user)), 'cyan')
    print colored("\nStats for " + directory + ":", 'cyan')
    print colored('Owner UID/name is - ' + str(owner) + "/" + ownerName, 'cyan')
    print colored("directory permissions - " + directoryPermissions, 'cyan')
    #print colored("\ndirectory stats (verbose)- " + str(dirStats), 'cyan')
    
    if userIsOwner:
        print colored("User is owner!", 'cyan')
        userPermissions = permissions[directoryPermissions[3]] 
        print colored("User permissions - " + userPermissions, 'cyan')
    else:
        print colored("User is NOT owner!", 'cyan')
        
    if (userInOwnerGroup and not userIsOwner):
        print colored("User in owner group!", 'cyan')
        userPermissions = permissions[directoryPermissions[4]] 
        print colored("User permissions - " + userPermissions, 'cyan')

    if (not userInOwnerGroup and not userIsOwner):
        print colored("User is NOT in owner group!", 'cyan')
        userPermissions = permissions[directoryPermissions[5]] 
        print colored("User permissions - " + userPermissions, 'cyan')

def checkAccessLite(user, directory):
    userGroup = getpwnam(user)[3]
    dirStats = os.stat(directory)
    owner = dirStats.st_uid
    ownerName = pwd.getpwuid(owner).pw_name
    ownerGroup = dirStats.st_gid
    directoryPermissions = str(oct(dirStats[0])[-6:])
    userPermissions = 'null'
    
    if ownerName == user:
        userIsOwner = True
    else:
        userIsOwner = False
    
    if ownerGroup == userGroup:
        userInOwnerGroup = True
    else:
        userInOwnerGroup = False

    if userIsOwner:
        userPermissions = permissions[directoryPermissions[3]] 
    if (userInOwnerGroup and not userIsOwner):
        userPermissions = permissions[directoryPermissions[4]] 
    if (not userInOwnerGroup and not userIsOwner):
        userPermissions = permissions[directoryPermissions[5]] 
    return userPermissions

def cleanNewlineSymb(inputList):
    result = []
    for i in range(0, len(inputList)):
        if (inputList[i].rstrip("\n") != ""):
            result.append(inputList[i].rstrip("\n"))
    return result

def parseSudoTest():
    input = []
    sudoers = []
    sudoersWl = {}
    i = 0
    input = cleanNewlineSymb(open('/etc/sudoers', 'r').readlines())
    for line in input:
        if ('ALL' in line) and ('#' not in line):
            sudoers.append(line.split('=')[0].split('\t')[0].split(' ')[0])
            if '%' not in line.split('=')[0].split('\t')[0].split(' ')[0]:
                sudoersWl["user"] = line.split('=')[0].split('\t')[0].split(' ')[0]
            else:
                sudoersWl["group"] = line.split('=')[0].split('\t')[0].split(' ')[0]
    print(sudoersWl)

def parseSudoProd():
    input = []
    sudoersWl = {}
    input = cleanNewlineSymb(open('/etc/sudoers', 'r').readlines())
    for line in input:
        if ('ALL' in line) and ('#' not in line):
            if '%' not in line.split('=')[0].split('\t')[0].split(' ')[0]:
                sudoersWl["user"] = line.split('=')[0].split('\t')[0].split(' ')[0]
            else:
                sudoersWl["group"] = line.split('=')[0].split('\t')[0].split(' ')[0]
    return sudoersWl

def checkPermissionsFromLists(inputLine):
    pathToUsersFile = inputLine.split(" ")[0]
    pathToObjectsFile = inputLine.split(" ")[1]
    mode = inputLine.split(" ")[2]
    users = cleanNewlineSymb(open(pathToUsersFile).readlines())
    objects = cleanNewlineSymb(open(pathToObjectsFile).readlines())
    outResult = {}
    sudoersList = parseSudoProd()
    i = 0

    #generate .txt report
    if mode == "-txt":
        outFile = open('Permissions_report.txt', 'w')
        outFile.write(str(socket.gethostname()).upper() + 'STATION')
        for user in users:
            i = i + 1
            outResult[str(i) + " User Name"] = str(user)
            outFile.write("--- " + str(user).upper() + " PERMISSIONS ---" + "\n\n")
            for directory in objects:
                outResult[str(directory)] = checkAccessLite(user, directory)
                outFile.write(str(directory) + " : " + checkAccessLite(user, directory)+ "\n")
            outFile.write("\n------------------------\n\n")
        outFile.close()

    #generate .html tables report for users one by one
    if mode == "-html":
        outFile = open('Permissions_report.html', 'w')
        outFile.write('<!DOCTYPE html>\n<html>\n<head>\n<style>\ntable {\n    border-collapse: collapse;\n    width: 100%;\n}\ntd, th {\nborder: 2px solid #b3c6ff;\n   text-align: left;\n   padding: 6px;\n}\ntr:nth-child(even) {\n   background-color: #b3c6ff;\n}\n</style>\n</head>\n<body>')
        outFile.write("<h1>" + "hostname: " + str(socket.gethostname()).upper() + "</h1>")
        for user in users:
            i = i + 1
            outResult[str(i) + " User Name"] = str(user)
            outFile.write("<h2>" + str(user).upper() + " PERMISSIONS" + "</h2>")
            outFile.write('\n<table>\n<tr>\n    <th>Object/Directory</th>\n    <th>User permissions</th>\n  </tr>')
            for directory in objects:
                outResult[str(directory)] = checkAccessLite(user, directory)
                outFile.write("<tr>\n    <td>" + str(directory) + "</td>\n    <td>" + checkAccessLite(user, directory) + "</td>\n  </tr>")
            outFile.write("\n</table>\n<br>")
        outFile.write("\n</body>\n</html>")
        outFile.close()
        
    #generate .html one-table report for all users and objects
    if mode == "-matrixHTML":
        outFile = open('Permissions_report.html', 'w')
        outFile.write('<!DOCTYPE html>\n<html>\n<head>\n<style>\ntable {\n    border-collapse: collapse;\n    width: 100%;\n}\ntd, th {\nborder: 2px solid #b3c6ff;\n   text-align: left;\n   padding: 6px;\n}\ntr:nth-child(even) {\n   background-color: #b3c6ff;\n}\n</style>\n</head>\n<body>')
        outFile.write("<h1>" + "hostname: " + str(socket.gethostname()).upper() + "</h1>")
        outFile.write('\n<table>\n<tr>\n  	<th>user</th>')
        for directory in objects:
            outFile.write('\n<th>' + str(directory) + '</th>')
        for user in users:
            outFile.write('\n<tr>\n  	<th>' + str(user) + '</th>')
            for directory in objects:
                outFile.write('\n<th>' + checkAccessLite(user, directory) + '</th>')
        outFile.write("\n</table>\n<br>")
        outFile.write("\n</body>\n</html>")
        outFile.close()  
    i = 0

### MAIN
    
inputCom = ''
title()

while input != "exit":

    inputComSrc = getUserInput()

    if len(inputComSrc.split(" ")) == 2:
        inputArgs = "null null null"
        
    if len(inputComSrc.split(" ")) == 4:
        inputArgs = inputComSrc.split(" ")[2] + " " + inputComSrc.split(" ")[3] + " null"

    if len(inputComSrc.split(" ")) == 5: 
        inputArgs = inputComSrc.split(" ")[2] + " " + inputComSrc.split(" ")[3] + " "+ inputComSrc.split(" ")[4]
   
    if len(inputComSrc) > 2:
        try:
            inputCom = inputComSrc.split(" ")[0] + " " + inputComSrc.split(" ")[1]
        except:
            inputCom = inputComSrc

    if len(inputComSrc) == 1:
        inputCom = inputComSrc[0]

    if inputCom == "show directory":
        print("" + os.getcwd())

    if inputCom == "check user":
        checkCwd()
    
    if inputCom == "sudo list":
        print(parseSudoProd())

    if inputCom == "check accesslite":
        print(checkAccessLite("root","/etc"))

    if inputCom == "check permissions":
        if (inputArgs.split(' ')[0] != "null" and inputArgs.split(' ')[1] != "null" and inputArgs.split(' ')[2] == "null"):
            checkAccess(inputArgs)
        if (inputArgs.split(' ')[0] != "null" and inputArgs.split(' ')[1] != "null" and inputArgs.split(' ')[2] == "-txt"):
            checkPermissionsFromLists(inputArgs)
            print("\nPermissions list created in file 'Permissions_report.txt'")
        if (inputArgs.split(' ')[0] != "null" and inputArgs.split(' ')[1] != "null" and inputArgs.split(' ')[2] == "-html"):
            checkPermissionsFromLists(inputArgs)
            print("\nPermissions list created in file 'Permissions_report.html'")
        if (inputArgs.split(' ')[0] != "null" and inputArgs.split(' ')[1] != "null" and inputArgs.split(' ')[2] == "-matrixHTML"):
            checkPermissionsFromLists(inputArgs)
            print("\nPermissions list created in file 'Permissions_report.html'")

    if inputCom == "show banner":
        showTitle()

    if inputCom in helpCommands:
        showHelp()

    if inputCom == "exit":
        print("Exiting...")
        sys.exit()
