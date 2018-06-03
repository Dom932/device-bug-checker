import pytest

from devices import BaseDevice
from devices.cisco import BaseCisco
from devices.cisco import CiscoASA

cred = {'hostname': 'u', 'password': 'p', 'secret': 's'}

init = {
    'ipaddr': '192.168.254.4',
    'credentials': cred,
    'hostname': 'device1',
    'version': '1.0'
}

sh_ver_output1 = "Cisco Adaptive Security Appliance Software Version 8.4(1.11)\nCompiled on Tue 14-Dec-10 12:00 by " \
                 "builders\nSystem image file is 'disk0:/asa841-11-k8.bin' "


@pytest.fixture
def device():
    class MockConnection:
        """ Mocking class for connection """
        def __init__(self):
            self.connection = True
            self.enable_mode = False

        def disconnect(self):
            self.connection = False

        def is_alive(self):
            return self.connection

        def enable(self):
            self.enable_mode = True

        def check_enable_mode(self):
            return self.enable_mode

        def exit_enable_mode(self):
            self.enable_mode = False

        def find_prompt(self):
            return f"{init['hostname']}#"

        def send_command(self, command):
            if command.lower() == "sh ver":
                return sh_ver_output1
            else:
                return None

    d = CiscoASA(**init)
    d.connection = MockConnection()
    return d


class TestCiscoASA:

    def test_instance(self, device):
        """ Test device object type """
        assert isinstance(device, CiscoASA)
        assert isinstance(device, BaseCisco)
        assert isinstance(device, BaseDevice)

    def test_init(self, device):
        """ Test __init__"""
        assert device.ipaddr is init['ipaddr']
        assert device.credentials is cred
        assert device.hostname is init['hostname']
        assert device.version is init['version']
        assert device.connection is not None

    def test_check_connection(self, device):
        """ Test check_connection """
        assert device.check_connection() is True
        device.disconnect()
        assert device.check_connection() is False

    def test_disconnect(self, device):
        """ Test close_connection """
        assert device.connection is not None
        device.disconnect()
        assert device.connection is None

    def test_manufacture(self, device):
        """ Test manufacture """
        assert device.manufacture == "cisco"

    def test_device_type(self, device):
        """ Test device_type """
        assert device.device_type == "cisco_asa"

    def test_enable_mode(self, device):
        """ Test entering / existing enable mode"""
        assert device.check_enable_mode() is False
        device.enter_enable_mode()
        assert device.check_enable_mode() is True
        device.exit_enable_mode()
        assert device.check_enable_mode() is False

    def test_version(self, device):
        """ Test version attribute """
        device._version = None
        assert device.version == "8.4(1.11)"
        device._version = "1.1.1"
        assert device.version == "1.1.1"

    def test_hostname(self, device):
        """ Test hostname attribute """
        device._hostname = None
        assert device.hostname == init['hostname']
        device._hostname = "host123"
        assert device.hostname == "host123"


# TODO - test check bug

