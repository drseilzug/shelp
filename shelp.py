#!/usr/bin/env python3
import argparse


parser = argparse.ArgumentParser()
args_ip_group = parser.add_mutually_exclusive_group()
args_ip_group.add_argument("-i", "--interface", help="Specify the interface to get your IP")
args_ip_group.add_argument("-a", "--ip", help="Specify your IP")
parser.add_argument("-p", "--port", help="Specify your port")
args = parser.parse_args()

print(args)
