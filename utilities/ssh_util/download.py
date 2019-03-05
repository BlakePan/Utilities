# -*- coding: utf-8 -*-
import os
import scp
import paramiko

ssh_server = 'ip address of server'
ssh_port = 22
ssh_user = 'user name'
ssh_key_file = 'file path of ssh key file'


def download_files_by_sftp(remote_dir: str, local_dir: str) -> int:
    """
    Download files from a given path in remote server

    :param remote_dir:
    remote path where to download files

    :param local_dir:
    local path where to save downloaded files

    :return:
    0 for success, others for error
    """
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_server, port=ssh_port, username=ssh_user, key_filename=ssh_key_file)

    sftp = ssh.open_sftp()
    remote_files = sftp.listdir(remote_dir)

    for f in remote_files:
        r_f = remote_dir + '/' + f
        l_f = local_dir + '/' + f
        sftp.get(r_f, l_f)

    sftp.close()
    ssh.close()

    return 0


def progress_callback(filename, size, sent):
    """
    Progress callback function for scp.SCPClient(progress=)

    :param filename:
    :param size:
    :param sent:
    :return:
    """
    print('{}, size: {}, sent: {}'.format(filename, size, sent), end='\r', flush=True)


def download_file_by_scp(fname, remote, local, progress=None):
    """
    Download a file from remote path to local path by scp module

    :param fname:
    :param remote:
    :param local:
    :param progress:
    :return:
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_server, port=ssh_port, username=ssh_user, key_filename=ssh_key_file)
    with scp.SCPClient(ssh.get_transport(), sanitize=lambda x: x, progress=progress) as _scp:
        _scp.get(remote_path=remote + '/' + fname, local_path=local)
    ssh.close()

    return 0


def download_dir(remote, local, progress=None):
    """
    Download a dir from remote path to local path by scp module

    :param remote:
    :param local:
    :param progress:
    :return:
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_server, port=ssh_port, username=ssh_user, key_filename=ssh_key_file)
    with scp.SCPClient(ssh.get_transport(), sanitize=lambda x: x, progress=progress) as _scp:
        _scp.get(remote_path=remote, local_path=local, recursive=True)
    ssh.close()

    return 0
