#! /usr/bin/env python

import sys, requests, json, getpass, pprint, ConfigParser
from os.path import expanduser
home = expanduser("~")
# Create session for login.
s = requests.Session()

# Set ZeroTier API URL variables.
ztAuth_URL = 'https://my.zerotier.com/api/_auth/local'
ztNetworkData_URL = 'https://www.zerotier.com/api/network'
ztCreateNetwork_URL = 'https://www.zerotier.com/api/task/createNetwork'

# Check for .ztlogin config file with login info (so user doesn't have to keep typing username/pw for repeated operations)
config = ConfigParser.ConfigParser()
savecreds = ConfigParser.RawConfigParser()
c = config.read(home+'/.ztlogin')
user = ""
pw = ""

if len(c) != 0:
    user = config.get('ZeroTier', 'username')
    pw = config.get('ZeroTier', 'password')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Login to ZeroTier.
def login():
    global user
    global pw
    if user == "":
        user = raw_input("Username: ")
        pw = getpass.getpass()
    
    info = {
        'login': user,
        'password': pw
    }
    
    l = s.post(ztAuth_URL, data=info, headers={'Content-Type': 'application/json'}))
    
    if l.ok == True:
        print bcolors.OKGREEN+"Login Successful."+bcolors.ENDC
        if len(c) == 0:
            save = raw_input("Save username/password? (y/n): ")
            if save == "y" or save == "Y":
                config.add_section('ZeroTier')
                config.set('ZeroTier', 'username', user)
                config.set('ZeroTier', 'password', pw)
                with open(home+'/.ztlogin', 'wb') as configfile:
                    config.write(configfile)

    else:
        print "Login failed!"
        login()
    
# Retrieve all network data.
def getData():
    r = s.get(ztNetworkData_URL)
    data = json.loads(r.text)
    return data

# Retrieve data for specific network.
def getNetwork(networkID):
    r = s.get(ztNetworkData_URL+"/"+networkID)
    network = json.loads(r.text)
    return network

# List network names and members.
def list_networks():
    data = getData()
    
    print "Networks:"
    for network in data.keys():
        print data[network]['desc']+" ("+network+"):"
        for member in data[network]['/member'].keys():
            status = ""
            if data[network]['/member'][member]['_online'] == 1:
                status = bcolors.OKGREEN+"Online"+bcolors.ENDC
            else:
                status = bcolors.FAIL+"Offline"+bcolors.ENDC

            try:
                print "\t"+status+"\t"+data[network]['/member'][member]['id']+"\t"+data[network]['/member'][member]['ipAssignments']+"\t"+data[network]['/member'][member]['notes']
            except KeyError:
                # "notes" field is blank
                print "\t"+status+"\t"+data[network]['/member'][member]['id']+"\t"+data[network]['/member'][member]['ipAssignments']
                
        
# Set/change an attribute on a network member.
def setMemberData(networkID, memberID, attribute, value):
    memberData = getData()[networkID]['/member'][memberID]
    allowedAttributes = ["ipAssignments", "activeBridge", "authorized", "notes"]
    
    if attribute not in allowedAttributes:
        print "Invalid attribute '"+attribute+"'."
        print "Allowed attributes: "+str(allowedAttributes)
        s.close()
        sys.exit()
    
    memberData[attribute] = value

    r = s.post(ztNetworkData_URL+"/"+networkID+'/member/'+memberID, data=memberData)
    
    if r.ok:
        print "Set "+str(attribute)+" for "+str(memberID)+" to "+str(value)+"."
    else:
        print "Failed to set "+str(attribute)+" for "+str(memberID)+"."
        
# Create a new network.
def createNetwork(name):
    info = { "name": name }
    
    r = s.post(ztCreateNetwork_URL, data=info)
    
    if r.status_code == 409:
        # Network name already exists.
        print r.text
    elif r.status_code != 200:
        print "Failed to create network!"
    else:
        print "Network '"+name+"' created."

# Set/change an attribute on a network.
def setNetworkData(networkID, attribute, value):
    # Retrieve network data and create array of writable attributes to check against.
    networkData = getNetwork(networkID)
    allowedAttributes = ["name", "desc", "enableBroadcast", "etherTypes", "infrastructure", "multicastLimit", "private", "v4AssignMode", "v4AssignPool", "v6AssignMode", "v6AssignPool"]
    
    # Check if the specified attribute is writable (included in allowedAttributes array).
    if attribute not in allowedAttributes:
        print "Invalid attribute '"+attribute+"'."
        print "Allowed attributes: "+str(allowedAttributes)
    else:
        networkData[attribute] = value
        r = s.post(ztNetworkData_URL+"/"+networkID, data=networkData)
        
        if r.ok:
            print "Set "+str(attribute)+" for "+str(networkID)+" to "+str(value)+"."
        else:
            print "Failed to set "+str(attribute)+" for "+str(networkID)+"."
            
def authorizeAll(networkID):
    # Authorize all computers asking to join a networkID (useful for mass-deployments)
    data = getData()
    for member in data[networkID]['/member'].keys():
        setMemberData(networkID, member, "authorized", 1)
            
# Show info for specified network.
def networkInfo(networkID):
    network = getNetwork(networkID)
    del network['/member']
    pprint.pprint(network)


# Begin main program.
#
# Log into ZeroTier and parse command options.

if len(sys.argv) == 1:
    login()
    list_networks()
    
elif sys.argv[1] == "create":
    login()
    createNetwork(sys.argv[2])
    
elif sys.argv[1] == "setmember":
    if len(sys.argv) == 6:
        login()
        setMemberData(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print "Usage: setmember <networkid> <memberid> <attribute> <value>"
        
elif sys.argv[1] == "setnetwork":
    if len(sys.argv) == 5:
        login()
        setNetworkData(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print "Usage: setnetwork <networkid> <attribute> <value>"
        
elif sys.argv[1] == "authall":
    if len(sys.argv) == 3:
        login()
        authorizeAll(sys.argv[2])
        
elif sys.argv[1] == "networkinfo":
    if len(sys.argv) == 3:
        login()
        networkInfo(sys.argv[2])
    else:
        print "Usage: networkinfo <networkid>"
        
else:
    # If no valid command options found, print usage."
    print "Usage: <command> <options>..."
    print ""
    print "create\t\t<name>\t\t\t\t\t\tCreate a new network."
    print "setmember\t<networkid> <memberid> <attribute> <value>\tSet/change an attribute on a network member."
    print "setnetwork\t<networkid> <attribute> <value>\t\t\tSet/change an attribute on a network."
    print "authall\t\t<networkid>\t\t\t\t\tAuthorize all computers asking to join a network id."
    print "networkinfo\t<networkid>\t\t\t\t\tShow info for a specified network."

s.close()

