[![Build Status](https://travis-ci.org/djmgit/SaberX.svg?branch=master)](https://travis-ci.org/djmgit/SaberX)

## Saberx

Saberx is a trigger based monitoring, alerting and action execution system which can be used for self healing. Saberx watches
for specific events in your system and fires its trigger when any such event happens. In reply to the firing of any such trigger,
you can execute an action, like sending alert to you alert management system or any command to heal your system.

A very simple example would be waching your apache server and making sure its receiving connections at port 80. If its not, then
you can configure saberx to fire a trigger for this. When such a trigger gets fired, you may send a curl request call
to your alert manager to raise a alert and at the same time restart your apache server.

Saberx provides many more such triggers like filetrigger (watching over files), Process trigger (watching over processes),
CPUTrigger (watching over CPU), memory trigger (watching over memory) and the already described TCP trigger (watching over
ports).

## Getting started with Saberx

### Installing Saberx

Saberx can be simply installed using following steps:

- Clone/download this repository
- Enter into the repo
- Run ```sudo python3 setup.py install```
- Verify installation using ```saberx --help```

