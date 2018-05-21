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
        :return lst
        """
        return "linux"

    def set_version(self):
        """
        Set object version attribute by connecting to device and querying it
        :return:
        """

        reqs_disconnect = False

        if not self.connection:
            self.connect()
            reqs_disconnect = True

        self.version = self.connection.send_command("uname -r")

        if reqs_disconnect:
            self.disconnect()

    def set_hostname(self):
        """
        set object hostname attribute by conneng to the device and querting it
        :return: str
        """

        reqs_disconnect = False

        if not self.connection:
            self.connect()
            reqs_disconnect = True

        self.hostname = self.connection.send_command("hostname")

        if reqs_disconnect:
            self.disconnect()