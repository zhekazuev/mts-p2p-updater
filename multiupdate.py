#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is a script for automate pushing Updates for P2P Plugin
    Script by Eugene Zuev (ezuev)
"""
from client import RemoteClient
from threading import Thread
from pathlib import Path
import paramiko
import config
import click
import time
import re


def run_commands(device, file):
    project_dir = Path().resolve()
    local_path = Path(project_dir, file)
    remote_path = f'/sftp/{file}'
    host = device.get("host")
    hostname = device.get("hostname")

    user = config.StarOS.script_user
    password = config.StarOS.script_password

    try:
        with RemoteClient(host, user, password) as ssh:
            ssh.upload_file(hostname, local_path, remote_path)
            ssh.shell(["y\n",
                       f"copy /flash/sftp/{file} /flash/{file}\n",
                       "yes\n",
                       "show plugin p2p\n",
                       f"dir /flash | grep {file}\n"],
                      pause=2)
            ssh.disconnect()
    except paramiko.SSHException as sshException:
        print(f'Error: {sshException}')


@click.command()
@click.argument("path")
@click.option("--p", default=False, help='If you need to start printing info to Console add this option with key "y"')
def main(path, p):
    """
    Input path, for example:
    /opt/scripts/Python/p2pupdater/patch_libp2p-2.51.1246.so.tgz
    Full command example:
    python3.6 multiupdate.py /opt/scripts/Python/p2pupdater/patch_libp2p-2.51.1246.so.tgz
    or
    python3.6 multiupdate.py patch_libp2p-2.51.1246.so.tgz
    """
    devices = config.StarOS.all_hosts

    files = re.findall(".*(patch_libp2p.+.so.tgz)", path)

    try:
        file = files[0]
    except IndexError as index_error:
        print("Error in filename")
        return index_error

    start_time = time.time()
    threads = []
    for device in devices:
        t = Thread(target=run_commands, args=(device, file))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"Plugin {file} successfully copied")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
