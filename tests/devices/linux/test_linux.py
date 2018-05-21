import pytest

from devices import BaseDevice
from devices.linux import Linux

cred = {'username': 'u', 'password': 'p', 'secret': 's'}

init = {
    'ipaddr': '192.168.254.4',
    'credentials': cred,
    'hostname': 'device1',
    'version': '1.0'
}


@pytest.fixture
def device():
    class MockConnection:
        """ Mocking class for connection """

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
            if command == "uname -r":
                return init['version']
            elif command == "hostname":
                return init['hostname']

    d = Linux(**init)
    d.connection = MockConnection()
    return d


class TestCiscoIOS:

    def test_instance(self, device):
        """ Test device object type """
        assert isinstance(device, Linux)
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
        assert device.manufacture == "linux"

    def test_device_type(self, device):
        """ Test device_type """
        assert device.device_type == "linux"

    def test_enable_mode(self, device):
        """ Test entering / existing enable mode"""
        assert device.check_enable_mode() == False
        device.enter_enable_mode()
        assert device.check_enable_mode() == True
        device.exit_enable_mode()
        assert device.check_enable_mode() == False

    def test_set_version(self, device):
        """ Test set_version to set IOS version"""
        device.version = None
        assert device.version is None
        device.set_version()
        assert device.version == init['version']

    def test_set_hostname(self, device):
        """ Test set_hostname to set hostname """
        device.hostname = None
        assert device.hostname is None
        device.set_hostname()
        assert device.hostname == init['hostname']

# TODO - test check bug

