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
        :return list:
        """
        return "autodetect"

    def set_version(self):
        """
        Set object version attribute by connecting to device and querying it
        :return:
        """
        self.version = 'unknown'

    def set_hostname(self):
        """
        set object hostname attribute by conneng to the device and querting it
        :return: str
        """
        reqs_disconnect = False

        if not self.connection:
            self.connect()
            reqs_disconnect = True

        hostname = self.connection.find_prompt()
        self.hostname = hostname[0:(len(hostname) - 1)]

        if reqs_disconnect:
            self.disconnect()
