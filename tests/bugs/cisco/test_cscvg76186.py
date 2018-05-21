import pytest

from bugs.cisco import CSCvg76186

unaffected_output1 = 'Role: Client (SmartInstall Disabled)'
unaffected_output2 = 'Capability: Client\nOper Mode: Disabled\nRole: NA'

affected_output1 = 'Role: Client (SmartInstall enabled)'
affected_output2 = 'Capability: Client\nOper Mode: Enabled\nRole: Client'

not_supported = 'Command not supported on platform'


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

    def test_requirements(self, bug):
        """ Test requirements """
        assert bug.requirements == ['connection']

    def test_get_bug_id(self, bug):
        """ Test get_bug_id """
        assert bug.bug_id == 'CSCvg76186'

    def test_affected_devices(self, bug):
        """ Test affected_devices """
        assert bug.affected_devices == ['Switch']

    def test_remediate_implimented(self, bug):
        """ Test remediate_implemented"""
        assert bug.remediate_implimented is False

    def test_manufacture(self, bug):
        """ Test manufacture """
        assert bug.manufacture == 'Cisco'

    def test_remediate(self, bug):
        """ Test remediate not implmented """
        with pytest.raises(Exception):
            bug.remediate()

    def test_check_bug_unaffected1(self, bug, mock_connection):
        """ Test check_bug with unaffected device """
        mock_connection.vstack_output = unaffected_output1
        result = bug.check_bug(mock_connection)
        assert result.impacted is False

    def test_check_bug_unaffected2(self, bug, mock_connection):
        """ Test check_bug with unaffected device """
        mock_connection.vstack_output = unaffected_output2
        result = bug.check_bug(mock_connection)
        assert result.impacted is False

    def test_check_bug_affected1(self, bug, mock_connection):
        """ Test check_bug with affected device """
        mock_connection.vstack_output = affected_output1
        result = bug.check_bug(mock_connection)
        assert result.impacted is True

    def test_check_bug_affected2(self, bug, mock_connection):
        """ Test check_bug with affected device """
        mock_connection.vstack_output = affected_output2
        result = bug.check_bug(mock_connection)
        assert result.impacted is True

    def test_check_bug_command_not_supported(self, bug, mock_connection):
        """ Check output from a command not supported"""
        result = bug.check_bug(mock_connection)
        assert result.impacted is False
        assert result.output == not_supported

    def test_enable_mode_required(self,bug):
        """ Test if enable mode is required """
        assert bug.enable_mode_required is False