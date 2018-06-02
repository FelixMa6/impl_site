#!/usr/local/bin/python3
import os
import sys
from socket import socket, AF_INET, SOCK_STREAM
from optparse import OptionParser

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-c', action='store', type='string', dest='input_file', help='config_file')
    (options, args) = parser.parse_args()
    ini_path = os.path.abspath(options.input_file)
    sendout = bytes(ini_path, encoding='utf8')
	
    #addr = sock.accept()
    #print('socket address is ', addr)
    s = socket(AF_INET, SOCK_STREAM)
    #s.connect(('10.10.0.70', 17500))
    s.connect(('felix-ThinkPad-E480', 17500))
    s.send(sendout)
    (output,status) = s.recvfrom(8192)
    output = str(output,encoding='utf8')
    if output=="":
        print('info_error pelase debug on server')
    elif output == b"No such INI File":
        print(output)
    else:
        print(output)
