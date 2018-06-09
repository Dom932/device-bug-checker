import pytest
from tests.test_helpers import MockConnection
from devices import BaseDevice
from devices.autodetect import AutoDetect

cred = {'username': 'u', 'password': 'p', 'secret': 's'}

init = {
    'ipaddr': '192.168.254.4',
    'credentials': cred,
    'hostname': 'device1',
    'version': '1.0'
}


@pytest.fixture
def device():

    d = AutoDetect(**init)

    command_list = {
        None: None
    }

    mock_param = {
        'ip': init['ipaddr'],
        'hostname': init['hostname'],
        'device_type': d.device_type,
        'username': cred['username'],
        'password': cred['password'],
        'secret': cred['secret'],
        'command_list': command_list
    }

    mock = MockConnection(**mock_param)
    d.connection = mock
    return d


class TestAutoDetect:

    def test_instance(self, device):
        """ Test device object type """
        assert isinstance(device, AutoDetect)
        assert isinstance(device, BaseDevice)

    def test_init(self, device):
        """ Test  __init__"""
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
        assert device.manufacture == "autodetect"

    def test_device_type(self, device):
        """ Test device_type """
        assert device.device_type == ("autodetect",)

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
        assert device.version == "unknown"
        device._version = '1.1.1'
        assert device.version == "1.1.1"

    def test_hostname(self, device):
        """ Test hostname attribute """
        device._hostname = None
        assert device.hostname == init['hostname']
        device._hostname = "host123"
        assert device.hostname == "host123"

# TODO - test check bug
