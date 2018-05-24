from abc import ABC, abstractmethod
from collections import namedtuple


class BaseBug(ABC):
    """
    BaseBug class which all bugs need to inherit from
    """

    # Name tuple which is returned to indicate if a device is affected by a bug
    Bug = namedtuple("Bug", "impacted output")

    @abstractmethod
    def check_bug(self, **kwargs):
        """
        Abstract method to check if a device is susceptible to a bug
        :param kwargs: arguments required for check_bug
        :type kwargs:
        :return: namedtuple - Bug(impacted(bool) output(str))
        """
        pass

    @staticmethod
    @abstractmethod
    def bug_id(self):
        """
        Abstract methods to get the bug ID
        :return: str - Bug ID
        """
        pass

    @staticmethod
    @abstractmethod
    def requirements(self):
        """
        Requirements for this bug check to check the bug. These will be passed as kwargs to to
        bug checker function.

        Current support values are:
            ip_address - IP address of device
            connection - netmiko.ConnectionHandler connection to the device
        :return: list of requirements
        """
        pass

    @staticmethod
    @abstractmethod
    def manufacture(self):
        """
        Returns which manufacture this device bug affects
        :return: str
        """
        pass

    @staticmethod
    @abstractmethod
    def enable_mode_required(self):
        """
        Returns if enable mode is required for the bug check
        :return: bool
        """

    @staticmethod
    @abstractmethod
    def affected_devices(self):
        """
        Return list devices types which are affected by this put
        ["Switch","Router","Firewall","AP"]
        :return: list
        """
        pass

    @staticmethod
    @abstractmethod
    def remediate_implimented(self):
        """
        Check if remediate function implemented
        :return: bool
        """
        pass


    @abstractmethod
    def remediate_bug(self):
        """
        Abstract method to resolve the bug. Thorws NotImplemented if bug fix code is not implmented
        :return: bool if bug was remediated
        """
        pass
