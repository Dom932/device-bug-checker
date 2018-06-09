import re
from devices.cisco import BaseCisco


class CiscoWLC(BaseCisco):
    """
    Class to represent Cisco WLC device
    """

    def __init__(self, **kwargs):
        super(CiscoWLC, self).__init__(**kwargs)

    @property
    def device_type(self):
        """
        Returns device type
        :param self:
        :return tuple:
        """
        return 'cisco_wlc',

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

            config = self.connection.send_command("sh sysinfo")

            output = re.search(self._get_version_regex(), config)

            if output:
                self._version = output.group(1)
            else:
                self._version = "Unable to determine IOS version"

            if reqs_disconnect:
                self.disconnect()

            return self._version

    def _get_version_regex(self):
        """
        Returns the regular expression string required for the version property to determine the Cisco IOS version from
        a show version output
        :return: Regular expression string
        """
        return r"Product Version.................................. ?(.*)"
