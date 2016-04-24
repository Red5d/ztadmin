#! /usr/bin/env python

import sys, requests, json, pprint, configparser
from zerotier import *
from os.path import expanduser
home = expanduser("~")

# Check for .ztadmin config file with api key
config = configparser.ConfigParser()
savecreds = configparser.RawConfigParser()
c = config.read(home+'/.ztadmin')
key = ""

if len(c) != 0:
    key = config.get('ZeroTier', 'API_KEY')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Create ZeroTier object.
z = ZT(key)

# Get list of network objects
networks = z.list_networks()

# Show listing of networks and their active members
print("Networks:")
for net in networks:
    print(bcolors.YELLOW+net.name+" ("+net.id+"):"+bcolors.ENDC)
    for member in net.activeMembers:
        print("\t"+member.name.ljust(18)+"\t"+member.address+"\t"+member.ipAssignments[0])
    
    print("")
