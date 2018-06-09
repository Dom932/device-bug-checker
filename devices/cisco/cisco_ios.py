from devices.cisco import BaseCisco


class CiscoIOS(BaseCisco):
    """
    Class to represent Cisco IOS device
    """

    def __init__(self, **kwargs):
        super(CiscoIOS, self).__init__(**kwargs)

    @property
    def device_type(self):
        """
        Returns device type
        :param self:
        :return tuple:
        """
        return 'cisco_ios',

    def _get_version_regex(self):
        """
        Returns the regular expression string required for the version property to determine the Cisco IOS version from
        a show version output
        :return: Regular expression string
        """
        return r"Cisco IOS Software, .* Version ?(.*)"
