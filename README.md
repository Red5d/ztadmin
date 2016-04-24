ZTAdmin
=======

[ZeroTier One](https://www.zerotier.com/) is a Software Defined Networking service that allows for creating a
scalable, secure P2P virtual network between all your computers no matter where they are.

This tool manipulates the settings on the [admin panel](https://my.zerotier.com) and can be scripted.

I am not associated with ZeroTier Networks, I just think it's awesome.


##Requirements:
* Python 3.x
* Python [requests](https://pypi.python.org/pypi/requests/) module.
* A ZeroTier One account.

Run the script with the "help" option to show the usage information:

Example: `python ztadmin.py help`

If run with no parameters, the script will prompt you to log in, and will then
display a listing of your networks and their members.

##Current features:
I'm in the process of doing a major rewrite of this tool since the ZeroTier API has changed and the tool wasn't very modular 
before. Currently, if run with no parameters, the tool will show a listing of the user's ZeroTier networks and their active members.
* ~~Create a network.~~
* ~~Set attributes of a network or member of a network.~~
* ~~Authorize all pending join requests for a network (useful for mass-deployments).~~
* The zerotier.py file is an importable Python module.
* Show network settings and information for a specified network ID.
* Read api key from a file named ".ztadmin" in the same directory (enables using the tool in automated scripts).

The ".ztadmin" file should be in .ini format like this:
```
[ZeroTier]
API_KEY=supersecret
```

##Future features:
I'll be working on making the tool return more precise information when actions are applied (return network id 
when a network is created, for example) that will be useful when using the tool in scripts.

I haven't personally used ZeroTier One on a large scale or part of an infrastructure, but I know people do.
If you think of a feature that would be useful in that environment, submit an issue or pull request and I'll see what I can do.
I will probably do a little bit more polishing of the existing code though before accepting pull requests in case I change 
some things.
