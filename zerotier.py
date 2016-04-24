import requests, datetime

class ZT(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.api_base = "https://my.zerotier.com/api"

    def request(self, path, data = None):
        if data == None:
            return requests.get(self.api_base+path, headers={'Authorization': 'Bearer '+self.api_key})
        else:
            return requests.get(self.api_base+path, headers={'Authorization': 'Bearer '+self.api_key}, data=data)

    def status(self):
        return self.request("/status").json()

    def self(self):
        return self.request("/self").json()

    def user(self):
        return self.request("/user").json()

    def list_networks(self):
        return [Network(self, n) for n in self.request("/network").json()]

    def network(self, nwid):
        return Network(self, self.request("/network/"+nwid).json())

    def list_members(self, nwid):
        return list(self.request("/network/"+nwid+"/member").json().keys())
    
    def member(self, nwid, mid, netActive = []):
        return Member(self, self.request("/network/"+nwid+"/member/"+mid).json(), netActive)


class Network(object):
    def __init__(self, z, njson):
        self.name = njson['config']['name']
        self.description = njson['description']
        self.id = njson['id']
        self.creationTime = datetime.datetime.fromtimestamp(njson['config']['creationTime'] / float(1000))
        self.private = njson['config']['private']
        self.authorizedMemberCount = njson['config']['authorizedMemberCount']
        self.allowPassiveBridging = njson['config']['allowPassiveBridging']
        self.ipAssignmentPools = njson['config']['ipAssignmentPools']
        self.ipLocalRoutes = njson['config']['ipLocalRoutes']
        self.multicastLimit = njson['config']['multicastLimit']
        self.v4AssignMode = njson['config']['v4AssignMode']
        self.v6AssignMode = njson['config']['v6AssignMode']
        self.gateways = njson['config']['gateways']
        self.relays = njson['config']['relays']
        self.rules = njson['config']['rules']
        self.clock = datetime.datetime.fromtimestamp(njson['config']['clock'] / float(1000))
        self._json = njson
        self._z = z
        
    @property
    def activeMembers(self):
        members = []
        # Get a Member object for each active member of this network.
        for mem in list(self._json['activeMembers'].keys()):
            members.append(self._z.member(self.id, mem, list(self._json['activeMembers'].keys())))

        return members

    
class Member(object):
    def __init__(self, z, mjson, netActive = []):
        self.name = mjson['name']
        self.description = mjson['description']
        self.activeBridge = mjson['config']['activeBridge']
        self.address = mjson['config']['address']
        self.authorized = mjson['config']['authorized']
        self.clock = datetime.datetime.fromtimestamp(mjson['config']['clock'] / float(1000))
        self.ipAssignments = mjson['config']['ipAssignments']
        self.networkId = mjson['networkId']
        self.nodeId = mjson['nodeId']
        self.identity = mjson['config']['identity']
        self.importance = mjson['importance']
        self.recentLog = mjson['config']['recentLog']

        # If a list of active network members has been given, check against that to see if this member is active.
        if netActive != []:
            if self.nodeId in netActive:
                self.online = True
            else:
                self.online = False
        else:
            # ...if not, request the active member list for this member's network.
            if self.nodeId in list(z.request("/network/"+self.networkId).json()['activeMembers'].keys()):
                self.online = True
            else:
                self.online = False

        
