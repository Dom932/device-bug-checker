
class MockConnection():
    """
    Mock Connection class to mock basic functionality of netmiko to perform test with
    """

    def __init__(self, ip, hostname, device_type, username, password, secret=None, command_list=None):
        """
        Init method
        :param ip: IP address of device
        :type ip: str
        :param hostname: hostname of device - required for find_prompt
        :type hostname: str
        :param device_type: device type of device connecting to
        :type device_type: str
        :param username: username
        :type username: str
        :param password: password
        :type password: str
        :param secret: secret
        :type secret: str
        :param command_list: dictionary of all commands that will be mocked (key) and output (value). If state needs
        to be retained, the value should be a defined method
        :type command_list: dict
        """
        self.ip = ip
        self.hostname = hostname
        self.device_type = device_type
        self.username = username
        self.password = password
        self.secret = secret
        self.command_list = command_list
        self.enable_mode = False
        self.conection = True

    def connect(self):
        """ Connect method """
        self.conection = True

    def disconnect(self):
        """ Disconnect method """
        self.disconnect = False

    def find_prompt(self):
        """ Returns the cmd prompt of device """
        return f"{self.hostname}#"

    def is_alive(self):
        """ Checks if the connection is still alive"""
        return self.conection

    def enable(self):
        """ Enter enable mode """
        self.enable_mode = True

    def exit_enable_mode(self):
        """ Exit enable mode """
        self.enable_mode = False

    def check_enable_mode(self):
        """
        Check if currently in enable mode
        :return: bool
        """
        return self.enable_mode

    def send_command(self, command):
        """
        Sends command to device.


        :param command: command to be exicuted on device
        :type command: str
        :return: output
        """
        return self.command_list[command]

    def send_config_set(self,commands):
        """
        Send a set of commands to device.
        Command will be looked up in send_command
        :param commands: list of commands to send to device
        :type command: list
        :return: output
        """
        output = []
        for c in commands:
            output += self.command_list(c)
        return output
