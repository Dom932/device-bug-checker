from bugs.base_bug import BaseBug


class TestBug(BaseBug):
    """
    This is a simple test bug to test bug check functionality on a device.

    This bug check will always report the device as affected

    Notes:
        Please review and understand the code before running it on any device.
        This bug check is provided "as is" and is to be used at your own risk.

    """

    @staticmethod
    def bug_description():
        """
        Get information regarding the bug
        :return: str - Description of bug
        """
        desc = "Simple Test Bug"
        return desc

    @staticmethod
    def bug_reference():
        """
        Get reference of bug information
        :return: str - URL to the source information
        """
        return None

    @staticmethod
    def manufacture_bug_id():
        """
        Returns the cisco Bug ID this class checks for
        :return: str - Bug ID
        """
        return "TestBug"

    @staticmethod
    def cve_id():
        """
        Get the Common Vulnerabilities and Exposure (CVE) ID
        :return: CSV ID or None if there is not one
        """
        return None

    @staticmethod
    def bug_severity():
        """
        Get the severity of the bug, based on manufacture scoring.
        Critical, Warning, Error, Informational, Minimal
        :return: The bug severity
        """
        return "Informational"

    @staticmethod
    def connection_requirements():
        """
        Connection requirements for this bug check to check the bug. These will be passed as kwargs to to
        bug checker function.
        :return:
        """
        return ["connection"]

    @staticmethod
    def device_type_requirements():
        """
        Get the device type which this bug can be checked against
        :return: tuple of device types
        """
        return 'linux',

    @staticmethod
    def manufacture():
        """
        Returns which manufacture this device bug affects
        :return: str
        """
        return None

    @staticmethod
    def enable_mode_required():
        """
        Returns if enable mode is required for the bug check
        :return: bool
        """
        return False

    @staticmethod
    def affected_devices():
        """
        Return list devices types which are affected by this put
        ["Switch","Router","Firewall","AP"]
        :return: list
        """
        return ["Switch","Router","Firewall","AP"]

    @staticmethod
    def remediate_implemented():
        """
        Check if remediate function implemented
        :return: bool
        """
        return False

    def check_bug(self, connection, **kwargs):
        """
        Checks if device if the bug is present
        :param connection: connection to device
        :type connection: netmiko.ConnectHandler

        :return: namedtuple - Bug(impacted(bool) output(str))
        """

        output = connection.send_command("Unknown cmd")
        return self.Bug(True, output)

    def remediate_bug(self):
        """
        Method to remediate bug.

        Current not implemented

        :raises NotImplemented

        """
        # TODO - implement remediate_bug
        raise NotImplemented("Remediate not implemented")
