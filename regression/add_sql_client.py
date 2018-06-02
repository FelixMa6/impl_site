#!/cad/tools/Python-3.5.2/bin/python3
import os
import sys
from socket import socket,AF_INET,SOCK_STREAM
 
from optparse import OptionParser


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-c', action='store', type='string', dest='input_file', help='config file')
    (options, args) = parser.parse_args()
    ini_path = os.path.abspath(options.input_file)
    sendout = bytes(ini_path,encoding="utf8")


    s = socket(AF_INET,SOCK_STREAM)
    s.connect(('ct1511',17400))
    s.send(sendout)
    (output,status) = s.recvfrom(8192)
    output = str(output,encoding="utf8")
    if output=="":
        print("info_error please debug on server")
    elif output == b"No such INI File":
        print(output)
    else:
        print(output)

    