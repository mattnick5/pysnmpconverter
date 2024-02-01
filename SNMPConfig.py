import yaml

lookup_severity = None


class SNMPConfig:
    def __init__(self, config_path):
        with open(config_path) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        engine_data = config.get('Engine', {})
        target_data = config.get('Target', {})
        lookup = config.get('Lookup', {})

        self.engine_port = engine_data['port']
        self.engine_host = engine_data['host']
        self.engine_ipv6 = engine_data['ipv6']
        self.engine_mibdir = engine_data['mib_dir']

        self.target_port = target_data['port']
        self.target_host = target_data['host']

        lookup['severity']
        global lookup_severity
        lookup_severity = lookup['severity']

    @property
    def get_engine_port(self):
        return self.engine_port

    @property
    def get_engine_host(self):
        return self.engine_host

    @property
    def get_engine_ipv6(self):
        return self.engine_ipv6

    @property
    def get_engine_mibdir(self):
        return self.engine_mibdir

    @property
    def get_target_host(self):
        return self.target_host

    @property
    def get_target_port(self):
        return self.target_port
