class Network(object):
    def __init__(self, allowPassiveBridging, authorizedMemberCount, clock, creationTime, enableBroadcast, gateways, ipAssignmentPools, ipLocalRoutes, multicastLimit, name, id, private, relays, rules, v4AssignMode, v6AssignMode):
        self.allowPassiveBridging = allowPassiveBridging    
    
class Member(object):
    def __init__(self, description, activeBridge, address, authorized, clock, ipAssignments, networkId, nodeId, state):
        self.description = description
        self.activeBridge = activeBridge
        self.address = address
        self.authorized = authorized
        self.clock = clock
        self.ipAssignments = ipAssignments
        self.networkId = networkId
        self.nodeId = nodeId
        self.state = state
        
