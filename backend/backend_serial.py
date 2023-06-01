# We use RS-485 -> COM driver to switch from RS to USB-COM
# BUK use RS-485 interfese to interact with user.
# To interact with desctop we use pyserial
# Here is code to transmit and resive messeges
import time
from . import backend_logs as logs
from . import backend_parser as parser
import serial
import serial.tools.list_ports
PORT = '/dev/ttyACM1'
BAUD = 9600
BYTE_SIZE = 8
PARITY = 'N'
STOP_BITS = 1
ATTEMPTS = 3
BUK_DEV = 'Arduino'



def avilable_com() -> str:
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if BUK_DEV in desc or "ACM" in port:
            return str(port)
    return '0'


def commands_generator(buk_num: str, command: str) -> str:
    return 'bmk:' + buk_num + ":" + command


def send_command(command:str, port:serial.Serial) -> dict[str, bool | dict[str, str]]:
    global PORT
    dict_to_write:dict[str, bool | dict[str, str]] = {}
    command_name = f'{command[8:]}'
    for _ in range(ATTEMPTS):
        try:
            if port.write(command.encode()):
                # s_t = time.time()
                print(command.encode())
                line = port.readline()
                print(line)
                # print(f"Time for read 175b :{time.time() - s_t}")
                dict_to_write[command_name] = parser.parse_com_str(line, command_name)
                if dict_to_write[command_name]:
                    logs.success_parsing_log(str(line))
                    break
                else:
                    logs.error_parsing_log(str(line))
                    continue
            else:
                logs.error_write_log(command)
                continue
        except serial.SerialException:
            dict_to_write[command_name] = {}
            raise serial.SerialException
    return dict_to_write
