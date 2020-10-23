"""Client to handle connections and actions executed against a remote host.
Original repo - https://github.com/hackersandslackers/paramiko-tutorial
Information - https://hackersandslackers.com/automate-ssh-scp-python-paramiko/"""
from paramiko import SSHClient, AutoAddPolicy
from paramiko.auth_handler import AuthenticationException, SSHException
from log import logger
import time


class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, host, user, password, remote_path="/"):
        self.host = host
        self.user = user
        self.password = password
        # self.ssh_key_filepath = ssh_key_filepath
        self.remote_path = remote_path
        self.client = None
        self.channel = None
        self.scp = None
        self.conn = None
        # self._upload_ssh_key()

    # @logger.catch
    # def _get_ssh_key(self):
    #     """ Fetch locally stored SSH key."""
    #     try:
    #         self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath)
    #         logger.info(f'Found SSH key at self {self.ssh_key_filepath}')
    #     except SSHException as error:
    #         logger.error(error)
    #     return self.ssh_key

    # @logger.catch
    # def _upload_ssh_key(self):
    #     try:
    #         system(f'ssh-copy-id -i {self.ssh_key_filepath} {self.user}@{self.host}>/dev/null 2>&1')
    #         system(f'ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.host}>/dev/null 2>&1')
    #         logger.info(f'{self.ssh_key_filepath} uploaded to {self.host}')
    #     except FileNotFoundError as error:
    #         logger.error(error)

    @logger.catch
    def _connect(self):
        """Open connection to remote host. """
        if self.conn is None:
            try:
                self.client = SSHClient()
                self.client.load_system_host_keys()
                self.client.set_missing_host_key_policy(AutoAddPolicy())
                self.client.connect(
                    self.host,
                    username=self.user,
                    password=self.password,
                    # key_filename=self.ssh_key_filepath,
                    look_for_keys=True,
                    timeout=5000
                )
            except AuthenticationException as error:
                logger.error(f'Authentication failed: did you remember to change password? {error}')
                raise error
        return self.client

    @logger.catch
    def _shell_connect(self):
        """Open connection to remote host. """
        if self.conn is None:
            try:
                self.client = SSHClient()
                self.client.load_system_host_keys()
                self.client.set_missing_host_key_policy(AutoAddPolicy())
                self.client.connect(
                    self.host,
                    username=self.user,
                    password=self.password,
                    # key_filename=self.ssh_key_filepath,
                    look_for_keys=True,
                    timeout=5000
                )
                self.channel = self.client.invoke_shell()
            except AuthenticationException as error:
                logger.error(f'Authentication failed: did you remember to change password? {error}')
                raise error
        return self.channel

    def disconnect(self):
        """Close ssh connection."""
        if self.client:
            self.client.close()
        if self.scp:
            self.scp.close()

    # @logger.catch
    # def bulk_upload(self, files):
    #     """
    #     Upload multiple files to a remote directory.
    #
    #     :param files: List of paths to local files.
    #     :type files: List[str]
    #     """
    #     self.conn = self._connect()
    #     uploads = [self._upload_single_file(file) for file in files]
    #     logger.info(f'Finished uploading {len(uploads)} files to {self.remote_path} on {self.host}')

    # def _upload_single_file(self, file):
    #     """Upload a single file to a remote directory."""
    #     upload = None
    #     try:
    #         self.scp.put(
    #             file,
    #             recursive=True,
    #             remote_path=self.remote_path
    #         )
    #         upload = file
    #     except SCPException as error:
    #         logger.error(error)
    #         raise error
    #     finally:
    #         logger.info(f'Uploaded {file} to {self.remote_path}')
    #         return upload

    def download_file(self, file):
        """Download file from remote host."""
        self.conn = self._connect()
        self.scp.get(file)

    @logger.catch
    def execute_commands(self, commands):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """
        self.conn = self._connect()
        responses = ""
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            output = ""
            for line in response:
                output += line
            responses += response
            logger.info(f'\nINPUT: {cmd}\nOUTPUT:\n {output}')
        return responses

    @logger.catch
    def shell(self, commands, pause=1, buffer=10000):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        :type commands: List[str]
        :param pause: Time to wait for one command
        :type pause: int
        :param buffer: Max recv buffer
        :type buffer: int
        """
        self.channel = self._shell_connect()
        responses = ""
        for cmd in commands:
            self.channel.send(cmd)
            time.sleep(pause)
            response = self.channel.recv(buffer).decode('utf8')
            output = ""
            for line in response:
                output += line
            responses += response
        logger.info(f'\nINPUT: {commands}\nOUTPUT:\n {responses}')
        return responses
