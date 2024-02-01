import json
import logging.config
from datetime import datetime
from pysnmp.proto import api
from pyasn1.codec.ber import decoder
from SNMPConverter import cbFunConverter


def cth(transportAddress, wholeMsg, mibModules):
    trap_json = {}
    enterprise = None
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
            trap_json.update({'version': msgVer})
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
        )

        trap_json.update({'transportAddress': transportAddress[0]})
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                trap_json.update({'enterprise': pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()})
                trap_json.update({'agentAddress': pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()})
                trap_json.update({'genericTrap': pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()})
                trap_json.update({'specificTrap': pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()})
                trap_json.update({'uptime': pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()})
                varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
                enterprise = pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
            else:
                varBinds = pMod.apiPDU.getVarBinds(reqPDU)
                # logging.debug(varBinds)

            # mibBuilder = builder.MibBuilder()
            # mibViewController = view.MibViewController(mibBuilder)
            # compiler.addMibCompiler(mibBuilder, sources=['file:///opt/PySNMPConverter/mibs/'])

            # mibBuilder.loadModules('MIB-PNMSJ-IPASOLINK-1000-COMMON-MIB', 'MIB-PNMSJ-IPASOLINK-400-COMMON-MIB',
            #                       'MIB-PNMSJ-IPASOLINK-VR10-COMMON-MIB', 'MIB-PNMSJ-IPASOLINK-100-200-COMMON-MIB',
            #                       'MIB-PNMSJ-IPASOLINK-VR4-COMMON-MIB', 'BRIDGE-MIB', 'Comviva', 'EXFO-SMI-REG',
            #                       'NQMSFIBER-MIB', 'MahindraComviva-GLOBAL-MIB', 'OPENNMS-MIB')
            #                       'NQMSFIBER-MIB', 'MahindraComviva-GLOBAL-MIB', 'OPENNMS-MIB', 'AMS-PCF-MIB')

            # try:
            # varBinds = [rfc1902.ObjectType(rfc1902.ObjectIdentity(x[0]), x[1]).resolveWithMib(mibViewController)
            #    varBinds = [
            #        rfc1902.ObjectType(rfc1902.ObjectIdentity(x[0]), x[1]).resolveWithMib(mibLoads.get_mib_controller())
            #        for x in varBinds
            #    ]
            #    logging.debug("varbinds")
            # except Exception as e:
            #    logging.error(e, exc_info=True)
            #    print(sys.exc_info())

            varbinary_dict = {}
            for varBind in varBinds:
                #logging.debug("%s = %s", varBind[0], varBind[1])
                #varbinary_dict.update([varBind.prettyPrint().split(' = ')])
                varbinary_dict.update([(str(varBind[0]), str(varBind[1]))])

            if not enterprise:
                for varBind in varBinds:
                    # logging.debug("%s = %s", varBind[0], varBind[1])
                    if str(varBind[0]) == "1.3.6.1.6.3.1.1.4.1.0":
                        if str(varBind[1]).endswith(".0"):
                            enterprise = str(varBind[1])[:-2]
                        else:
                            enterprise = str(varBind[1])
                        trap_json.update({'enterprise': ".".join(enterprise.split(".")[:-1])})
                        trap_json.update({'specificTrap': enterprise.split(".")[-1]})
                        break

            trap_json.update({'dateTime': datetime.now()})
            trap_json.update({'varBinds': varbinary_dict})

            logging.info("From: %s Version: %s OID: %s", transportAddress[0], msgVer, enterprise)

            if enterprise:
                cbFunConverter(enterprise, varBinds, mibModules, json.dumps(trap_json, indent=2, default=str))
            else:
                logging.error(trap_json)

    return wholeMsg
