#!/usr/bin/env python3
import argparse
import netifaces
import json
import sys
import os

<<<<<<< HEAD
__version__ = "0.3.4"

# TODO have default values for arguments [read from a .conf file]

=======
__version__ = "0.3.3"

# TODO have default values for arguments [read from a .conf file]

# TODO make error handling for file not found
>>>>>>> 6c61a1d45bf1c2fd7af661fe72946ded9a893c88
try:
    with open(os.path.join(sys.path[0], 'shells.json'), "r") as shells_file:
        shells = json.load(shells_file)
        shell_choices = []
        for element in shells:
            shell_choices += element["lang"]
except IOError:
    print("There was no json file for shells found")
    sys.exit(1)

# Argument parsing
parser = argparse.ArgumentParser()
args_ip_group = parser.add_mutually_exclusive_group()
args_ip_group.add_argument("-i", "--interface", metavar="INTER",
                           help="Specify the interface to get your IP")
args_ip_group.add_argument("-a", "--ip", help="Specify your IP")
parser.add_argument("-p", "--port", help="Specify your port", type=int)
parser.add_argument("-l", "--language", metavar="LANG",
                    help="""Specify the language you want your shell in.
                     available languages: %(choices)s""",
                    default="bash", choices=shell_choices)
parser.add_argument("--shells_path",
                    help="Path to alternative json file with shell_codes.")
parser.add_argument("--nonewline", "-n", help="Don't add newline to output.",
                    action="store_true")

args = parser.parse_args()

if args.shells_path:
    shells_path = args.shells_path
else:
    shells_path = os.path.join(sys.path[0], 'shells.json')

# TODO add option to query public ip addr from router

data = {'ip': '127.0.0.1', 'port': '9999'}  # DEFAULT data for now TODO


def get_ip_from_interface(interface):
    """ return your external IP on given interface """
    inter = netifaces.ifaddresses(interface)
    try:
        ip = inter[netifaces.AF_INET][0]['addr']
    except KeyError:
        # TODO make this an error
        print("no IPv4 adress for {} found. Deault to localhost.".format(interface))
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
