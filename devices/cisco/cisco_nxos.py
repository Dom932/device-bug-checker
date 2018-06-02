from devices.cisco import BaseCisco

class CiscoNXOS(BaseCisco):
    """
    Class to represent Cisco NXOS device
    """

    def __init__(self, **kwargs):
        super(CiscoNXOS, self).__init__(**kwargs)

    @property
    def device_type(self):
        """
        Returns device type
        :param self:
        :return list:
        """
        return 'cisco_nxos'

    def _get_version_regex(self):
        """
        Returns the regular expression string required for the version property to determin the Cisco IOS version from
        a show version output
        :return: Regular expression string
        """
        return r"system:    version ?(.*)"
