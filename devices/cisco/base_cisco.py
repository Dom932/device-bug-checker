import re
from devices.base_device import BaseDevice
from abc import abstractmethod


class BaseCisco(BaseDevice):
    """
    Class to represent base Cisco device
    """


    def __init__(self, **kwargs):
        super(BaseCisco, self).__init__(**kwargs)

    @property
    def manufacture(self):
        """
        Returns manufacture of device
        :param self:
        :return str:
        """
        return "cisco"

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

            output = re.search(self._get_version_regex(), config)

            if output:
                self._version = output.group(1)
            else:
                self._version = "Unable to determine IOS version"

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

    @abstractmethod
    def _get_version_regex(self):
        """
        Returns the regular expression string required for the version property to determin the Cisco IOS version from
        a show version output
        :return: Regular expression string
        """
        pass
