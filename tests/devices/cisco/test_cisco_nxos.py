import pytest

from devices import BaseDevice
from devices.cisco import BaseCisco
from devices.cisco import CiscoNXOS

cred = {'hostname': 'u', 'password': 'p', 'secret': 's'}

init = {
    'ipaddr': '192.168.254.4',
    'credentials': cred,
    'hostname': 'device1',
    'version': '1.0'
}

sh_ver_output1 = "Software\n  BIOS:      version 1.2.0\n  loader:    version N/A\n  kickstart: version 6.0(2)U2(5)\n " \
                 " system:    version 6.0(2)U2(5)\n  Power Sequencer Firmware:\n             Module 1: version v4.4\n" \
                 "  BIOS compile time:       08/25/2011\n  kickstart image file is: " \
                 "bootflash:///n3000-uk9-kickstart.6.0.2.U2.5.bin\n  kickstart compile time:  5/8/2014 16:00:00 [" \
                 "05/09/2014 03:38:26]\n  system image file is:    bootflash:///n3000-uk9.6.0.2.U2.5.bin\n  system " \
                 "compile time:     5/8/2014 16:00:00 [05/09/2014 05:30:06]\n "


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

    d = CiscoNXOS(**init)
    d.connection = MockConnection()
    return d


class TestCiscoIOS:

    def test_instance(self, device):
        """ Test device object type """
        assert isinstance(device, CiscoNXOS)
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
        assert device.device_type == "cisco_nxos"

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
        assert device.version == "6.0(2)U2(5)"
        device._version = '1.1.1'
        assert device.version == "1.1.1"

    def test_hostname(self, device):
        """ Test hostname attribute """
        device._hostname = None
        assert device.hostname == init['hostname']
        device._hostname = "host123"
        assert device.hostname == "host123"


# TODO - test check bug

