import os
import logging.config
from pysnmp.smi import builder, view, compiler


def mib_path(path):
    files = os.listdir(path)
    result = []
    for file in files:
        if file.endswith(".py"):
            result.append(file.replace(".py", ""))
    return result


class MIBLoad(object):
    def __init__(self, path):
        self.controller = None
        self.mibBuilder = None
        self.path = path

        self.mibBuilder = builder.MibBuilder()
        self.controller = view.MibViewController(self.mibBuilder)
        compiler.addMibCompiler(self.mibBuilder, sources=['http://mibs.snmplabs.com/asn1/@mib@'])
        logging.info("---Load MIB Modules (%s)--------------------------", self.path)
        for file in mib_path(self.path):
            try:
                logging.info(file)
                self.mibBuilder.loadModules(file)
            except Exception as e:
                logging.error(e, exc_info=True)
        logging.info("------------------------------------------------------------------------")



    def get_mib_builder(self):
        return self.mibBuilder

    def get_mib_controller(self):
        return self.controller
