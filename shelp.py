#!/usr/bin/env python3
import argparse
import netifaces
import json
import sys
import os
import configparser

__version__ = "0.4.0"

try:
    with open(os.path.join(sys.path[0], 'shells.json'), "r") as shells_file:
        shells = json.load(shells_file)
        shell_choices = []
        for element in shells:
            shell_choices += element["lang"]
except IOError:
    print("There was no json file for shells found")
    sys.exit(1)

# parsing config for default values or set them if not found
default_conf = {}
config_path = os.path.join(sys.path[0], 'config.ini')
if os.path.isfile(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    default_conf['ip'] = config['DEFAULT'].get('ip')
    default_conf['interface'] = config['DEFAULT'].get('interface')
    default_conf['port'] = config['DEFAULT'].getint('port')
    default_conf['language'] = config['DEFAULT'].get('language')
    default_conf['nonewline'] = config['DEFAULT'].getboolean('nonewline')
    default_conf['shells_path'] = config['DEFAULT'].get('shells_path')

else:
    default_conf['ip'] = '127.0.0.1'
    default_conf['interface'] = None
    default_conf['port'] = 9001
    default_conf['language'] = 'bash'
    default_conf['nonewline'] = False
    default_conf['shells_path'] = None

# Argument parsing
parser = argparse.ArgumentParser()
args_ip_group = parser.add_mutually_exclusive_group()
args_ip_group.add_argument("-i", "--interface", metavar="INTER",
                           help="Specify the interface to get your IP",
                           default=default_conf['interface'])
args_ip_group.add_argument("-a", "--ip", help="Specify your IP",
                           default=default_conf['ip'])
parser.add_argument("-p", "--port", help="Specify your port", type=int,
                    default=default_conf['port'])
parser.add_argument("-l", "--language", metavar="LANG",
                    help="""Specify the language you want your shell in.
                     available languages: %(choices)s""",
                    default=default_conf['language'], choices=shell_choices)
parser.add_argument("--shells_path",
                    help="Path to alternative json file with shell_codes.",
                    default=default_conf['shells_path'])
parser.add_argument("--nonewline", "-n", help="Don't add newline to output.",
                    action="store_true", default=default_conf['nonewline'])

args = parser.parse_args()

if args.shells_path:  # TODO error handling for invalid path --> go to default
    shells_path = args.shells_path
else:
    shells_path = os.path.join(sys.path[0], 'shells.json')

# TODO add option to query public ip addr from router

data = {'ip': '127.0.0.1', 'port': '9999'}  # DEFAULT data for now should never be used TODO


def get_ip_from_interface(interface):
    """ return your external IP on given interface """
    inter = netifaces.ifaddresses(interface)
    try:
        ip = inter[netifaces.AF_INET][0]['addr']
    except KeyError:
        print("no IPv4 adress for {} found. Deault to IP setting.".format(interface, data['ip']))
        if args.ip:
            return args.ip
        else:
            print("No IP settings found. Default to locahost.")
            return "127.0.0.1"
    return ip


def generate_shell(data, lang):
    """generates the reverse shell code"""
    shell_code = ""
    with open(shells_path, "r") as shells_file:
        shells = json.load(shells_file)
        for element in shells:
            if lang in element["lang"]:
                shell_code = element["code"].format(d=data)
                break
    return shell_code


def main():
    """Main function"""
    # get IP
    if args.interface:
        data['ip'] = get_ip_from_interface(args.interface)
    elif args.ip:
        data['ip'] = args.ip

    # get port
    if args.port:
        data['port'] = args.port
    shell = generate_shell(data, args.language)
    if args.nonewline:
        sys.stdout.write(shell)
        sys.stdout.flush()
    else:
        print(shell)


if __name__ == '__main__':
    main()
