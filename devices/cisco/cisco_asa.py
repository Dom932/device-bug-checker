import re
from devices.base_device import BaseDevice
from helpers import DeviceHelper

class CiscoASA(BaseDevice):
    """
    Class to represent Cisco ASA device
    """

    def __init__(self, **kwargs):
        super(CiscoASA, self).__init__(**kwargs)

    @property
    def manufacture(self):
        """
        Returns manufacture of device
        :param self:
        :return str:
        """
        return "cisco"

    @property
    def device_type(self):
        """
        Returns device type
        :param self:
        :return list:
        """
        return 'cisco_asa'

    @property
    def version(self):
        """
        Get device OS Version
        :return: str
        """

        if self._version:
            return self._version
        else:
            reqs_disconnect = False

            if not self.connection:
                self.connect()
                reqs_disconnect = True

            config = self.connection.send_command("sh ver")

            rexp = r"Cisco Adaptive Security Appliance Software Version ?(.*)"
            output = re.search(rexp, config)

            if output:
                self._version = output.group(1)
            else:
                self._version = "Unable to determine ASA version"

            if reqs_disconnect:
                self.disconnect()

            return self._version

    @version.setter
    def version(self, version):
        """
        Set Device OS version
        :param version: OS version
        :type version: str
        :return:
        """
        self._version = version

    @property
    def hostname(self):
        """
        Get hostname set of device
        :return: str
        """
        if self._hostname:
            return self._hostname
        else:
            reqs_disconnect = False

            if not self.connection:
                self.connect()
                reqs_disconnect = True

            hostname = self.connection.find_prompt()
            self._hostname = hostname[0:(len(hostname) - 1)]

            if reqs_disconnect:
                self.disconnect()

            return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        """
        Set hostname
        :param hostname: Hostname of the device
        :type hostname: str
        :return:
        """
        self._hostname = hostname
