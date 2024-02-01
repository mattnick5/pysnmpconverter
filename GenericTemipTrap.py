from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi import CommunityData, UdpTransportTarget, ContextData, sendNotification
from pysnmp.proto.rfc1902 import OctetString
from pysnmp.smi.rfc1902 import NotificationType, ObjectIdentity
import logging.config

from SNMPConfig import SNMPConfig

_FILE_CONFIG = '/opt/PySNMPConverter/conf/properties.yml'
GENERIC_OID = ".1.3.6.1.4.1.123456.3.0.1"
v_alarmtrap = '.1.3.6.1.4.1.123456.3.0.1'
v_alarmnumb = ".1.3.6.1.4.1.123456.1.1.1.1"
v_severidad = ".1.3.6.1.4.1.123456.1.1.1.2"
v_alarmtext = ".1.3.6.1.4.1.123456.1.1.1.3"
v_alarmtype = ".1.3.6.1.4.1.123456.2.1.1.1"
v_objeto = ".1.3.6.1.4.1.123456.2.1.1.2"
v_resourceoid = ".1.3.6.1.4.1.123456.1.1.1.4"


class GenericTemipTrap:
    def __init__(self):
        config = SNMPConfig(_FILE_CONFIG)
        self.server = config.get_target_host
        self.port = config.get_target_port

    def send(self, data) -> bool:

        logging.info('Send message: [%s:%s] OID: %s VarBinds: %s', self.server, self.port, v_alarmtrap, data)
        try:
            iterator = sendNotification(
                SnmpEngine(),
                CommunityData('public'),
                UdpTransportTarget((self.server, self.port)),
                ContextData(),
                'trap',
                NotificationType(
                    ObjectIdentity(GENERIC_OID)
                ).addVarBinds(
                     ('1.3.6.1.6.3.1.1.4.1.0', GENERIC_OID),
                    #(v_alarmtrap, GENERIC_OID),
                    (v_alarmnumb, OctetString(str(data['v_alarmnumb']))),
                    (v_severidad, OctetString(str(data['v_severidad']))),
                    (v_alarmtext, OctetString(str(data['v_alarmtext']))),
                    (v_alarmtype, OctetString(str(data['v_alarmtype']))),
                    (v_objeto, OctetString(str(data['v_objeto']))),
                    (v_resourceoid, OctetString(str(data['v_resourceoid'])))
                ).loadMibs(
                    'SNMPv2-MIB'
                )
            )

            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

            if errorIndication:
                logging.error(errorIndication)
                return False

        except Exception as e:
            logging.error(e, exc_info=True)
            return False

        return True
