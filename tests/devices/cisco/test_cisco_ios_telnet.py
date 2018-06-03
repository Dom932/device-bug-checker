import pytest

from devices import BaseDevice
from devices.cisco import BaseCisco
from devices.cisco import CiscoIOSTelnet

cred = {'hostname': 'u', 'password': 'p', 'secret': 's'}

init = {
    'ipaddr': '192.168.254.4',
    'credentials': cred,
    'hostname': 'device1',
    'version': '1.0'
}

sh_ver_output1 = "Cisco IOS Software, 3600 Software (C3660-I-M), Version 12.3(4)T\nTAC Support: " \
                "http://www.cisco.com/tac\nCopyright (c) 1986-2003 by Cisco Systems, Inc.\nCompiled Thu 18-Sep-03 " \
                "15:37 by ccai\n\nROM: System Bootstrap, Version 12.0(6r)T, RELEASE SOFTWARE (fc1)\nROM: \n\nC3660-1 " \
                "uptime is 1 week, 3 days, 6 hours, 41 minutes\nSystem returned to ROM by power-on\nSystem image file" \
                "is 'slot0:tftpboot/c3660-i-mz.123-4.T'\n\nCisco 3660 (R527x) processor (revision 1.0) with " \
                "57344K/8192K bytes of memory.\nProcessor board ID JAB000000FF\nR527x CPU at 225Mhz, Implementation " \
                "40, Rev 10.0, 2048KB L2 Cache\n\n3660 Chassis type: ENTERPRISE\n2 FastEthernet interfaces\n4 Serial " \
                "interfaces\nDRAM configuration is 64 bits wide with parity disabled.\n125K bytes of NVRAM.\n16384K " \
                "bytes of processor board System flash (Read/Write)\n\nFlash card inserted. Reading " \
                "filesystem...done.\n20480K bytes of processor board PCMCIA Slot0 flash (Read/Write)\n\nConfiguration" \
                "register is 0x2102\n "


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

    d = CiscoIOSTelnet(**init)
    d.connection = MockConnection()
    return d


class TestCiscoIOS:

    def test_instance(self, device):
        """ Test device object type """
        assert isinstance(device, CiscoIOSTelnet)
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
        assert device.device_type == "cisco_ios_telnet"

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
        assert device.version == "12.3(4)T"
        device._version = "1.1.1"
        assert device.version == "1.1.1"

    def test_hostname(self, device):
        """ Test hostname attribute """
        device._hostname = None
        assert device.hostname == init['hostname']
        device._hostname = "host123"
        assert device.hostname == "host123"


# TODO - test check bug

