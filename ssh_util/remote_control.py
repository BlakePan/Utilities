import time
import paramiko


ssh_server = 'ip address to server'
ssh_port = 22
ssh_user = 'user name'
ssh_key_file = 'file path to ssh key file'


def make_dir_in_remote(remote_path: str, target_dir_name: str)->int:
    """
    Build a folder in remote though ssh connection
    
    :param remote_path:
    a path in remote server

    :param target_dir_name:
    a name for a dir to build

    :return:
    0 for success, others for error
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_server, port=ssh_port, username=ssh_user, key_filename=ssh_key_file)
    _, ssh_stdout, _ = ssh.exec_command('ls {}'.format(remote_path + '/'))
    time.sleep(1)  # a delay for ssh command response

    result = ssh_stdout.readlines()
    if target_dir_name + '\n' not in result:
        ssh.exec_command('mkdir {}'.format(remote_path + '/' + target_dir_name))
        time.sleep(10)  # a delay for ssh command response
    ssh.close()

    return 0


def make_file_in_remote(remote_dir: str, target_file: str,
                        mode: str = 'create', remote_copy_dir: str = None)->int:
    """
    1. Create a file in remote though ssh connection
    2. Copy a file from remote_copy_dir to remote_dir

    :param remote_dir:
    a path in remote server

    :param target_file:
    a name for a file to be created or copied

    :param mode:
    'create' or 'copy'

    :param remote_copy_dir:
    a path which target file exists in remote server

    :return:
    0 for success, others for error
    """
    assert mode == 'copy' or mode == 'create'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_server, port=ssh_port, username=ssh_user, key_filename=ssh_key_file)
    _, ssh_stdout, _ = ssh.exec_command('ls {}'.format(remote_dir + '/'))
    time.sleep(1)  # a delay for ssh command response

    result = ssh_stdout.readlines()
    if target_file + '\n' not in result:
        if mode == 'copy':
            assert remote_copy_dir is not None
            ssh.exec_command('cp {} {}'.format(remote_copy_dir + '/' + target_file,
                                               remote_dir + '/' + target_file))
        elif mode == 'create':
            ssh.exec_command('touch {}'.format(remote_dir + '/' + target_file))
        time.sleep(10)  # a delay for ssh command response

    ssh.close()

    return 0
