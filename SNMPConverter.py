import logging.config
import importlib

from rules.FMS import FMS
from rules.NQMS import NQMS
from rules.Pnmsj import Pnmsj
from rules.Opennms import Opennms
from rules.Wavenet import Wavenet



def cbFunConverter(enterprise, varBinds, mibModules, data_json):

    if enterprise.startswith("1.3.6.1.4.1.119"):
        # pnmsj = Pnmsj(data_json, varBinds, mibModules)
        # pnmsj.start()
        module = importlib.import_module("rules.Pnmsj")
        my_class = getattr(module, "Pnmsj")
        instance = my_class(data_json, varBinds, mibModules)
        instance.start()
    elif enterprise.startswith("1.3.6.1.4.1.6718.3.2.1"):
         fms = FMS(data_json, varBinds, mibModules)
         fms.start()
    elif enterprise.startswith("1.3.6.1.4.1.6718.3.2.2"):
         nqms = NQMS(data_json, varBinds, mibModules)
         nqms.start()
    elif enterprise.startswith("1.3.6.1.4.1.5813"):
        opennms = Opennms(data_json, varBinds, mibModules)
        opennms.start()
    elif enterprise.startswith("1.3.6.1.4.1.9817"):
        wavenet = Wavenet(data_json, varBinds, mibModules)
        wavenet.start()
    else:
        logging.critical("OID not set %s", enterprise, stack_info=False)
