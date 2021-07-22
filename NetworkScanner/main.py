#!/usr/bin/python3

import netifaces
import nmap
import logging

def get_list():
    '''Get network devices addresses'''
    logging.info('# get_list()')
    base = '192.168.0.0/24'
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=base, arguments='-n -sP -PE -PA21,23,80,3389')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        for host, status in hosts_list:
            logging.info('{}'.format(host))
    except nmap.PortScannerError as error:
        logging.error('Nmap scan fail')

def get_ip():
    '''Gets host ip'''
    logging.info('# get_ip()')
    ip = 'N/A'
    try:
        host_name = netifaces.gateways()
        ip = host_name['default'][2][0]
        logging.info('Current IP: {}'.format(ip))
    except KeyError as error:
        logging.error('Key error found')
    except IndexError as error:
        logging.error('Index error')
    return ip


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting program")
    ip = get_ip()
    get_list()