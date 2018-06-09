from devices.base_device import BaseDevice


class AutoDetect(BaseDevice):
    """
    Class to represent a generic device. Will use netmiko autodetect to try and determine best device type
    at connection.
    """

    def __init__(self, **kwargs):
        super(AutoDetect, self).__init__(**kwargs)

    @property
    def manufacture(self):
        """
        Returns manufacture of device
        :param self:
        :return str
        """
        return "autodetect"

    @property
    def device_type(self):
        """
        Returns device type
        :param self:
        :return tuple:
        """
        return "autodetect",

    @property
    def version(self):
        """
        Get device OS Version
        :return: str
        """

        if self._version:
            return self._version
        else:
            self._version = "unknown"
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
            self.hostname = hostname[0:(len(hostname) - 1)]

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
