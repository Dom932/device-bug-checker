from devices.cisco import CiscoIOS


class CiscoIOSSSHTelnet(CiscoIOS):
    """
    Class to represent Cisco IOS device to connect via ssh or telnet if unsure what connection is required
    """

    def __init__(self, **kwargs):
        super(CiscoIOS, self).__init__(**kwargs)

    @property
    def device_type(self):
        """
        Returns device type - IOS SSH first then IOS telnet
        :param self:
        :return tuple:
        """
        return 'cisco_ios', 'cisco_ios_telnet'
