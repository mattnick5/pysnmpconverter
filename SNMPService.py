# PySNMPConverter
# Description:
# Author: Virgil Jones   - vjones@tigo.com.gt
# NOC Automation - Tigo Guatemala
# Date: December, 2023

import logging.config
import sys

import yaml
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp, udp6
from SNMPConfig import SNMPConfig
from SNMPTrap import SNMPTrap


class SNMPService:

    def __init__(self, snmpconfig):
        logging.info("init SNMPService")
        cbFun = SNMPTrap(snmpconfig)
        transportdispatcher = AsyncoreDispatcher()
        transportdispatcher.registerRecvCbFun(cbFun.cbFun)

        # UDP/IPv4
        transportdispatcher.registerTransport(
            udp.domainName,
            udp.UdpSocketTransport().openServerMode((snmpconfig.get_engine_host, snmpconfig.get_engine_port))
        )
        logging.info('transportdispatcher registered')
        # UDP/IPv6
        transportdispatcher.registerTransport(
            udp6.domainName,
            udp6.Udp6SocketTransport().openServerMode((snmpconfig.get_engine_ipv6, snmpconfig.get_engine_port))
        )

        transportdispatcher.jobStarted(1)

        try:
            logging.info("PySNMPConverter service is running")
            logging.info("Listen on %s:%s" % (snmpconfig.get_engine_host, snmpconfig.get_engine_port))
            transportdispatcher.runDispatcher()
        except Exception as error:
            logging.error(error)
        finally:
            transportdispatcher.closeDispatcher()


if __name__ == '__main__':
    _FILE_LOG = '/opt/PySNMPConverter/conf/logging.yml'
    _FILE_CONFIG = '/opt/PySNMPConverter/conf/properties.yml'
    # Loggin File
    try:
        with open(_FILE_LOG, "r") as file:
            yaml_config = yaml.safe_load(file)
            logging.config.dictConfig(yaml_config)

        #logging.config.fileConfig(_FILE_LOG)
        #logging.basicConfig(level=logging.DEBUG, filename="log/service.log", filemode="a", format="%(asctime)s %(levelname)s %(message)s")
    except Exception as e:
        print(e)
        sys.exit()

    # Config File
    try:
        config = SNMPConfig(_FILE_CONFIG)
        logging.info("File %s is load", _FILE_CONFIG)
    except Exception as e:
        logging.error(e, exc_info=True)
        logging.error("%s is not loaded", _FILE_CONFIG)
        sys.exit()

    # Main Service
    try:
        service = SNMPService(config)
        logging.info("PySNMPConverter service is starting")
    except Exception as e:
        logging.error(e)
    finally:
        logging.critical("PySNMPConverter service is down")
