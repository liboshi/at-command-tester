#==================================================
# File: at_command_result.py -- AT Command result
# Author:
# Date:
# Usage:
#==================================================

import time

def logging(at_command, result):
    with open(r'./at_test.log', 'a') as fp:
        timestamp = time.ctime()
        if at_command:
            fp.write('[ %s ] AT Command: %s -- Result: %s\n' % (timestamp, at_command, result))
        else:
            fp.write('===================================== Test Result: %s =====================================\n\n' % result)
