import getpass
import logging
from datetime import datetime
from pathlib import Path


class DeviceHelper:
    """
    Helper class for connection related tasks
    """

    _logger = logging.getLogger(__name__)

    @staticmethod
    def get_credentials():
        """
        Method to guide the user through building a credential set which can be used to provide
        credentials to connect_to_device() method

        :return: list - a list containing credential sets (dictionary)
        """

        credential_set = []

        valid_input = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

        while True:

            username = input("Please enter a username: ")
            password = getpass.getpass()

            credential = {"username": username, "password": password}

            while True:
                secret = input("Do you need a secret? [yes/no]: ").lower()
                if secret in valid_input:
                    if valid_input[secret]:
                        secret = getpass.getpass(prompt="Please enter a secret: ")
                        credential["secret"] = secret
                        break
                    else:
                        break

            credential_set.append(credential)

            while True:

                additional_credentials = input("Do you need to provide additional credential? [yes/no]: ").lower()

                if additional_credentials in valid_input:

                    if not valid_input[additional_credentials]:
                        return credential_set
                    else:
                        break

    @staticmethod
    def backup_config(config, location, hostname):
        """
        Write a config to backup

        :param config: config to write to file
        :type config: str
        :param location: Directory to save config to
        :param hostname:

        """
        path = Path(location)

        if path.is_dir():

            dt = datetime.now()
            dt = dt.strptime(format="%Y-%m-%d_%H-%m")
            filename = f"{hostname}_{dt}.txt"
            path = path / filename

            with path.open(mode="w") as file:
                file.writelines(config)
        else:
            raise ValueError(f"Location is not a directory - {location}")
