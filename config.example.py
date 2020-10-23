import os


script_user = os.environ["SCRIPTS_USER"]
script_password = os.environ["SCRIPTS_PASS"]

hosts = [('hostname1', '1.1.1.1'), ('hostname2', '1.1.1.2')]


class StarOS:
    script_user = 'user'
    script_password = 'password'
    # STAROS_SCRIPTS_TACACS_USER = os.environ['STAROS_SCRIPTS_TACACS_USER']
    # STAROS_SCRIPTS_TACACS_PASS = os.environ['STAROS_SCRIPTS_TACACS_PASS']

    all_hosts = [{"hostname": "hostname1", "host": "1.1.1.1"},
                 {"hostname": "hostname2", "host": "1.1.1.2"}]
