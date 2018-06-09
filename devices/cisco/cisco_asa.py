from devices.cisco import BaseCisco


class CiscoASA(BaseCisco):
    """
    Class to represent Cisco ASA device
    """

    @property
    def device_type(self):
        """
        Returns device type
        :param self:
        :return tuple:
        """
        return 'cisco_asa',

    def _get_version_regex(self):
        """
        Returns the regular expression string required for the version property to determine the Cisco IOS version from
        a show version output
        :return: Regular expression string
        """
        return r"Cisco Adaptive Security Appliance Software Version ?(.*)"
