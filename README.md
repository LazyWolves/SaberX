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

**Currently Saberx only supports Linux.**

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

```sleep_period``` is the amount of time (in seconds) saberx will wait before initiating the next run.

## How Saberx works

This setion describes how Saberx works, what it does and how it does and how to configure it properly.

### Actions and Groups

As already mentioned above, in the yaml file (which we will refer as the **action yaml**), we can provide a list of groups.

Each group comprises of a list of actions.

Each action comprises of a **trigger** and a **execute** section.

The important and interesting thing to be notes here is Saberx evaluates all the groups concurrently. It spawns a thread
for each group. So two actions in two different group will be executed concurrently. However, inside the same group, the
actions are executed synchronously.

Lets take an example:

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
      threshold: 1
    execute:
    - "command 1"
    - "command 2"
  - actionname: action_2
    trigger:
      type: TCP_TRIGGER
      check: tcp_fail
      host: 127.0.0.1
      port: 443
      attempts: 3
      threshold: 1
    execute:
    - "command 1"
    - "command 2"
- groupname: grp2
  actions:
  - actionname: action_1
    trigger:
      type: PROCESS_TRIGGER
      check: cmdline
      regex: "nginx"
      count: 1
      operation: '>='
    execute:
    - "command 1"
```

In the above action yaml, grp1 and grp2 will be run concurrently. Saberx will spawn two threads and allocate one group to each
thread. This would mean both the TCP triggers will be evaluated concurrently on each run with the process trigger 
(more on process trigger below). However both tcp triggers will be evaluated synchronously. That is first saberx will evaluate
the tcp trigger for port 80 and then for port 443.

If the above seems to be confusing, the here is a small description of the control flow for the above config.

At the start of each run, Saberx will spawn a thread for each group. In this case there will be two threads in total. The thread
responsible for a group, lets consider the first group, will first evaluate grp1, once it is done with grp1 (if trigger is
fired it will run commands or simply pass), it will try to evaluate the second trigger (the one for port 443).

The second thread responsible for grp2 will also be excuting concurrently along with grp1 and hence the action contained with
in grp2 (and hence the trigger and execute sections) will be evaluated concurrently to the actions present in grp1.

Here another important thing worth noting is, if in the same group, one action's execute section fails, that action is marked as
a failure and all the remaining actions in that group will be ignored.

For example, in the above scanario, if command 1 in action_1 in grp_1 fails (throws exception, returns non 0 exit code), then
action_1 will be marked as a failure and action_2 in grp1 will be skipped in that run. However this wont affect any action
in grp2.

In short, if you want your actions to be evaluated concurrently with no **dependency** between them, consider putting them in
separate groups. If you want your actions to be synchronous, then put them in same group.

### Execute section

Each trigger should have an execute section. This section/key contains a list of commands to be executed if the corresponding
trigger is fired. Lets take an example:

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
    - "command 1"
    - "command 2"
    - "command 3"
    - "command 4"
```

In this example, if the above trigger fails, that is saberx is unable to open connection to 127.0.0.1:80, then Saberx will try to
execute all the 4 commands one after the other synchronously.

Omce again, it is to be noted over here that if any of the commands fail, the rest of the command will be ignored in that run.

Saberx marks the execution of a command as failure if, the command throws an error/exception or it returns a non 0 return code.

## What happens in Saberx run

Before Saberx initiates a run, it tries to aquire a lock. It does so by trying to create a lock file in the configured lock
directory (present in /etc/saberx/saberx.conf).

If Saberx fails to create the file, the run fails. If a lock file is already present, it means the previous run is not yet
finished, so it does nothing and waits for the next turn.

If it succeeds in creating the lock file, then the run begins. Saberx first parses the action yaml, extarcts all the groups.
Following that it spawns one thread for each group. Each thread evaluates the actions of the concerned groups. Whenever a triiger
in any action is fired, it executes the commands present in that action's execute section.

Once all the threads have done their job, the lock file is deleted and Saberx waits for the next run. If Saberx is unable to
delete the lock file it throws error and exits.

## Triggers

Saberx provides the following 5 triggers as of now:

- TCP_TRGIGGER
- PROCESS_TRIGGER
- CPU_TRIGGER
- MEMORY_TRIGGER
- FILE_TRIGGER

### TCP_TRIGGER

TCP_TRIGGER watches for tcp connection to a given host and port. It gets triggered when it succeeds/fails in creating normal/ssl
connection to a given host and port.

Example:

```
- actionname: action_1
    trigger:
      type: TCP_TRIGGER
      check: tcp_fail
      host: 127.0.0.1
      port: 8899
      attempts: 3
      threshold: 1  
    execute:
    - "command 1"
```
- ```type``` tells what kind of trigger it is. It is mandatory for all triggers.

- ```check``` denotes what we want to check. If we want to fire our trigger on tcp failure then we have to set this to
  ```tcp_failure```. If we want it to fire on tcp connect, then we have to set this to ```tcp_connect```

- ```host``` tells the host to connect to. Can be hostname or IP address. Default is ```127.0.0.1```.

- ```port``` tell the port of the host to connect to. Default is ```80```.

- ```ssl``` need to be set to True we want to create TCP connection with SSL or else False. Default is ```False```.

- ```timeout``` is the time in seconds after which saberx will give up trying to establish the connection and report as failure.
  Default is 5.

- ```attempts``` is the number of times saberx should try to establish a connection to the given host, port. Default is 3.

- ```threshold``` is the minimum number of success or failure saberx must enounter in order to report the same.

### PROCESS_TRIGGER

Process trigger watches for processes with given name/regex or commandline arguments matcing given regex. If saberx
finds a process with the matching conditionals, then it fires this trigger based on certain conditions.
For example you can instruct saberx to fire process trigger if there are more than (or less than or equal to) 5 (or any number)
process with the name "nginx" running in the system.

Example:

```
- actionname: action_2
    trigger:
      type: PROCESS_TRIGGER
      check: cmdline
      regex: "k.* start"
      count: 1
      operation: '>='
    execute:
    - "command 1"
```

- ```type``` tells what kind of trigger it is. It is mandatory for all triggers.

- ```check``` can be set to either ```name``` or ```cmdline```. If set to name then saberx will look for name and if set to
  cmdline then it will look out for processes with arguments matching the given regex.
  
- ```regex``` is the regex pattern to match against the process name or command line arguments.

- ```count``` can be any integer. Saberx checks if the number of desired procsses in the system are greater than or less than
  or equal to (as configured) ```count``` then the trigger is fired.
  
- ```operation``` can be anything among ```<, >, <=, >=, =```. This is how Saberx will compare the number of desired processes
  against the provided ```count``` in order to fire the trigger.
  
  In the above example, the trigger will be fired if the number of processes in the system having command line matching the
  given regex is greater than or equal to 1.
  
  ### CPU_TRIGGER
  
  
  
  

