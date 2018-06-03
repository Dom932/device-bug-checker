from bugs.base_bug import BaseBug


class TestBug(BaseBug):
    """
    Simple test bug, which will always return a device as affected. Used for test/debugging the project
    """

    @property
    def requirements(self):
        """
        Requirements for check_bug - connection only required
        :return:
        """

        return ["connection"]

    @property
    def bug_id(self):
        """
        Returns the cisco Bug ID this class checks for
        :return: str - Bug ID
        """
        return "TestBug"

    @property
    def affected_devices(self):
        """
        Return list devices types which are affected by this put
        ["Switch","Router","Firewall","AP"]
        :return: list
        """
        return ["Switch", "Router", "Firewall", "AP"]

    @property
    def remediate_implemented(self):
        """
        Check if remediate function implemented
        :return: bool
        """
        return False

    @property
    def manufacture(self):
        """
        Returns which manufacture this device bug affects
        :return: str
        """
        return "Cisco"

    def check_bug(self, connection, **kwargs):
        """
        Checks if device if the bug is present.

        Not this bug is will always indicate that the device is impacted by the bug.

        :param connection: connection to device
        :type connection: netmiko.ConnectHandler

        :return: namedtuple - Bug(impacted(bool) output(str))
        """

        output = connection.send_command("testcommand")

        return self.Bug(True, output)

    def remediate_bug(self):
        """
        Method to remediate bug.

        Current not implemented
        :return:
        """
        # TODO - implement remediate
        raise NotImplemented("Remediate not implemented")

    @property
    def enable_mode_required(self):
        """
        Returns if enable mode is required for the bug check
        :return: bool
        """
        return False
