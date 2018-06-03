import pytest

from bugs.cisco import CSCvg76186

unaffected_output1 = "Role: Client (SmartInstall Disabled)"
unaffected_output2 = "Capability: Client\nOper Mode: Disabled\nRole: NA"

affected_output1 = "Role: Client (SmartInstall enabled)"
affected_output2 = "Capability: Client\nOper Mode: Enabled\nRole: Client"

not_supported = "Command not supported on platform"


@pytest.fixture()
def bug():
    return CSCvg76186()


@pytest.fixture()
def mock_connection():
    class MockConnection:
        """ Mocking class for connection """
        def __init__(self):
            self.connection = True
            self.vstack_output = not_supported

        def disconnect(self):
            self.connection = False

        def is_alive(self):
            return self.connection

        def send_command(self, input):
            return self.vstack_output

    return MockConnection()


class TestCSCvg76186:

    def test_instance(self, bug):
        """ Test object instance """
        assert isinstance(bug, CSCvg76186)
        assert isinstance(bug, CSCvg76186)

    def test_bug_description(self):
        """ Test bug_description method. Note only tests that result is not null"""
        assert CSCvg76186.bug_description() is not None

    def test_bug_reference(self):
        """ Test bug_reference method. Note only tests that result is not null"""
        assert CSCvg76186.bug_reference() is not None

    def test_manufacture_bug_id(self):
        """ Test manufacture_bug_id method """
        assert CSCvg76186.manufacture_bug_id() == "CSCvg76186"

    def test_cve_id(self):
        """ Test cve_id method """
        assert CSCvg76186.cve_id() == "CVE-2018-0171"

    def test_bug_severity(self):
        """ Tesht bug_severity method"""
        assert CSCvg76186.bug_severity() == "Critical"

    def test_requirements(self):
        """ Test requirements method """
        assert CSCvg76186.requirements() == ['connection']

    def test_manufacture(self):
        """ Test manufacture method """
        assert CSCvg76186.manufacture() == "Cisco"

    def test_enable_mode_required(self):
        """ Test if enable_mode_required method """
        assert CSCvg76186.enable_mode_required() is False

    def test_affected_devices(self):
        """ Test affected_devices method """
        assert CSCvg76186.affected_devices() == ['Switch']

    def test_remediate_implimented(self):
        """ Test remediate_implemented method """
        assert CSCvg76186.remediate_implemented() is False

    def test_check_bug_unaffected1(self, bug, mock_connection):
        """ Test check_bug method with an unaffected device """
        mock_connection.vstack_output = unaffected_output1
        result = bug.check_bug(mock_connection)
        assert result.impacted is False

    def test_check_bug_unaffected2(self, bug, mock_connection):
        """ Test check_bug method with an unaffected device """
        mock_connection.vstack_output = unaffected_output2
        result = bug.check_bug(mock_connection)
        assert result.impacted is False

    def test_check_bug_affected1(self, bug, mock_connection):
        """ Test check_bug method with an affected device """
        mock_connection.vstack_output = affected_output1
        result = bug.check_bug(mock_connection)
        assert result.impacted is True

    def test_check_bug_affected2(self, bug, mock_connection):
        """ Test check_bug method with an affected device """
        mock_connection.vstack_output = affected_output2
        result = bug.check_bug(mock_connection)
        assert result.impacted is True

    def test_check_bug_command_not_supported(self, bug, mock_connection):
        """ Check check_bug method output returns not supported when it is unable to get vstack output"""
        result = bug.check_bug(mock_connection)
        assert result.impacted is False
        assert result.output == not_supported

    def test_remediate(self, bug):
        """ Test remediate method not implemented """
        with pytest.raises(Exception):
            bug.remediate()
