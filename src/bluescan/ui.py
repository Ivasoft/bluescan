#!/usr/bin/env python3

r'''bluescan v0.0.8

Usage:
    bluescan (-h | --help)
    bluescan (-v | --version)
    bluescan [-i <hcix>] -m br [--inquiry-len=<n>]
    bluescan [-i <hcix>] -m lmp BD_ADDR
    bluescan [-i <hcix>] -m sdp BD_ADDR
    bluescan [-i <hcix>] -m le [--timeout=<sec>] [--le-scan-type=<type>] [--sort=<key>]
    bluescan [-i <hcix>] -m gatt [--include-descriptor] --addr-type=<type> BD_ADDR
    bluescan [-i <hcix>] -m vuln --addr-type=br BD_ADDR

Arguments:
    BD_ADDR    Target Bluetooth device address

Options:
    -h, --help                  Display this help
    -v, --version               Show the version
    -i <hcix>                   HCI device for scan [default: hci0]
    -m <mode>                   Scan mode, support BR, LE, LMP, SDP, GATT and vuln
    --inquiry-len=<n>           Inquiry_Length parameter of HCI_Inquiry command [default: 8]
    --timeout=<sec>             Duration of LE scan [default: 10]
    --le-scan-type=<type>       Active or passive scan for LE scan [default: active]
    --sort=<key>                Sort the discovered devices by key, only support RSSI now [default: rssi]
    --include-descriptor        Fetch descriptor information
    --addr-type=<type>          Public, random or BR
'''

green  = lambda text: '\x1B[1;32m' + text + '\x1B[0m'
blue   = lambda text: '\x1B[1;34m' + text + '\x1B[0m'
yellow = lambda text: '\x1B[1;33m' + text + '\x1B[0m'
red    = lambda text: '\x1B[1;31m' + text + '\x1B[0m'

DEBUG = '[DEBUG]'
INFO = '['+blue('INFO')+']'
WARNING = '['+yellow('WARNING')+']'
ERROR = '['+red('ERROR')+']'

from docopt import docopt
from .helper import valid_bdaddr


def parse_cmdline() -> dict:
    args = docopt(__doc__, version='v0.0.8', options_first=True)
    #print("[Debug] args =", args)

    args['-m'] = args['-m'].lower()
    args['--inquiry-len'] = int(args['--inquiry-len'])
    args['--timeout'] = int(args['--timeout'])
    args['--le-scan-type'] = args['--le-scan-type'].lower()
    args['--sort'] = args['--sort'].lower()

    try:
        if args['-m'] == 'gatt' or args['-m'] == 'sdp':
            if args['BD_ADDR'] is None:
                raise ValueError(ERROR + 'Need BD_ADDR')
            else:
                args['BD_ADDR'] = args['BD_ADDR'].lower()
                if not valid_bdaddr(args['BD_ADDR']):
                    raise ValueError(
                        ERROR + 'Invalid BD_ADDR: ' + args['BD_ADDR']
                    )

        if args['-m'] == 'gatt':
            if args['--addr-type'] != 'public' and \
               args['--addr-type'] != 'random':
                raise ValueError(
                    ERROR + 'Invalid --addr-type, must be public or random'
                )
            args['--addr-type'] = args['--addr-type'].lower()
    except ValueError as e:
        print(e)
        exit(1)
        
    return args


def __test():
    pass


if __name__ == "__main__":
    __test()
