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
python multiupdate.py patch_libp2p-2.51.1246.so.tgz
```


License
----
Free Software