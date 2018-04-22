from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
import sys
import fusion
import time
import os
import codecs
import re
import sys

api = fusion.api_access()


'''
Step 1: Close Marionette Port after detected EFI stage
Step 2: Re-config COM port in order to use Serial
Step 3: Send serial command to run memtest
Step 4: System reboot
Step 5: Pull serial log and search for pass string
'''


def run_memtest():
    _result = "Failed"
    _state = api.marionette.get_connected_os()
    if _state == 'EFI':
        api.marionette.execute_command("exitmarionette",1)
    elif _state == 'DISCONNECTED':
        print('System already disconnected from Marionette.')
    else:
        print('***Unknown state***')
    print('Configuring COM Port')
    api.serial_port.configure_then_listen_on_serial_port(9, 'BR_115200','DB_8','NO_PARITY','ONE','NONE')
    api.serial_port.send_data_bytes(9, [0xd])
    api.serial_port.send_data_bytes(9, [0xd])
    api.serial_port.flush_buffer(9)
    print('Deleting previous Memtest log')
    api.serial_port.send_data_string(9,'del fs0:\MemTest86.log')
    api.serial_port.send_data_bytes(9, [0xd])
    time.sleep(2)
    print('Executing memtest86 with command "fs0:\BOOTX64.efi"')
    api.serial_port.send_data_string(9,'fs0:\BOOTX64.efi') #command to run memtest
    api.serial_port.send_data_bytes(9, [0xd]) #enter keys
    '''
    Now check if the memtest completed and returned back to EFI
    '''
    _stateFlag = False
    while _stateFlag == False:
        _stateNow = api.marionette.get_connected_os()
        if _stateNow == 'EFI':
            _stateFlag = True
        else:
            pass
    print("System back to EFI state, perform pass string search.")

    regex_pattern = 'Pass(.*?)100\%'
    _fail_pattern = re.compile(r'Errors:(.*)\s{4}1')
    _serialOutput = os.path.join(api.test_iteration.LogDirectory, r'SerialBusLog.csv')
    with open(_serialOutput,'r') as _file:
        _file.seek(0)
        for _line in _file:
            _match = _fail_pattern.search(regex_pattern)
            if _match is not None:
                print('Pass string found, printing line output: ')
                print(_line)
                print(_match.group())
                _result = 'Passed'
                break
            else:
                _result = 'Failed'
    return _result


