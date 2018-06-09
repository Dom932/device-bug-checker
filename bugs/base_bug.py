from abc import ABC, abstractmethod
from collections import namedtuple


class BaseBug(ABC):
    """
    BaseBug class which all bugs need to inherit from
    """

    # Name tuple which is returned to indicate if a device is affected by a bug
    Bug = namedtuple("Bug", "impacted output")

    @staticmethod
    @abstractmethod
    def bug_description():
        """
        Get information regarding the bug
        :return: str - Description of bug
        """
        pass

    @staticmethod
    @abstractmethod
    def bug_reference():
        """
        Get reference of bug information
        :return: str - URL to the source information
        """
        pass

    @staticmethod
    @abstractmethod
    def manufacture_bug_id():
        """
        Returns the manufacture bug ID
        :return: str - Bug ID
        """
        pass

    @staticmethod
    @abstractmethod
    def cve_id():
        """
        Get the Common Vulnerabilities and Exposure (CVE) ID
        :return: CSV ID or None if there is not one
        """
        pass

    @staticmethod
    @abstractmethod
    def bug_severity():
        """
        Get the severity of the bug, based on manufacture scoring.
        Critical, Warning, Error, Informational, Minimal
        :return: The bug severity
        """
        pass

    @staticmethod
    @abstractmethod
    def connection_requirements():
        """
        Connection requirements for this bug check to check the bug. These will be passed as kwargs to to
        bug checker function.

        Current support values are:
            ip_address - IP address of device
            connection - netmiko.ConnectionHandler connection to the device
        :return: list of requirements
        """
        pass

    @staticmethod
    @abstractmethod
    def device_type_requirements():
        """
        Get the device type which this bug can be checked against
        :return: tuple of device types
        """
        pass

    @staticmethod
    @abstractmethod
    def manufacture():
        """
        Returns which manufacture this device bug affects
        :return: str
        """
        pass

    @staticmethod
    @abstractmethod
    def enable_mode_required():
        """
        Returns if enable mode is required for the bug check
        :return: bool
        """

    @staticmethod
    @abstractmethod
    def affected_devices():
        """
        Return list devices types which are affected by this put
        ["Switch","Router","Firewall","AP"]
        :return: list
        """
        pass

    @staticmethod
    @abstractmethod
    def remediate_implemented():
        """
        Check if remediate function implemented
        :return: bool
        """
        pass

    @abstractmethod
    def check_bug(self, **kwargs):
        """
        Abstract method to check if a device is susceptible to a bug
        :param kwargs: arguments required for check_bug
        :type kwargs:
        :return: namedtuple - Bug(impacted(bool) output(str))
        """
        pass

    @abstractmethod
    def remediate_bug(self):
        """
        Abstract method to resolve the bug. Throws NotImplemented if bug fix code is not implemented
        :return: bool if bug was remediated
        """
        pass
