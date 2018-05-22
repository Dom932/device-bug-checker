import re
from devices.base_device import BaseDevice


class CiscoWLC(BaseDevice):
    """
    Class to represent Cisco WLC device
    """

    def __init__(self, **kwargs):
        super(CiscoWLC, self).__init__(**kwargs)

    @property
    def manufacture(self):
        """
        Returns manufacture of device
        :param self:
        :return str
        """
        return "cisco"

    @property
    def device_type(self):
        """
        Returns device type
        :param self:
        :return lst
        """
        return "cisco_wlc"

    def set_version(self):
        """
        Set object version attribute by connecting to device and querying it
        :return:
        """
        reqs_disconnect = False

        if not self.connection:
            self.connect()
            reqs_disconnect = True

        config = self.connection.send_command("sh sysinfo")

        rexp = r"Product Version.................... ?(.*)"
        output = re.search(rexp, config)

        if output:
            self.version = output.group(1)
        else:
            self.version = "Unable to determine IOS version"

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

        hostname = self.connection.find_prompt()
        self.hostname = hostname[0:(len(hostname) - 1)]

        if reqs_disconnect:
            self.disconnect()

