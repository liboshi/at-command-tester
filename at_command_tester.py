# ===========================================================
# File: at_command_tester.py -- AT Command Automation tester
# Author:
# Date:
# Usage:
# ===========================================================

import unittest, serial, time, \
       sys, time, re
import xml.dom.minidom

if sys.version_info >= (3, 0):
    def data(at_command):
        return bytes(at_command + '\r', 'latin1')

    def to_string(byte_data):
        return str(byte_data, 'latin1')
else:
    def data(at_command): return at_command + '\r'

    def to_string(byte_data): return byte_data

class ATCommand(object):
    def __init__(self, port = None, baudrate = 460800, timeout = 45):
        try:
            self.ser = serial.Serial(int(port) - 1, int(baudrate))
        except serial.serialutil.SerialException as error:
            print(error)
    
    def send_at_command(self, at_command, at_resp):
        print('>>> Start test AT Command: %s' % at_command)
        at_command_byte = data(at_command)
        self.ser.write(at_command_byte)
        time.sleep(5)
        #if at_resp != 'None':
        return self.check_return_status(at_resp)
      
    def check_return_status(self, result):
        #ATCommand.ser.readline()
        #ret = ATCommand.ser.readline()
        size  = self.ser.inWaiting()
        ret_lst = []
        for item in to_string(self.ser.read(size)).strip().split('\n'):
            ret_lst.append(re.sub('\s+', '', item))
        ret_info = '\n'.join(ret_lst[1: -1])
        print(ret_info)
        ret_status = ret_lst[-1]
        print(ret_status)
        if result in ret_status:
            return True
        else:
            return False

    def close_ser_connect(self):
        self.ser.close()

class ParseXML(object):
    def __init__(self, path):
        self.path = path
        self.test_scripts = []

    def parse_xml(self):
        dom_tree = xml.dom.minidom.parse(self.path)
        root = dom_tree.documentElement
        test_scripts = root.getElementsByTagName('testscript')
        try:
            i = 1
            script = []
            for test_script in test_scripts:
                commands = test_script.getElementsByTagName('command')
                for command in commands:
                    phone_id= command.getAttribute('name')
                    cmd_node = command.getElementsByTagName('cmd')[0]
                    resp_node = command.getElementsByTagName('resp')[0]
                    cmd = cmd_node.childNodes[0].data
                    resp = resp_node.childNodes[0].data
                    script.append({phone_id: (cmd, resp)})
                self.test_scripts.append(script)
                script = []
                i = i + 1
            print(self.test_scripts)
        except IndexError as e:
            print(e)
            print('>>> Please check %s file...' % self.path)
            sys.exit()
        if self.test_scripts:
            return self.test_scripts
        else:
            print('>>> Please check %s file...' % self.path)
