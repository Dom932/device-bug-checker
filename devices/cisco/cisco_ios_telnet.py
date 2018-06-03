from devices.cisco import CiscoIOS


class CiscoIOSTelnet(CiscoIOS):
    """
    Class to represent Cisco IOS device
    """

    def __init__(self, **kwargs):
        super(CiscoIOSTelnet, self).__init__(**kwargs)

    @property
    def device_type(self):
        """
        Returns device type
        :param self:
        :return list:
        """
        return 'cisco_ios_telnet'
