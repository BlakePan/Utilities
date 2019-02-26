import os
import paramiko

ssh_server = 'ip address to server'
ssh_port = 22
ssh_user = 'user name'
ssh_key_file = 'file path to ssh key file'


def download_from_ssh_server(remote_dir: str, local_dir: str)->int:
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
