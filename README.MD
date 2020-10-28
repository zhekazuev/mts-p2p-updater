# ADC P2P Plugin Updater

[![N|Solid](https://modernnetsec.io/wp-content/uploads/2020/09/cisco-issues-warning-over-ios-xr-zero-day-flaw-being-targeted-in-the-wild-1.jpg)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

ADC P2P Plugin update package delivery script.

  - Delivery of the update package via SFTP to the /flash/sftp folder
  - Сopy from /flash/sftp to /flash
  - Show current plugin version
  - Show file in directory

### Installation

Git clone from repo
```sh
git clone https://github.com/Zhekazuev/p2p-updater.git p2p-updater
```

Install the dependencies from requirements.txt. 
```sh
cd p2p-updater
cat requirements.txt
source install.sh
```

Start script
```sh
python multiupdate.py patch.so.tgz
```

Example:
```console
[root@server1 p2p-updater]# source env/bin/activate
(env) [root@server1 p2p-updater]# python multiupdate.py patch.so.tgz
10-28-2020 12:36:58 | INFO:                server1: Uploaded /opt/projects/p2p-updater/patch.so.tgz to /sftp/patch.so.tgz
10-28-2020 12:36:58 | INFO:                server2: Uploaded /opt/projects/p2p-updater/patch.so.tgz to /sftp/patch.so.tgz
...
10-28-2020 12:36:58 | INFO:                server3: Uploaded /opt/projects/p2p-updater/patch.so.tgz to /sftp/patch.so.tgz
INPUT: ['y\n', 'copy /flash/sftp/patch.so.tgz /flash/patch.so.tgz\n', 'yes\n', 'show plugin p2p\n', 'dir /flash | grep patch.so.tgz\n']
OUTPUT:
...
INPUT: ['y\n', 'copy /flash/sftp/patch.so.tgz /flash/patch.so.tgz\n', 'yes\n', 'show plugin p2p\n', 'dir /flash | grep patch.so.tgz\n']
OUTPUT:
...
Plugin patch.so.tgz successfully copied
--- 20.8922240734100342 seconds ---
(env) [root@server1 supermassive]# deactivate
[root@server1 supermassive]#
```

License
----
Free Software