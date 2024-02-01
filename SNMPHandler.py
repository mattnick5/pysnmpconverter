# PySNMPConverter
# Description:
# Author: Virgil Jones   - vjones@tigo.com.gt
# NOC Automation - Tigo Guatemala
# Date: December, 2023
from abc import abstractmethod
import logging.config


class SNMPEngine:
    @abstractmethod
    def trap_receiver(self):
        pass

    @abstractmethod
    def trap_handler(self):
        var_binds = dict()
        return var_binds

    @abstractmethod
    def log_handler(self):
        logging.config.fileConfig('logging_config.ini')

