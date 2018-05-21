import logging
from abc import ABC, abstractmethod
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
from bugs import BaseBug


class ConnectionException(Exception):
    """
    Unable to connect to device
    """
    pass


class BaseDevice(ABC):
    """
    Base class which all devices must inherit from
    """

    _logger = logging.getLogger("BugChecker.Device")

    def __init__(self, ipaddr=None, credentials=None, hostname=None, version=None, **kwargs):
        self.ipaddr = ipaddr
        self.credentials = credentials
        self.hostname = hostname
        self.version = version
        self.bugs = {}
        self.connection = None

    @property
    @abstractmethod
    def manufacture(self):
        """
        Returns manufacture of device
        :param self:
        :return str
        """
        pass

    @property
    @abstractmethod
    def device_type(self):
        """
        Returns device type
        :param self:
        :return lst
        """
        pass

    @abstractmethod
    def set_version(self):
        """
        Set object version attribute by connecting to device and querying it
        :return:
        """
        pass

    @abstractmethod
    def set_hostname(self):
        """
        set object hostname attribute by conneng to the device and querting it
        :return: str
        """
        pass

    def check_bug(self, bug_check_obj):
        """
        Check a bug against the device. The outcome will be added to the device object bug property
        :param bug_check_obj:
        :type bug_check_obj: BaseDeviceChecker
        :return bool: idicates if the device is inpacted by the bug
        :raises ValueError: If a unknown object is passed
        """

        if isinstance(bug_check_obj, BaseBug):

            # Get list of requirements
            requirements = bug_check_obj.requirements
            self._logger.debug(f"{self.ipaddr} - Bug {bug_check_obj.bug_id} requirements: {requirements}")

            kwargs = {}

            if 'connection' in requirements:
                kwargs['connection'] = self.connection
            if 'ip_address' in requirements:
                kwargs['ip_address'] = self.ipaddr
            if 'credentials' in requirements:
                kwargs['credentials'] = self.credentials

            self._logger.debug(f"{self.ipaddr} - Checking if connection is established")
            if self.check_connection():

                self._logger.debug(f"{self.ipaddr} - Connection is established")

                result = bug_check_obj.check_bug(**kwargs)
                bug_id = bug_check_obj.bug_id
                self.bugs[bug_id] = result

                self._logger.debug(f"{self.ipaddr} - Bug ID: {bug_id} Result: {result}")

                if result.impacted:
                    return True
                else:
                    return False

            else:
                self._logger.error(f"{self.ipaddr} - No connection to device established")
                raise ConnectionException("No connection to device established")

        else:
            self._logger.error(f"{self.ipaddr} - Incorrect Object")
            raise ValueError('Incorrect Object passed. Must be of an instance of  BaseBug')

    def connect(self):
        """
        TODO
        :return:
        """

        # verify if that credentials is not empty
        if self.credentials:

            self._logger.info(f"{self.ipaddr} - Attempting to connect")

            # Start populating device dictionary to pass to netmiko
            device = {
                "ip": self.ipaddr
            }

            # convert credentials to a list if its just a dictionary
            if isinstance(self.credentials, dict):
                self.credentials = [self.credentials]
            try:
                for c in self.credentials:

                    # set username / password / secret
                    if "username" in c:
                        device["username"] = c["username"]

                    if "password" in c:
                        device["password"] = c["password"]

                    if "secret" in c:
                        device["secret"] = c["secret"]
                    else:
                        # if no secret then remove it
                        device.pop("secret", None)

                    device["device_type"] = self.device_type

                    try:
                        self._logger.debug(f"{self.ipaddr} - Attempting to connect using "
                                           f"device type: {self.device_type}")
                        self.connection = ConnectHandler(**device)
                        self.set_hostname()
                        self._logger.debug(f"{self.ipaddr} - Hostname: {self.hostname}")
                        self.set_version()
                        self._logger.debug(f"{self.ipaddr} - Version: {self.version}")
                        self._logger.info(f"{self.ipaddr} - Connection established")
                        return

                    except NetMikoAuthenticationException:
                        # ignore except - unable to connect based on current User/pass type combo
                        # Move onto next set
                        self._logger.debug(f"{self.ipaddr} - Current username/password incorrect")
                        pass
                    except NetMikoTimeoutException as e:
                        # unable to connect to device
                        self._logger.info(f"{self.ipaddr} - Connection timeout")
                        raise e

                # If this point is reached no connection was established
                self._logger.error(f"{self.ipaddr} - Unable to connect to device")
                raise ConnectionException(f"{self.ipaddr} - Unable to connect to device")

            except NetMikoTimeoutException:
                raise ConnectionException(f"{self.ipaddr} - Connection to device timed out")
        else:
            self._logger.error("No credentials provided")
            raise ConnectionException("No Credentials provided")

    def check_connection(self):
        """
        Check if connection is still established
        :param self:
        :return bool: indicates if the connection to device is still established
        """
        if not self.connection:
            return False
        else:
            return self.connection.is_alive()

    def disconnect(self):
        """
        Close the connection to the device
        :param self:
        """
        self.connection.disconnect()
        self.connection = None

    def enter_enable_mode(self):
        """
        Enter enable mode on device
        :return:
        """
        if self.connection:
            self.connection.enable()

    def exit_enable_mode(self):
        """
        Exit enable mode
        :return:
        """
        if self.connection:
            if self.connection.check_enable_mode():
                self.connection.exit_enable_mode()
                
    def check_enable_mode(self):
        """
        Check if connection is in enable mode
        :return: bool if device is in enable mode
        """
        if self.connection:
            return self.connection.check_enable_mode()
        else:
            return False