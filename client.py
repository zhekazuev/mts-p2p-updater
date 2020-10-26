"""Client to handle connections and actions executed against a remote host.
Original repo - https://github.com/hackersandslackers/paramiko-tutorial
Information - https://hackersandslackers.com/automate-ssh-scp-python-paramiko/"""
from paramiko.auth_handler import AuthenticationException, SSHException
from paramiko import SSHClient, AutoAddPolicy, SFTPError
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
        self.sftp = None
        self.conn = None
        # self._upload_ssh_key()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

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
    def __connect(self):
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
                    # look_for_keys=True,
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
        if self.sftp:
            self.sftp.close()

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

    @logger.catch
    def bulk_upload(self, files):
        """
        Upload multiple files to a remote directory.
        :param files: List of local files to be uploaded.
        :type files: List[str]
        """
        self.conn = self.__connect()
        uploads = [self.__upload_single_file(self.host, file, self.remote_path) for file in files]
        logger.info(f'Finished uploading {len(uploads)} files to {self.remote_path} on {self.host}')

    def __upload_single_file(self, hostname, file, remote_path, pause=0):
        """Upload a single file to a remote directory."""
        upload = None
        self.sftp = self.__connect().open_sftp()
        try:
            self.sftp.put(file, remote_path)
            time.sleep(pause)
            upload = file
            self.sftp.close()
        except SFTPError as error:
            logger.error(error)
            raise error
        finally:
            logger.info(f'{hostname}: Uploaded {file} to {remote_path}')
            self.sftp.close()
            return upload

    @logger.catch
    def upload_file(self, hostname, file, remote_path, pause=0):
        """Upload a single file to a remote directory."""
        upload = None
        self.sftp = self.__connect().open_sftp()
        try:
            self.sftp.put(file, remote_path)
            time.sleep(pause)
            upload = file
            self.sftp.close()
        except SFTPError as error:
            logger.error(error)
            raise error
        finally:
            logger.info(f'{hostname}: Uploaded {file} to {remote_path}')
            self.sftp.close()
            return upload

    @logger.catch
    def download_file(self, hostname, remote_path, local_path, pause=0):
        """Download file from remote host."""
        download = None
        self.sftp = self.__connect().open_sftp()
        try:
            self.sftp.get(remote_path, local_path)
            time.sleep(pause)
            download = local_path
            self.sftp.close()
        except SFTPError as error:
            logger.error(error)
            raise error
        finally:
            logger.info(f'{hostname}: Downloaded {local_path} from {remote_path}')
            self.sftp.close()
            return download

    @logger.catch
    def execute_commands(self, commands):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        :type commands: List[str]
        """
        self.conn = self.__connect()
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
        self.conn = self.__connect()
        self.channel = self.conn.invoke_shell()
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
