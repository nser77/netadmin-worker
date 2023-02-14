# netadmin-worker

## Requirements
Before installation, make sure that your system has the following packages installed:

```
root@ubuntu:/opt# apt-get update
root@ubuntu:/opt# apt-get install git virtualenv
```

## Installation
Download and install NETADMIN with ```git``` and ```venv```.
```
root@ubuntu:/opt# cd /opt
root@ubuntu:/opt# git clone git@github.com:nser77/netadmin-worker.git
root@ubuntu:/opt/netadmin-worker# cd netadmin-worker/
root@ubuntu:/opt/netadmin-worker# virtualenv ./venv
root@ubuntu:/opt/netadmin-worker# source ./venv/bin/activate
(venv) root@ubuntu:/opt/netadmin-worker# pip install -r requirements.txt
(venv) root@ubuntu:/opt/netadmin-worker# deactivate
```

Create NETADMIN user and assign the ownerships:
```
root@ubuntu:/opt/netadmin-worker# adduser --system --group --home /opt/netadmin-worker/netadmin-worker --no-create-home netadmin_worker
root@ubuntu:/opt/netadmin-worker# chown -R netadmin_worker: /opt/netadmin-worker
```
