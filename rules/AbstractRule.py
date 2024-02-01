import json
import logging.config
import re

from pysnmp.smi import rfc1902

import SNMPConfig


class AbstractRule:

    def __init__(self, msg_json, var_binds, mib_modules):
        super().__init__()
        self.debug = False
        self.msgJson = msg_json
        self.values = json.loads(self.msgJson)
        self.var_binds = self.values['varBinds']
        self.varBinds = var_binds
        self.mibModules = mib_modules
        self.set_var_binds()

    def set_var_binds(self):
        try:
            varbinary_dict = {}
            for varBind in self.varBinds:
                varbinary_dict.update([rfc1902.ObjectType(rfc1902.ObjectIdentity(varBind[0]),
                                                          varBind[1]).resolveWithMib(
                    self.mibModules.controller).prettyPrint().split(' = ')])
            self.var_binds = varbinary_dict
        except Exception as e:
            logging.error(e, exc_info=True)

    def get_var_bind(self, key):
        if key in self.var_binds:
            tv = TrapValue(self.var_binds[key])
            return tv
        else:
            logging.error("No key [%s] found for varBind", key)
        return "None"

    def set_debug(self, debug):
        self.debug = debug

    def print_debug(self, msg):
        if self.debug:
            logging.debug(msg)

    def pretty_print(self):
        logging.debug(self.msgJson)
        logging.debug(str(self.var_binds))


class TrapValue:
    def __init__(self, text):
        self.value = text

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def match(self, regular):
        tmp = re.search(regular, self.value)
        if tmp:
            return tmp.group()
        return self.value

    def severity(self):
        for k, v in SNMPConfig.lookup_severity.items():
            if self.value in v:
                return k

        return self.value
