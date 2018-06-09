from devices.base_device import BaseDevice


class Linux(BaseDevice):
    """
    Class to represent linux
    """

    def __init__(self, **kwargs):
        super(Linux, self).__init__(**kwargs)

    @property
    def manufacture(self):
        """
        Returns manufacture of device
        :param self:
        :return str
        """
        return "linux"

    @property
    def device_type(self):
        """
        Returns device type
        :param self:
        :return tuple:
        """
        return "linux",

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

            self._version = self.connection.send_command("uname -r")

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

            self.hostname = self.connection.send_command("hostname")

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
