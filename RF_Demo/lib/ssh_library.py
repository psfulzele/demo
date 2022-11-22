import os
import paramiko
import socket
import logging
from scp import SCPClient


class ssh_library:
    """
    This class contains methods to perform various remote operations over SSH.
    """
    ROBOT_LIBRARY_SCOPE = 'TESTCASE'

    def __init__(self, name):
        self._current_ssh_client = None
        self.ssh_client = None
        self.hostname = None
        self.name = name

    def create_ssh_connection(self, host, user, password):
        """
        Method to create a SSH client session and return the SSH client object.
        This method uses device hostname, device username and device password to create the SSH client session.
        :param host: Device hostname with which we want to create the SSH connection.
                     This could be the name of host or an IP address.
        :param user: User which will be used for authentication for creating the SSH connection.
        :param password: Password which will be used for authentication for creating the SSH connection.
        :return: ssh_client
        """
        try:
            self.hostname = host
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            logging.info(F"Opening a SSH connection with host: {host}")
            self.ssh_client.connect(hostname=host, username=user, password=password)
            logging.info(F"SSH connection created with host: {host}")
            return self.ssh_client
        except paramiko.AuthenticationException:
            logging.error("Authentication failed, please verify your credentials.")
        except paramiko.BadHostKeyException as badHostKeyException:
            logging.error(F"Device host key could not be verified: {badHostKeyException}")
        except paramiko.SSHException as sshException:
            logging.error(F"Could not create the SSH connection: {sshException}")

    def close_ssh_connection(self):
        """
        Method to close the SSH client session. This method will check if the client session is active.
        If it is active, then it will close that client session else it will not do anything.
        :return:
        """
        if self.ssh_client.get_transport() is not None:
            if self.ssh_client.get_transport().is_active():
                logging.info(F"Disconnecting SSH connection with host: {self.hostname}")
                self.ssh_client.close()
        else:
            logging.info("SSH connection was disconnected already")

    def execute_command(self, command, timeout=60):
        """
        Method to execute the commands over SSH connection.
        :param command: Command that needs to executed.
        :param timeout: integer in minutes
        :return: str (command_output)
        """
        try:
            logging.info(F"Executing command: {command}")
            stdin, stdout, stderr = self.ssh_client.exec_command(command=command, timeout=timeout)
            rc = stdout.channel.recv_exit_status()
            if rc == 0:
                output = stdout.read().decode(encoding='UTF-8').strip("\n")
            else:
                output = stderr.read().decode(encoding='UTF-8').strip("\n")
            return rc, output
        except socket.timeout as e:
            logging.info(str(e))
            return None, None
        except paramiko.SSHException:
            logging.error(F"Failed to execute the command: {command}")
            return None, None

    def file_or_directory_exists(self, path):
        """
        Method to check if the file or directory exists.
        It uses paramiko's SFTP client to check the existence of the directory.
        :param path: Absolute file/directory path.
        :return: boolean (True/False)
        """
        sftp = self._current_ssh_client.open_sftp()
        try:
            sftp.stat(path)
            logging.info(F"File or Directory exists: {path}")
            return True
        except IOError:
            logging.warning(F"File or Directory does not exist: {path}")
            return False

    def set_file_or_directory_permission(self, path, mode):
        """
        Method to set/change the file or directory permission.
        This method accepts the Octal notation for changing the file permissions.
        :param path: Absolute file or directory path.
        :param mode: Octal notation (for example: 600, 644, 700, 750, etc.)
        :return:
        """
        sftp = self._current_ssh_client.open_sftp()
        if self.file_or_directory_exists(path):
            sftp.chmod(path, mode)
            logging.info(F"Permission {str(mode)} set for file or directory: {path}")
            return True
        else:
            logging.error(
                F"Error occurred while setting permission {str(mode)} for file or directory: {path}")
            return False

    def list_directory(self, directory_path):
        """
        Method to list all files under the give directory path.
        :param directory_path: Directory path.
        :return: list (files_list)
        """
        sftp = self._current_ssh_client.open_sftp()
        if self.file_or_directory_exists(directory_path):
            files_list = sftp.list_folder(directory_path)
        else:
            logging.info("File or Directory does not exist, hence returning an empty list")
            files_list = []
        return files_list

    def remove_file(self, file_name, file_path):
        """
        Method to delete the file from the remote machine using SSH connection.
        Use the method file_or_directory_exists() to check if the file got deleted or not.
        :param file_name: Name of the file to be deleted.
        :param file_path: File path where the path is present.
        :return:
        """
        complete_path = F"{file_path}/{file_name}"
        sftp = self._current_ssh_client.open_sftp()
        if self.file_or_directory_exists(complete_path):
            try:
                sftp.remove(complete_path)
            except IOError as e:
                logging.error(F"Failed to remove the file {complete_path}, {e}")

    def scp_files_to_remote_machine(self, local_path, local_file_name, remote_dest_path):
        """
        This method is to scp the file from local machine to remote machine.
        :param local_path absolute path of the filel to be copied on the local machine.
        :param local_file_name file to be copied on the remote machine
        :param remote_dest_path path on the remote machine where file is to be placed
        """
        complete_path = F"{local_path}/{local_file_name}"
        try:
            with SCPClient(self._current_ssh_client.get_transport()) as scp:
                scp.put(complete_path, remote_dest_path)
                logging.info(F"File {complete_path} copied successfully to the remote machine on path {remote_dest_path}")
        except Exception as e:
            logging.error(F"Failed to scp the file from local machine to remote dest machine {complete_path}, {e}")

    def _set_active_client(self, connected_client):
        """
        Method to set this client as active client session.
        :param connected_client: Connected SSH client object.
        :return:
        """
        self._current_ssh_client = connected_client

    def copy_files(self, source_location: str, destination_location: str):
        """
        Method to copy files from source location to destination location
        :param source_location: location of source file or directory to be copied
        :param destination_location: location at which file to be copied
        :return:
        """
        try:
            if os.path.isdir(source_location):
                rc, output = self.execute_command(F"cp -pr {source_location} {destination_location}")
            else:
                rc, output = self.execute_command(F"cp {source_location} {destination_location}")
            assert rc == 0, F"Failed to copy files {source_location} to {destination_location}"
        except Exception as e:
            logging.error(F"Failed to copy file with error {e}")

    def replace_text_in_file(self, old_text: str, new_text: str, filename: str):
        """
        Method to replace text in file
        :param old_text: old_text to be replaced
        :param new_text: new_text to be put
        :param filename: file in which text to be replaced
        :return:
        """
        try:
            rc, output = self.execute_command(F"sed -i 's/{old_text}/{new_text}/g' {filename}")
            assert rc == 0, F"Failed to replace text {old_text} with {new_text}"
        except Exception as e:
            logging.error(F"Failed to replace text with error {e}")
