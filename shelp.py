#!/usr/bin/env python3
import argparse

# TODO have default values for arguments [read from a .conf file]
# TODO import reverseshell format strings from a shell.json file 
parser = argparse.ArgumentParser()
args_ip_group = parser.add_mutually_exclusive_group()
args_ip_group.add_argument("-i", "--interface", help="Specify the interface to get your IP")
args_ip_group.add_argument("-a", "--ip", help="Specify your IP")
parser.add_argument("port", help="Specify your port")
parser.add_argument("-l", "--language", help="Specify the language you want your shell in.", default="bash")
args = parser.parse_args()

print(args)

def get_ip_from_interface(interface):
    """ return your external IP on given interface """
    # TODO implement this
    return "127.0.0.1"

def generate_shell(ip, port, lang):
    """generates the reverse shell code"""
    # TODO implement this
    return "NOT IMPLEMENTED YET"

def main():
    """Main function"""
    if args.interface:
        ip = get_ip_from_interface(args.interface)
    else:
        ip = args.ip
    shell = generate_shell(ip, args.port, args.language)
    print(shell)  # TODO is print the best option? encoding?


if __name__ == '__main__':
    main()
