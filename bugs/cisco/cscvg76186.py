from bugs.base_bug import BaseBug


class CSCvg76186(BaseBug):
    """
    CSCvg76168 Bug Check

    This bug check is intended to check a Cisco switch to determine if the Cisco Smart Install
    feature is enabled which indicates if the device is vulnerable to CSCvg76168 (CVSS Score: 9.8
    (Critical).

    Please call get_description() for nor infoamtion.

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
        desc = "Cisco Smart Install is a feature in Cisco IOS and OIS XE software that provides plug and play " \
               "configuration and image management for zero touch deployment of new equipment. \n\nA " \
               "vulnerablility in the Smar Instll feature could allow an attacker to trigger a reload of a " \
               "device or execute arbitrary code. This attack is possible due to improper validation of packet " \
               "data. In order to exploit this vulnerablity, an attacker would create a Smart Install message " \
               "to an vulnerable device on port tcp/4786, which could cause a buffer overflow. \n\nThis bug " \
               "check works by checking the output of 'show vstack config' to determin if the Smart Install " \
               "feature is enabled (which it is by default). Note this bug check does not currently check IOS " \
               "version comparison and the output is only to indicate if a device might be affected (ie a " \
               "upgraded IOS version (with the bug fix) with Smart Install enable would be marked as affected, " \
               "Please check the IOS version). \n\nCVSS Score: 9.8 (Critical)"

        return desc

    @staticmethod
    def bug_reference():
        """
        Get reference of bug information
        :return: str - URL to the source information
        """
        return "https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-20180328-smi2"

    @staticmethod
    def manufacture_bug_id():
        """
        Returns the cisco Bug ID this class checks for
        :return: str - Bug ID
        """
        return "CSCvg76186"

    @staticmethod
    def cve_id():
        """
        Get the Common Vulnerabilities and Exposure (CVE) ID
        :return: CSV ID or None if there is not one
        """
        return "CVE-2018-0171"

    @staticmethod
    def bug_severity():
        """
        Get the severity of the bug, based on manufacture scoring.
        Critical, Warning, Error, Informational, Minimal
        :return: The bug severity
        """
        return "Critical"

    @staticmethod
    def requirements():
        """
        Requirements for check_bug
        :return:
        """
        return ["connection"]

    @staticmethod
    def manufacture():
        """
        Returns which manufacture this device bug affects
        :return: str
        """
        return "Cisco"


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
        return ["Switch"]

    @staticmethod
    def remediate_implimented():
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
