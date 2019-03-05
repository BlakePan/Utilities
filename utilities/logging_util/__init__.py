import configparser
import os


# loading config
config = configparser.ConfigParser()
config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ini/config_example.ini'))
config.read([config_file])
