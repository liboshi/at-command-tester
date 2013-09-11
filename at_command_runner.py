#==================================================
# File: at_command_runner.py -- AT Command runner
# Author:
# Date:
# Usage:
#==================================================

'''
- AT Command Runer

- Command Line parameters:
    --main_port     -- Port for main phone
    --ref_port      -- Port for reference phone
    --baudrate      -- Baudrate for the com serial
    --at_cmd_set    -- use for load at command suite which need test
'''

import os, sys, getopt
from at_command_tester import ATCommand, ParseXML
from at_command_result import logging

AT_conf = {'main_port':    None,
           'ref_port':     None,
           'baudrate':     None,
           'at_cmd_set':   None,
          }

def usage():
    print(__doc__)

def parse_commandline():
    try:
        optlst, args = getopt.getopt(sys.argv[1:], "h", \
                                 ['help', 'main_port=', 'ref_port=', 'baudrate=', 'at_cmd_set='])
        if optlst == []:
            usage()
            sys.exit(2)

        for option, argument in optlst:
            if option in ['-h', '--help']:
                usage()
                sys.exit(2)

            if option in ['--main_port']:
                AT_conf['main_port'] = argument

            if option in ['--ref_port']:
                AT_conf['ref_port'] = argument

            if option in ['--baudrate']:
                AT_conf['baudrate'] = argument

            if option in ['--at_cmd_set']:
                assert os.path.isfile(argument), 'Invild cmd set file...'
                AT_conf['at_cmd_set'] = argument

    except getopt.GetoptError as error:
        print(error)
        usage()
        sys.exit(1)

def main():
    # parse command line
    parse_commandline()
    if AT_conf['baudrate']:
        at_command_main = ATCommand(AT_conf['main_port'], AT_conf['baudrate'])
        at_command_ref = ATCommand(AT_conf['ref_port'], AT_conf['baudrate'])
    else:
        at_command_main = ATCommand(AT_conf['main_port'])
        at_command_ref = ATCommand(AT_conf['ref_port'])
    # Parse the test scripts file -- at_cmd.xml
    xml_parse = ParseXML(AT_conf['at_cmd_set'])
    test_scripts = xml_parse.parse_xml()
    try:
        for test_script in test_scripts:
            result = True
            for script in test_script:
                for phone_id, cmd_resp in script.items():
                    if phone_id == 'Main':
                        print('>>> Main Phone: Sending...')
                        ret = at_command_main.send_at_command(cmd_resp[0], cmd_resp[1])
                        result = result and ret
                        print(ret)
                        if ret:
                            logging(cmd_resp[0], 'Pass')
                        else:
                            logging(cmd_resp[0], 'Fail')
                    elif phone_id == 'Refer':
                        print('>>> Reference Phone: Sending...')
                        ret = at_command_ref.send_at_command(cmd_resp[0], cmd_resp[1])
                        result = result and ret
                        print(ret)
                        if ret:
                            logging(cmd_resp[0], 'Pass')
                        else:
                            logging(cmd_resp[0], 'Fail')
            if result:
                logging('', 'Pass')
            else:
                logging('', 'Fail')
    except Exception as e:
        print(e)
    finally:
        at_command_main.close_ser_connect()
        at_command_ref.close_ser_connect()

#############################
# AT COMMAND RUNNER STARTUP #
#############################

if __name__ == '__main__':
    main()
