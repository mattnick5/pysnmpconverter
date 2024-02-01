import concurrent
import logging.config
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from MIBLoad import MIBLoad
from SNMPConfig import SNMPConfig
import SNMPThread
from SNMPThread import cth


class SNMPTrap:
    def __init__(self, conf):
        self.mib_modules = None
        self.snmpconfig = conf
        self.loadMibs()

    def loadMibs(self):
        self.mib_modules = MIBLoad(self.snmpconfig.get_engine_mibdir)

    def cbFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg):
        # logging.debug(transportAddress)
        # logging.debug(self.snmpconfig.get_engine_host)
        # with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        #    executor.submit(cth, transportAddress=transportAddress, wholeMsg=wholeMsg)
        # logging.debug(self.mibs.get_mib_controller())
        #th = Thread(target=SNMPThread.cth, args=(transportAddress, wholeMsg, self.mib_modules), daemon=True)
        #th.start()
        SNMPThread.cth(transportAddress, wholeMsg, self.mib_modules)


        return wholeMsg
