from bugs.base_bug import BaseBug


class CSCvg76186(BaseBug):
    """
    TODO
    """

    @property
    def enable_mode_required(self):
        """
        Returns if enable mode is required for the bug check
        :return: bool
        """
        return False

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
        return "CSCvg76186"

    @property
    def affected_devices(self):
        """
        Return list devices types which are affected by this put
        ["Switch","Router","Firewall","AP"]
        :return: list
        """
        return ["Switch"]

    @property
    def remediate_implimented(self):
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
        Checks if device if the bug is present
        :param connection: connection to device
        :type connection: netmiko.ConnectHandler

        :return: namedtuple - Bug(impacted(bool) output(str))
        """

        vstack_output = connection.send_command("show vstack config")

        if "Invalid input detected" in vstack_output:
            return self.Bug(False, "Command not supported on platform")
        else:

            # check if vulnerable
            if "Role: Client (SmartInstall enabled)" in vstack_output:
                return self.Bug(True, vstack_output)
            elif "Oper Mode: Enabled" in vstack_output and "Role: Client" in vstack_output:
                return self.Bug(True, vstack_output)
            else:
                return self.Bug(False, vstack_output)

    def remediate_bug(self):
        """
        Method to remediate bug.

        Current not implemented
        
        :raises NotImplemented 
        
        """
        # TODO - implement remediate_bug
        raise NotImplemented("Remediate not implemented")
