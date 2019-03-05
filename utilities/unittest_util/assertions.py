# -*- coding: utf-8 -*-
import subprocess


def assert_keyword_NOT_in_log(keyword: str, log_fpath: str):
    """
    Check if a keyword is in a log file or not.

    :param keyword: target keyword
    :param log_fpath: path to log file to check
    :return: no return, raise assertion fail if a keyword contains in the log file
    """

    with subprocess.Popen('grep -H {} {}'.format(keyword, log_fpath), shell=True, stdout=subprocess.PIPE) as cmd:
        stdout_list = []
        for line in cmd.stdout:
            stdout_list.append(line.decode('utf-8'))
        assert stdout_list == [], '{}'.format(stdout_list)
