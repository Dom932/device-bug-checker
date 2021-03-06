from devices.autodetect import AutoDetect
from devices.base_device import BaseDevice
from devices.cisco import CiscoIOS
from devices.cisco import CiscoIOSSSHTelnet
from devices.cisco import CiscoIOSTelnet
from devices.cisco import CiscoWLC
from devices.cisco import CiscoASA
from devices.cisco import CiscoNXOS
from devices.linux import Linux


class DeviceClassMapper:
    """
    Class to map a device type to a device class
    """

    @staticmethod
    def get_device_class(device_type):
        """
        Static method to map a device type to a device class
        :param device_type: device type
        :type device_type: str
        :return: Device Class
        :raises KeyError: If unknown device_type is used
        """
        device_class_mapper = {
            None: AutoDetect,
            'BaseDevice': BaseDevice,
            'AutoDetect': AutoDetect,
            'CiscoIOS': CiscoIOS,
            'CiscoIOSSSHTelnet': CiscoIOSSSHTelnet,
            'CiscoIOSTelnet': CiscoIOSTelnet,
            'CiscoWLC': CiscoWLC,
            'CiscoASA': CiscoASA,
            'CiscoNXOS': CiscoNXOS,

            'Linux': Linux
        }

        try:
            return device_class_mapper[device_type]
        except KeyError:
            return device_class_mapper['AutoDetect']
