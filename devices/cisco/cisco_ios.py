import re
from devices.base_device import BaseDevice
from helpers import DeviceHelper

class CiscoIOS(BaseDevice):
    """
    Class to represent Cisco IOS device
    """

    def __init__(self, **kwargs):
        super(CiscoIOS, self).__init__(**kwargs)

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
        return 'cisco_ios'

    def set_version(self):
        """
        Set object version attribute by connecting to device and querying it
        :return:
        """

        reqs_disconnect = False

        if not self.connection:
            self.connect()
            reqs_disconnect = True


        config = self.connection.send_command("sh ver")

        rexp = r"Cisco IOS Software, .* Version ?(.*)"
        output = re.search(rexp, config)

        if output:
            self.version = output.group(1)
        else:
            self.version =  "Unable to determine IOS version"

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
