[![Build Status](https://travis-ci.org/djmgit/SaberX.svg?branch=master)](https://travis-ci.org/djmgit/SaberX)

## Saberx

Saberx is a trigger based monitoring, alerting and action execution system which can be used for self healing. Saberx watches
for specific events in your system and fires its trigger when any such event happens. In reply to the firing of any such trigger,
you can execute an action, like sending alert to you alert management system or any command to heal your system.

A very simple example would be waching your apache server and making sure its accessable at port 80. If its not, then
you can configure saberx to fire a trigger for this. When such a trigger gets fired, you may send a curl request call
to your alert manager to raise a alert and at the same time restart your apache server.

Saberx provides many more such triggers like filetrigger (watching over files), Process trigger (watching over processes),
CPUTrigger (watching over CPU), memory trigger (watching over memory) and the already described TCP trigger (watching over
ports).

Currently Saberx only supports Linux.

## Getting started with Saberx

### Installing Saberx

Saberx can be simply installed using following steps:

- Clone/download this repository
- Enter into the repo
- Run ```sudo python3 setup.py install```
- Verify installation using ```saberx --help```

### Setting up a simple Trigger and action

Lets setup a simple trigger like the once metioned in the above example. We will be setting up a trigger for Apache web server.
The trigger will check whether the server is accessable (accepting connections) at port 80. If not, the trigger will be fired,
and as a response to this trigger we will restart Apache.

Open **/etc/saberx/saberx.yaml** and paste the following in it

```
  actiongroups:
- groupname: grp1
  actions:
  - actionname: action_1
    trigger:
      type: TCP_TRIGGER
      check: tcp_fail
      host: 127.0.0.1
      port: 80
      attempts: 3
      threshold: 2
    execute:
    - "systemctl restart apache2"
```

Open **/etc/saberx/saberx.conf** and paste the following:

```

[DEFAULT]

action_plan = /etc/saberx/saberx.yaml
lock_dir = /run
sleep_period = 5

```

**Note**
```
Note: The above example assumes that you have Apache web server installed and configured to receive connections at port 80
It also assumes that Apache is being managed by systemd, which is the default case with most debian based systems.
```

Make sure the server is up and running.

Now start saberx by just typing  ```saberx```. Optionally you can start saberx using ```saberx &``` to push it to background.
Alternatively you can create a systemd service file for saberx (more on that later). The user with which saberx is being run
should have permission to restart Apache2.

In order to simulate an issue (refusal of connections at port 80), we will intentionally stop apache2:

```
sudo systemctl stop apache2

```

This will cause Apache2 to stop listening and port 80 and start rejecting connections. It will not take apache more than 5
seconds (since that is the sleep time we have configured and can be reduced) to detect that Apache is refusing connections at
port 80 and it will fire the TCPTrigger we have defined. Once that happens, the action we have provided will get excuted, thereby
restarting Apache.

### Understanding the config

```
  actiongroups:
- groupname: grp1
  actions:
  - actionname: action_1
    trigger:
      type: TCP_TRIGGER
      check: tcp_fail
      host: 127.0.0.1
      port: 80
      attempts: 3
      threshold: 2
    execute:
    - "systemctl restart apache2"
```

The above is the Trigger and action configuration. It contains only one action group: grp1 and grp 1 contains only one action: action_1. There can be multiple action groups and each group can contain multiple triggers. More on this later.

The type of the Trigger we used above is ```TCP_TRIGGER```. This triiger is only used to check tcp connections to given
host, port.

```check``` is set to ```tcp_fail```. This essectially means that the trigger will get fired when saberx fails to open a
tcp connection to the give host, port.

```host``` is the host we are monitoring and ```port``` is the respective port we are openning the TCP connection to.

```attempts``` indicate the number of attempts we are going to make. Here saberx tries to make 3 attempts at openning a tcp
connection port 80. ```threshold``` is the minimum number of times the tcp connection should fail to fire the trigger. So. in the
above example if saberx fails to open TCP connection to 127.0.0.1:80 twice out of the three times it will try, then the trigger
will get fired.

Under ```execute``` we give a list of commands to be executed when a trigger is fired. It can be any linux commnad or script
that needs to be executed. It is to be noted that if any command in the list of command fails or throws error or exit code if non
0, the rest of the commands after that is ignored.

```

[DEFAULT]

action_plan = /etc/saberx/saberx.yaml
lock_dir = /run
sleep_period = 5

```
This is the main conf file. It contains path to the yaml file containg the actions and triggers.

```action_plan``` is the path to the yaml file containing actions and triggers (the one mentioned above)

```lock_dir``` is the directory where saberx stores a lock file. This file acts as a lock making sure the next run of saberx
takes place only after the previous run has ended and all old threads are gone.

```sleep_period``` is the amount of time saberx will wait before initiating the next run.



